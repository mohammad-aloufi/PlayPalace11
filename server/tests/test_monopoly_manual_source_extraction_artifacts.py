from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
EXTRACTED_DIR = REPO_ROOT / "server/games/monopoly/manual_rules/extracted"
MANIFEST_PATH = EXTRACTED_DIR / "manifest.json"
ANCHOR_INDEX_PATH = REPO_ROOT / "server/games/monopoly/catalog/special_board_anchor_index.json"
EXPECTED_FALLBACK_MODES = {
    "marvel_flip": "strings_fallback",
}


def _load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_manifest_covers_all_anchor_board_ids() -> None:
    anchor_rows = _load_json(ANCHOR_INDEX_PATH)
    expected_board_ids = {
        row["board_id"]
        for row in anchor_rows
        if row.get("board_id")
    }
    manifest_rows = _load_json(MANIFEST_PATH)
    manifest_board_ids = {row["board_id"] for row in manifest_rows}
    assert expected_board_ids <= manifest_board_ids


def test_manifest_entries_are_valid_or_known_exceptions() -> None:
    manifest_rows = _load_json(MANIFEST_PATH)
    failed_board_ids = [row["board_id"] for row in manifest_rows if row.get("status") != "ok"]
    assert failed_board_ids == []

    for row in manifest_rows:
        board_id = row["board_id"]
        assert row.get("status") == "ok"

        assert row.get("page_count", 0) > 0
        assert row.get("text_char_count", 0) > 0
        assert row.get("pdf_sha256")
        assert row.get("text_sha256")
        extraction_mode = row.get("extraction_mode", "pypdf")
        expected_mode = EXPECTED_FALLBACK_MODES.get(board_id, "pypdf")
        assert extraction_mode == expected_mode

        text_path = Path(str(row["text_path"]))
        if not text_path.is_absolute():
            text_path = REPO_ROOT / text_path
        assert text_path.exists(), f"missing extracted text for {board_id}"
        text_content = text_path.read_text(encoding="utf-8")
        assert "=== Page 1 ===" in text_content
        assert len(text_content) >= row["text_char_count"]

        meta_path = EXTRACTED_DIR / f"{board_id}.json"
        assert meta_path.exists(), f"missing metadata for {board_id}"
