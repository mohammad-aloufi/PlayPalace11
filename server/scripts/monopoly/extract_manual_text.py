"""Extract manual text artifacts from board-linked Monopoly PDF manuals."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
from pathlib import Path
import re
import sys
from typing import Any
from urllib.request import Request, urlopen


# Allow direct script execution: python server/scripts/monopoly/extract_manual_text.py
if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

try:
    from pypdf import PdfReader
    import pypdf.filters as pypdf_filters
except ModuleNotFoundError as error:  # pragma: no cover - runtime dependency guard
    raise SystemExit(
        "Missing optional dependency 'pypdf'. Install with: "
        "./.venv/bin/python -m pip install pypdf"
    ) from error


BOARD_ZLIB_RETRY_LIMITS: dict[str, int] = {
    # This manual includes a very large compressed stream that exceeds
    # the default extraction cap.
    "marvel_flip": 252_000_000,
}


def _stable_dump(path: Path, data: Any) -> None:
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    tmp_path.write_text(
        json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False),
        encoding="utf-8",
    )
    tmp_path.replace(path)


def _fetch_pdf_bytes(url: str, timeout: float) -> bytes:
    request = Request(
        url,
        headers={"User-Agent": "PlayPalace-Monopoly-ManualExtract/1.0"},
    )
    with urlopen(request, timeout=timeout) as response:
        return response.read()


def _extract_pages(pdf_bytes: bytes) -> list[str]:
    reader = PdfReader(io.BytesIO(pdf_bytes))
    pages: list[str] = []
    for page in reader.pages:
        text = page.extract_text() or ""
        pages.append(text.strip())
    return pages


def _extract_text_strings_fallback(pdf_bytes: bytes, *, max_lines: int = 12_000) -> str:
    decoded = pdf_bytes.decode("latin-1", errors="ignore")
    pattern = re.compile(r"[A-Za-z0-9][A-Za-z0-9 .,;:!?()\-/'\"&%+=_]{5,}")
    lines: list[str] = []
    seen: set[str] = set()
    for match in pattern.findall(decoded):
        normalized = " ".join(match.split())
        if len(normalized) < 6:
            continue
        if normalized in seen:
            continue
        seen.add(normalized)
        lines.append(normalized)
        if len(lines) >= max_lines:
            break
    return "\n".join(lines).strip()


def _extract_pages_with_fallback(
    board_id: str,
    pdf_bytes: bytes,
    base_zlib_limit: int,
) -> tuple[list[str], int, str]:
    attempted_limits: list[int] = [base_zlib_limit]
    board_retry_limit = BOARD_ZLIB_RETRY_LIMITS.get(board_id)
    if (
        board_retry_limit is not None
        and board_retry_limit > base_zlib_limit
        and board_retry_limit not in attempted_limits
    ):
        attempted_limits.append(board_retry_limit)

    last_error: Exception | None = None
    for index, zlib_limit in enumerate(attempted_limits):
        pypdf_filters.ZLIB_MAX_OUTPUT_LENGTH = zlib_limit
        try:
            if index > 0:
                print(f"[retry] {board_id}: trying zlib limit {zlib_limit}")
            pages = _extract_pages(pdf_bytes)
            return pages, zlib_limit, "pypdf"
        except Exception as error:  # pragma: no cover - runtime decoding path
            last_error = error
            message = str(error)
            if "Limit reached while decompressing." not in message:
                raise
            if index == len(attempted_limits) - 1:
                fallback_text = _extract_text_strings_fallback(pdf_bytes)
                if fallback_text:
                    print(f"[fallback] {board_id}: using strings extraction fallback")
                    return [fallback_text], zlib_limit, "strings_fallback"
                raise

    assert last_error is not None
    raise last_error


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _select_targets(
    anchor_rows: list[dict[str, Any]],
    families: set[str],
    board_ids: set[str],
) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    for row in anchor_rows:
        board_id = str(row.get("board_id", ""))
        family = str(row.get("family", ""))
        if board_ids and board_id in board_ids:
            selected.append(row)
            continue
        if families and family in families:
            selected.append(row)
    selected.sort(key=lambda row: str(row.get("board_id", "")))
    return selected


def run_extraction(
    *,
    families: set[str],
    board_ids: set[str],
    anchor_index_path: Path,
    manual_rules_dir: Path,
    output_dir: Path,
    timeout: float,
    zlib_max_output_length: int,
    merge_manifest: bool,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    anchor_rows = _load_json(anchor_index_path)
    targets = _select_targets(anchor_rows, families=families, board_ids=board_ids)
    if not targets:
        raise SystemExit("No matching boards selected.")

    manifest_rows: list[dict[str, Any]] = []
    target_board_ids = {str(row.get("board_id", "")) for row in targets}
    if merge_manifest:
        existing_manifest_path = output_dir / "manifest.json"
        if existing_manifest_path.exists():
            existing_rows = _load_json(existing_manifest_path)
            if isinstance(existing_rows, list):
                for row in existing_rows:
                    if not isinstance(row, dict):
                        continue
                    board_id = str(row.get("board_id", ""))
                    if board_id and board_id not in target_board_ids:
                        manifest_rows.append(row)
    for row in targets:
        board_id = str(row["board_id"])
        family = str(row.get("family", ""))
        anchor_edition_id = str(row.get("anchor_edition_id", ""))
        rule_path = manual_rules_dir / f"{board_id}.json"
        if not rule_path.exists():
            manifest_rows.append(
                {
                    "board_id": board_id,
                    "family": family,
                    "anchor_edition_id": anchor_edition_id,
                    "status": "missing_manual_rule_file",
                }
            )
            continue

        rule_payload = _load_json(rule_path)
        manual_source = (
            rule_payload.get("mechanics", {}).get("manual_source", {})
            if isinstance(rule_payload.get("mechanics"), dict)
            else {}
        )
        pdf_url = str(manual_source.get("pdf_url", "")).strip()
        if not pdf_url:
            manifest_rows.append(
                {
                    "board_id": board_id,
                    "family": family,
                    "anchor_edition_id": anchor_edition_id,
                    "status": "missing_pdf_url",
                }
            )
            continue

        try:
            pdf_bytes = _fetch_pdf_bytes(pdf_url, timeout=timeout)
            pages, used_zlib_limit, extraction_mode = _extract_pages_with_fallback(
                board_id=board_id,
                pdf_bytes=pdf_bytes,
                base_zlib_limit=zlib_max_output_length,
            )
        except Exception as error:  # pragma: no cover - network/runtime failure path
            print(f"[fail] {board_id}: {error}")
            manifest_rows.append(
                {
                    "board_id": board_id,
                    "family": family,
                    "anchor_edition_id": anchor_edition_id,
                    "pdf_url": pdf_url,
                    "status": "failed",
                    "error": str(error),
                    "zlib_limit_attempted": zlib_max_output_length,
                }
            )
            continue

        text_path = output_dir / f"{board_id}.txt"
        text_chunks: list[str] = []
        for idx, text in enumerate(pages, start=1):
            text_chunks.append(f"=== Page {idx} ===\n{text}\n")
        full_text = "\n".join(text_chunks).strip() + "\n"
        text_path.write_text(full_text, encoding="utf-8")

        text_sha256 = hashlib.sha256(full_text.encode("utf-8")).hexdigest()
        pdf_sha256 = hashlib.sha256(pdf_bytes).hexdigest()
        text_char_count = len(full_text)
        meta = {
            "board_id": board_id,
            "family": family,
            "anchor_edition_id": anchor_edition_id,
            "status": "ok",
            "pdf_url": pdf_url,
            "instruction_url": manual_source.get("instruction_url"),
            "filename": manual_source.get("filename"),
            "pdf_sha256": pdf_sha256,
            "pdf_size_bytes": len(pdf_bytes),
            "page_count": len(pages),
            "text_char_count": text_char_count,
            "text_sha256": text_sha256,
            "text_path": str(text_path),
            "zlib_limit_used": used_zlib_limit,
            "extraction_mode": extraction_mode,
        }
        _stable_dump(output_dir / f"{board_id}.json", meta)
        manifest_rows.append(meta)
        print(f"[ok] {board_id}: pages={len(pages)} chars={text_char_count}")

    manifest_rows.sort(key=lambda item: str(item.get("board_id", "")))
    _stable_dump(output_dir / "manifest.json", manifest_rows)

    ok_count = sum(1 for row in manifest_rows if row.get("status") == "ok")
    print(
        f"Wrote extraction artifacts for {ok_count}/{len(manifest_rows)} "
        f"selected boards into {output_dir}"
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract text from Monopoly board manual PDFs into local artifacts."
    )
    parser.add_argument(
        "--family",
        action="append",
        default=[],
        help="Family id from special_board_anchor_index.json (repeatable).",
    )
    parser.add_argument(
        "--board-id",
        action="append",
        default=[],
        help="Explicit board id (repeatable).",
    )
    parser.add_argument(
        "--anchor-index",
        type=Path,
        default=Path("server/games/monopoly/catalog/special_board_anchor_index.json"),
        help="Path to special board anchor index JSON.",
    )
    parser.add_argument(
        "--manual-rules-dir",
        type=Path,
        default=Path("server/games/monopoly/manual_rules/data"),
        help="Directory containing board manual rule JSON files.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("server/games/monopoly/manual_rules/extracted"),
        help="Directory where extracted text/metadata artifacts are written.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=45.0,
        help="Download timeout in seconds for each manual PDF.",
    )
    parser.add_argument(
        "--zlib-max-output-length",
        type=int,
        default=120_000_000,
        help=(
            "pypdf decompression output limit for trusted large manual PDFs "
            "(0 disables limit)."
        ),
    )
    parser.add_argument(
        "--no-merge-manifest",
        action="store_true",
        help="Do not preserve existing manifest rows for non-target boards.",
    )
    args = parser.parse_args()

    families = {value.strip() for value in args.family if value.strip()}
    board_ids = {value.strip() for value in args.board_id if value.strip()}
    if not families and not board_ids:
        raise SystemExit("Provide at least one --family or --board-id selection.")

    run_extraction(
        families=families,
        board_ids=board_ids,
        anchor_index_path=args.anchor_index,
        manual_rules_dir=args.manual_rules_dir,
        output_dir=args.output_dir,
        timeout=args.timeout,
        zlib_max_output_length=args.zlib_max_output_length,
        merge_manifest=not args.no_merge_manifest,
    )


if __name__ == "__main__":
    main()
