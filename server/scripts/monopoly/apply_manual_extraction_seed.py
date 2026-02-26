"""Apply extracted manual metadata into Monopoly manual rule payloads."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


MARVEL_ACTION_SPACE_NAME_OVERRIDES: dict[str, dict[str, str]] = {
    "marvel_80_years": {
        "chance_1": "Catalog",
        "chance_2": "Catalog",
        "chance_3": "Catalog",
        "community_chest_1": "Catalog",
        "community_chest_2": "Catalog",
        "community_chest_3": "Catalog",
        "income_tax": "Infinity Gauntlet",
        "luxury_tax": "Cable & Deadpool",
    },
    "marvel_black_panther_wf": {
        "chance_1": "Wakandan",
        "chance_2": "Wakandan",
        "chance_3": "Wakandan",
        "community_chest_1": "Talokanil",
        "community_chest_2": "Talokanil",
        "community_chest_3": "Talokanil",
    },
    "marvel_deadpool": {
        "chance_1": "Dumb Luck",
        "chance_2": "Dumb Luck",
        "chance_3": "Dumb Luck",
        "community_chest_1": "Pouches",
        "community_chest_2": "Pouches",
        "community_chest_3": "Pouches",
    },
    "marvel_eternals": {
        "chance_1": "Uni-Mind",
        "chance_2": "Uni-Mind",
        "chance_3": "Uni-Mind",
        "community_chest_1": "Arishem's Judgement",
        "community_chest_2": "Arishem's Judgement",
        "community_chest_3": "Arishem's Judgement",
    },
    "marvel_falcon_winter_soldier": {
        "chance_1": "The Shield",
        "chance_2": "The Shield",
        "chance_3": "The Shield",
        "community_chest_1": "The Flag Smashers",
        "community_chest_2": "The Flag Smashers",
        "community_chest_3": "The Flag Smashers",
    },
    "marvel_spider_man": {
        "chance_1": "Daily Bugle",
        "chance_2": "Daily Bugle",
        "chance_3": "Daily Bugle",
        "community_chest_1": "Spider-Sense",
        "community_chest_2": "Spider-Sense",
        "community_chest_3": "Spider-Sense",
    },
    "marvel_super_villains": {
        "chance_1": "Chance",
        "chance_2": "Chance",
        "chance_3": "Chance",
        "community_chest_1": "Reshape the Universe",
        "community_chest_2": "Reshape the Universe",
        "community_chest_3": "Reshape the Universe",
    },
}

MARVEL_DECK_METADATA_OVERRIDES: dict[str, dict[str, str]] = {
    "marvel_80_years": {
        "chance": "Catalog",
        "community_chest": "Catalog",
    },
    "marvel_black_panther_wf": {
        "chance": "Wakandan",
        "community_chest": "Talokanil",
    },
    "marvel_deadpool": {
        "chance": "Dumb Luck",
        "community_chest": "Pouches",
    },
    "marvel_eternals": {
        "chance": "Uni-Mind",
        "community_chest": "Arishem's Judgement",
    },
    "marvel_falcon_winter_soldier": {
        "chance": "The Shield",
        "community_chest": "The Flag Smashers",
    },
    "marvel_spider_man": {
        "chance": "Daily Bugle",
        "community_chest": "Spider-Sense",
    },
    "marvel_super_villains": {
        "chance": "Chance",
        "community_chest": "Reshape the Universe",
    },
}

DISNEY_ACTION_SPACE_NAME_OVERRIDES: dict[str, dict[str, str]] = {
    "disney_animation": {
        "chance_1": "Magic Mirror",
        "chance_2": "Magic Mirror",
        "chance_3": "Magic Mirror",
        "community_chest_1": "Ariel's Treasure Chest",
        "community_chest_2": "Ariel's Treasure Chest",
        "community_chest_3": "Ariel's Treasure Chest",
        "income_tax": "The Evil Queen's Spell",
        "luxury_tax": "Maleficent's Curse",
    },
    "disney_legacy": {
        "chance_1": "Show Time",
        "chance_2": "Show Time",
        "chance_3": "Show Time",
        "community_chest_1": "Magic Moments",
        "community_chest_2": "Magic Moments",
        "community_chest_3": "Magic Moments",
    },
    "disney_lightyear": {
        "chance_1": "Hyperspeed",
        "chance_2": "Hyperspeed",
        "chance_3": "Hyperspeed",
        "community_chest_1": "Crystallic Fusion",
        "community_chest_2": "Crystallic Fusion",
        "community_chest_3": "Crystallic Fusion",
        "income_tax": "Bugs",
        "luxury_tax": "Zyclops",
    },
    "disney_lion_king": {
        "chance_1": "Destiny",
        "chance_2": "Destiny",
        "chance_3": "Destiny",
        "community_chest_1": "Destiny",
        "community_chest_2": "Destiny",
        "community_chest_3": "Destiny",
        "income_tax": "Water Fowl",
        "luxury_tax": "Wild Fire",
    },
    "disney_mickey_friends": {
        "chance_1": "Friendship",
        "chance_2": "Friendship",
        "chance_3": "Friendship",
        "community_chest_1": "Magic Moments",
        "community_chest_2": "Magic Moments",
        "community_chest_3": "Magic Moments",
        "income_tax": "Hot Dog Snack Break",
        "luxury_tax": "Popcorn Snack Break",
    },
    "disney_princesses": {
        "chance_1": "Sorte",
        "chance_2": "Sorte",
        "chance_3": "Sorte",
        "community_chest_1": "Magia",
        "community_chest_2": "Magia",
        "community_chest_3": "Magia",
        "income_tax": "Imposto",
        "luxury_tax": "Imposto",
    },
    "disney_star_wars_dark_side": {
        "chance_1": "The Empire",
        "chance_2": "The Empire",
        "chance_3": "The Empire",
        "community_chest_1": "The Dark Side",
        "community_chest_2": "The Dark Side",
        "community_chest_3": "The Dark Side",
        "income_tax": "Rebel Escape",
        "luxury_tax": "Rebel Attack",
    },
    "disney_villains": {
        "chance_1": "Chance",
        "chance_2": "Chance",
        "chance_3": "Chance",
        "community_chest_1": "Poison Apple",
        "community_chest_2": "Poison Apple",
        "community_chest_3": "Poison Apple",
    },
}

DISNEY_DECK_METADATA_OVERRIDES: dict[str, dict[str, str]] = {
    "disney_animation": {
        "chance": "Magic Mirror",
        "community_chest": "Ariel's Treasure Chest",
    },
    "disney_legacy": {
        "chance": "Show Time",
        "community_chest": "Magic Moments",
    },
    "disney_lightyear": {
        "chance": "Hyperspeed",
        "community_chest": "Crystallic Fusion",
    },
    "disney_lion_king": {
        "chance": "Destiny",
        "community_chest": "Destiny",
    },
    "disney_mickey_friends": {
        "chance": "Friendship",
        "community_chest": "Magic Moments",
    },
    "disney_princesses": {
        "chance": "Sorte",
        "community_chest": "Magia",
    },
    "disney_star_wars_dark_side": {
        "chance": "The Empire",
        "community_chest": "The Dark Side",
    },
    "disney_villains": {
        "chance": "Chance",
        "community_chest": "Poison Apple",
    },
}

STAR_WARS_ACTION_SPACE_NAME_OVERRIDES: dict[str, dict[str, str]] = {
    "star_wars_classic_edition": {
        "chance_1": "Use the Force",
        "chance_2": "Use the Force",
        "chance_3": "Use the Force",
        "community_chest_1": "Hyperspace",
        "community_chest_2": "Hyperspace",
        "community_chest_3": "Hyperspace",
        "income_tax": "Galactic Empire Tax",
        "luxury_tax": "Galactic Empire Tax",
    },
    "star_wars_legacy": {
        "chance_1": "Use the Force",
        "chance_2": "Use the Force",
        "chance_3": "Use the Force",
        "community_chest_1": "Hyperspace",
        "community_chest_2": "Hyperspace",
        "community_chest_3": "Hyperspace",
        "income_tax": "Galactic Empire Tax",
        "luxury_tax": "Galactic Empire Tax",
    },
    "star_wars_mandalorian": {
        "chance_1": "Signet",
        "chance_2": "Signet",
        "chance_3": "Signet",
        "community_chest_1": "Hyperspace Jump",
        "community_chest_2": "Hyperspace Jump",
        "community_chest_3": "Hyperspace Jump",
        "income_tax": "Imperial Credits",
        "luxury_tax": "Imperial Advance",
    },
    "star_wars_mandalorian_s2": {
        "chance_1": "Signet",
        "chance_2": "Signet",
        "chance_3": "Signet",
        "community_chest_1": "Hyperspace Jump",
        "community_chest_2": "Hyperspace Jump",
        "community_chest_3": "Hyperspace Jump",
        "income_tax": "Imperial Credits",
        "luxury_tax": "Imperial Advance",
    },
}

STAR_WARS_DECK_METADATA_OVERRIDES: dict[str, dict[str, str]] = {
    "star_wars_classic_edition": {
        "chance": "Use the Force",
        "community_chest": "Hyperspace",
    },
    "star_wars_legacy": {
        "chance": "Use the Force",
        "community_chest": "Hyperspace",
    },
    "star_wars_mandalorian": {
        "chance": "Signet",
        "community_chest": "Hyperspace Jump",
    },
    "star_wars_mandalorian_s2": {
        "chance": "Signet",
        "community_chest": "Hyperspace Jump",
    },
}

MARIO_ACTION_SPACE_NAME_OVERRIDES: dict[str, dict[str, str]] = {
    "mario_celebration": {
        "chance_1": "Question Block",
        "chance_2": "Question Block",
        "chance_3": "Question Block",
        "community_chest_1": "Community Chest",
        "community_chest_2": "Community Chest",
        "community_chest_3": "Community Chest",
        "income_tax": "Chain Chomp",
        "luxury_tax": "Piranha Plant",
    },
    "mario_collectors": {
        "chance_1": "? Block",
        "chance_2": "? Block",
        "chance_3": "? Block",
        "community_chest_1": "Warp Pipe",
        "community_chest_2": "Warp Pipe",
        "community_chest_3": "Warp Pipe",
    },
    "mario_kart": {
        "chance_1": "Power-Up",
        "chance_2": "Power-Up",
        "chance_3": "Power-Up",
        "community_chest_1": "Grand Prix",
        "community_chest_2": "Grand Prix",
        "community_chest_3": "Grand Prix",
    },
    "mario_movie": {
        "chance_1": "Question Block",
        "chance_2": "Question Block",
        "chance_3": "Question Block",
        "community_chest_1": "Bowser's Fury",
        "community_chest_2": "Bowser's Fury",
        "community_chest_3": "Bowser's Fury",
    },
}

MARIO_DECK_METADATA_OVERRIDES: dict[str, dict[str, str]] = {
    "mario_celebration": {
        "chance": "Question Block",
        "community_chest": "Community Chest",
    },
    "mario_collectors": {
        "chance": "? Block",
        "community_chest": "Warp Pipe",
    },
    "mario_kart": {
        "chance": "Power-Up",
        "community_chest": "Grand Prix",
    },
    "mario_movie": {
        "chance": "Question Block",
        "community_chest": "Bowser's Fury",
    },
}


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, data: Any) -> None:
    path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    path.write_text(path.read_text(encoding="utf-8").rstrip() + "\n", encoding="utf-8")


def _resolve_action_space_overrides(board_id: str) -> dict[str, str]:
    for table in (
        MARVEL_ACTION_SPACE_NAME_OVERRIDES,
        DISNEY_ACTION_SPACE_NAME_OVERRIDES,
        STAR_WARS_ACTION_SPACE_NAME_OVERRIDES,
        MARIO_ACTION_SPACE_NAME_OVERRIDES,
    ):
        overrides = table.get(board_id)
        if overrides:
            return overrides
    return {}


def _resolve_deck_overrides(board_id: str) -> dict[str, str]:
    for table in (
        MARVEL_DECK_METADATA_OVERRIDES,
        DISNEY_DECK_METADATA_OVERRIDES,
        STAR_WARS_DECK_METADATA_OVERRIDES,
        MARIO_DECK_METADATA_OVERRIDES,
    ):
        overrides = table.get(board_id)
        if overrides:
            return overrides
    return {}


def _upsert_citation(payload: dict[str, Any], *, anchor_edition_id: str, extraction_mode: str) -> None:
    citations = payload.get("citations")
    if not isinstance(citations, list):
        return
    for row in citations:
        if row.get("rule_path") == "mechanics.manual_extraction":
            row.update(
                {
                    "edition_id": anchor_edition_id,
                    "page_ref": (
                        "manual-extract:pypdf"
                        if extraction_mode == "pypdf"
                        else "manual-extract:strings-fallback"
                    ),
                    "confidence": "medium" if extraction_mode != "pypdf" else "high",
                }
            )
            return
    citations.append(
        {
            "rule_path": "mechanics.manual_extraction",
            "edition_id": anchor_edition_id,
            "page_ref": (
                "manual-extract:pypdf"
                if extraction_mode == "pypdf"
                else "manual-extract:strings-fallback"
            ),
            "confidence": "medium" if extraction_mode != "pypdf" else "high",
        }
    )


def _upsert_simple_citation(
    payload: dict[str, Any],
    *,
    rule_path: str,
    edition_id: str,
    page_ref: str,
    confidence: str,
) -> None:
    citations = payload.get("citations")
    if not isinstance(citations, list):
        return
    for row in citations:
        if row.get("rule_path") == rule_path:
            row.update(
                {
                    "edition_id": edition_id,
                    "page_ref": page_ref,
                    "confidence": confidence,
                }
            )
            return
    citations.append(
        {
            "rule_path": rule_path,
            "edition_id": edition_id,
            "page_ref": page_ref,
            "confidence": confidence,
        }
    )


def _apply_action_space_name_overrides(payload: dict[str, Any], board_id: str) -> None:
    overrides = _resolve_action_space_overrides(board_id)
    if not overrides:
        return

    board = payload.get("board")
    if not isinstance(board, dict):
        return
    spaces = board.get("spaces")
    if not isinstance(spaces, list):
        return

    for space in spaces:
        if not isinstance(space, dict):
            continue
        space_id = space.get("space_id")
        if not isinstance(space_id, str):
            continue
        new_name = overrides.get(space_id)
        if new_name is not None:
            space["name"] = new_name


def _apply_deck_metadata_overrides(payload: dict[str, Any], board_id: str) -> None:
    deck_overrides = _resolve_deck_overrides(board_id)
    if not deck_overrides:
        return
    mechanics = payload.get("mechanics")
    if not isinstance(mechanics, dict):
        return
    mechanics["decks"] = {
        "chance": deck_overrides["chance"],
        "community_chest": deck_overrides["community_chest"],
    }


def run_seed(
    *,
    anchor_index_path: Path,
    manifest_path: Path,
    manual_rules_dir: Path,
) -> None:
    anchor_rows = _load_json(anchor_index_path)
    manifest_rows = _load_json(manifest_path)

    target_board_ids = {
        str(row["board_id"])
        for row in anchor_rows
        if isinstance(row, dict) and str(row.get("board_id", "")).strip()
    }
    manifest_by_board = {
        row["board_id"]: row
        for row in manifest_rows
        if row.get("board_id") in target_board_ids and row.get("status") == "ok"
    }

    changed = 0
    for board_id in sorted(target_board_ids):
        row = manifest_by_board.get(board_id)
        if row is None:
            continue

        path = manual_rules_dir / f"{board_id}.json"
        if not path.exists():
            continue
        payload = _load_json(path)

        mechanics = payload.get("mechanics")
        if not isinstance(mechanics, dict):
            mechanics = {}
            payload["mechanics"] = mechanics

        extraction_mode = str(row.get("extraction_mode", "pypdf"))
        mechanics["manual_extraction"] = {
            "status": "seeded_from_extracted_manual_text",
            "extraction_mode": extraction_mode,
            "manifest_path": str(manifest_path),
            "text_path": row.get("text_path"),
            "text_sha256": row.get("text_sha256"),
            "pdf_sha256": row.get("pdf_sha256"),
            "pdf_size_bytes": row.get("pdf_size_bytes"),
            "page_count": row.get("page_count"),
        }

        _apply_action_space_name_overrides(payload, board_id)
        _apply_deck_metadata_overrides(payload, board_id)
        _upsert_citation(
            payload,
            anchor_edition_id=str(payload.get("anchor_edition_id", row.get("anchor_edition_id", ""))),
            extraction_mode=extraction_mode,
        )
        edition_id = str(payload.get("anchor_edition_id", row.get("anchor_edition_id", "")))
        action_overrides = _resolve_action_space_overrides(board_id)
        if action_overrides:
            _upsert_simple_citation(
                payload,
                rule_path="board.spaces.chance.name",
                edition_id=edition_id,
                page_ref="manual-extract:action-space-labels",
                confidence="medium",
            )
            _upsert_simple_citation(
                payload,
                rule_path="board.spaces.community_chest.name",
                edition_id=edition_id,
                page_ref="manual-extract:action-space-labels",
                confidence="medium",
            )
        if "income_tax" in action_overrides or "luxury_tax" in action_overrides:
            _upsert_simple_citation(
                payload,
                rule_path="board.spaces.tax.name",
                edition_id=edition_id,
                page_ref="manual-extract:action-space-labels",
                confidence="medium",
            )
        if _resolve_deck_overrides(board_id):
            _upsert_simple_citation(
                payload,
                rule_path="mechanics.decks",
                edition_id=edition_id,
                page_ref="manual-extract:deck-labels",
                confidence="medium",
            )
        _write_json(path, payload)
        changed += 1

    print(f"Seeded manual extraction metadata into {changed} board payload files")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Apply extracted manual metadata into special-board manual rule payloads."
    )
    parser.add_argument(
        "--anchor-index",
        type=Path,
        default=Path("server/games/monopoly/catalog/special_board_anchor_index.json"),
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("server/games/monopoly/manual_rules/extracted/manifest.json"),
    )
    parser.add_argument(
        "--manual-rules-dir",
        type=Path,
        default=Path("server/games/monopoly/manual_rules/data"),
    )
    args = parser.parse_args()

    run_seed(
        anchor_index_path=args.anchor_index,
        manifest_path=args.manifest,
        manual_rules_dir=args.manual_rules_dir,
    )


if __name__ == "__main__":
    main()
