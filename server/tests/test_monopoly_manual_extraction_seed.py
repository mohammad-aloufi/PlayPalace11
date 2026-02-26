from __future__ import annotations

import json
from pathlib import Path

import pytest

from server.games.monopoly.manual_rules.loader import load_manual_rule_set


REPO_ROOT = Path(__file__).resolve().parents[2]
ANCHOR_INDEX_PATH = REPO_ROOT / "server/games/monopoly/catalog/special_board_anchor_index.json"
MANIFEST_PATH = REPO_ROOT / "server/games/monopoly/manual_rules/extracted/manifest.json"


def _load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _target_board_ids() -> list[str]:
    anchor_rows = _load_json(ANCHOR_INDEX_PATH)
    return sorted(
        row["board_id"]
        for row in anchor_rows
        if row.get("board_id")
    )


def test_special_board_rules_include_extraction_seed_metadata() -> None:
    manifest_rows = _load_json(MANIFEST_PATH)
    manifest_by_board = {row["board_id"]: row for row in manifest_rows}

    for board_id in _target_board_ids():
        row = manifest_by_board[board_id]
        rule_set = load_manual_rule_set(board_id)
        mechanics = rule_set.mechanics

        manual_extraction = mechanics.get("manual_extraction")
        assert isinstance(manual_extraction, dict), board_id
        assert manual_extraction.get("status") == "seeded_from_extracted_manual_text"
        assert manual_extraction.get("text_sha256") == row.get("text_sha256")
        assert manual_extraction.get("pdf_sha256") == row.get("pdf_sha256")
        assert manual_extraction.get("page_count") == row.get("page_count")
        assert manual_extraction.get("extraction_mode") == row.get("extraction_mode", "pypdf")

        citation_paths = {citation.rule_path for citation in rule_set.citations}
        assert "mechanics.manual_extraction" in citation_paths


@pytest.mark.parametrize(
    ("board_id", "expected_names", "expected_decks"),
    [
        (
            "star_wars_classic_edition",
            {
                "chance_1": "Use the Force",
                "chance_2": "Use the Force",
                "chance_3": "Use the Force",
                "community_chest_1": "Hyperspace",
                "community_chest_2": "Hyperspace",
                "community_chest_3": "Hyperspace",
                "income_tax": "Galactic Empire Tax",
                "luxury_tax": "Galactic Empire Tax",
            },
            {
                "chance": "Use the Force",
                "community_chest": "Hyperspace",
            },
        ),
        (
            "star_wars_legacy",
            {
                "chance_1": "Use the Force",
                "chance_2": "Use the Force",
                "chance_3": "Use the Force",
                "community_chest_1": "Hyperspace",
                "community_chest_2": "Hyperspace",
                "community_chest_3": "Hyperspace",
                "income_tax": "Galactic Empire Tax",
                "luxury_tax": "Galactic Empire Tax",
            },
            {
                "chance": "Use the Force",
                "community_chest": "Hyperspace",
            },
        ),
        (
            "star_wars_mandalorian",
            {
                "chance_1": "Signet",
                "chance_2": "Signet",
                "chance_3": "Signet",
                "community_chest_1": "Hyperspace Jump",
                "community_chest_2": "Hyperspace Jump",
                "community_chest_3": "Hyperspace Jump",
                "income_tax": "Imperial Credits",
                "luxury_tax": "Imperial Advance",
            },
            {
                "chance": "Signet",
                "community_chest": "Hyperspace Jump",
            },
        ),
        (
            "star_wars_mandalorian_s2",
            {
                "chance_1": "Signet",
                "chance_2": "Signet",
                "chance_3": "Signet",
                "community_chest_1": "Hyperspace Jump",
                "community_chest_2": "Hyperspace Jump",
                "community_chest_3": "Hyperspace Jump",
                "income_tax": "Imperial Credits",
                "luxury_tax": "Imperial Advance",
            },
            {
                "chance": "Signet",
                "community_chest": "Hyperspace Jump",
            },
        ),
    ],
)
def test_star_wars_seed_applies_manual_action_space_labels(
    board_id: str,
    expected_names: dict[str, str],
    expected_decks: dict[str, str],
) -> None:
    rule_set = load_manual_rule_set(board_id)
    by_space_id = {
        row["space_id"]: row["name"]
        for row in rule_set.board.get("spaces", [])
    }
    for space_id, expected_name in expected_names.items():
        assert by_space_id.get(space_id) == expected_name
    assert rule_set.mechanics.get("decks") == expected_decks


@pytest.mark.parametrize(
    ("board_id", "expected_names", "expected_decks"),
    [
        (
            "marvel_80_years",
            {
                "chance_1": "Catalog",
                "chance_2": "Catalog",
                "chance_3": "Catalog",
                "community_chest_1": "Catalog",
                "community_chest_2": "Catalog",
                "community_chest_3": "Catalog",
                "income_tax": "Infinity Gauntlet",
                "luxury_tax": "Cable & Deadpool",
            },
            {
                "chance": "Catalog",
                "community_chest": "Catalog",
            },
        ),
        (
            "marvel_avengers",
            {
                "chance_1": "Stark Industries",
                "chance_2": "Stark Industries",
                "chance_3": "Stark Industries",
                "community_chest_1": "Infinity Gauntlet",
                "community_chest_2": "Infinity Gauntlet",
                "community_chest_3": "Infinity Gauntlet",
                "income_tax": "Ultron",
                "luxury_tax": "Hela",
            },
            {
                "chance": "Stark Industries",
                "community_chest": "Infinity Gauntlet",
            },
        ),
        (
            "marvel_black_panther_wf",
            {
                "chance_1": "Wakandan",
                "chance_2": "Wakandan",
                "chance_3": "Wakandan",
                "community_chest_1": "Talokanil",
                "community_chest_2": "Talokanil",
                "community_chest_3": "Talokanil",
            },
            {
                "chance": "Wakandan",
                "community_chest": "Talokanil",
            },
        ),
        (
            "marvel_deadpool",
            {
                "chance_1": "Dumb Luck",
                "chance_2": "Dumb Luck",
                "chance_3": "Dumb Luck",
                "community_chest_1": "Pouches",
                "community_chest_2": "Pouches",
                "community_chest_3": "Pouches",
            },
            {
                "chance": "Dumb Luck",
                "community_chest": "Pouches",
            },
        ),
        (
            "marvel_eternals",
            {
                "chance_1": "Uni-Mind",
                "chance_2": "Uni-Mind",
                "chance_3": "Uni-Mind",
                "community_chest_1": "Arishem's Judgement",
                "community_chest_2": "Arishem's Judgement",
                "community_chest_3": "Arishem's Judgement",
            },
            {
                "chance": "Uni-Mind",
                "community_chest": "Arishem's Judgement",
            },
        ),
        (
            "marvel_falcon_winter_soldier",
            {
                "chance_1": "The Shield",
                "chance_2": "The Shield",
                "chance_3": "The Shield",
                "community_chest_1": "The Flag Smashers",
                "community_chest_2": "The Flag Smashers",
                "community_chest_3": "The Flag Smashers",
            },
            {
                "chance": "The Shield",
                "community_chest": "The Flag Smashers",
            },
        ),
        (
            "marvel_spider_man",
            {
                "chance_1": "Daily Bugle",
                "chance_2": "Daily Bugle",
                "chance_3": "Daily Bugle",
                "community_chest_1": "Spider-Sense",
                "community_chest_2": "Spider-Sense",
                "community_chest_3": "Spider-Sense",
            },
            {
                "chance": "Daily Bugle",
                "community_chest": "Spider-Sense",
            },
        ),
        (
            "marvel_super_villains",
            {
                "chance_1": "Chance",
                "chance_2": "Chance",
                "chance_3": "Chance",
                "community_chest_1": "Reshape the Universe",
                "community_chest_2": "Reshape the Universe",
                "community_chest_3": "Reshape the Universe",
            },
            {
                "chance": "Chance",
                "community_chest": "Reshape the Universe",
            },
        ),
    ],
)
def test_marvel_seed_applies_manual_action_labels_and_deck_metadata(
    board_id: str,
    expected_names: dict[str, str],
    expected_decks: dict[str, str],
) -> None:
    rule_set = load_manual_rule_set(board_id)
    by_space_id = {
        row["space_id"]: row["name"]
        for row in rule_set.board.get("spaces", [])
    }
    for space_id, expected_name in expected_names.items():
        assert by_space_id.get(space_id) == expected_name

    assert rule_set.mechanics.get("decks") == expected_decks


@pytest.mark.parametrize(
    ("board_id", "expected_names", "expected_decks"),
    [
        (
            "disney_animation",
            {
                "chance_1": "Magic Mirror",
                "chance_2": "Magic Mirror",
                "chance_3": "Magic Mirror",
                "community_chest_1": "Ariel's Treasure Chest",
                "community_chest_2": "Ariel's Treasure Chest",
                "community_chest_3": "Ariel's Treasure Chest",
                "income_tax": "The Evil Queen's Spell",
                "luxury_tax": "Maleficent's Curse",
            },
            {
                "chance": "Magic Mirror",
                "community_chest": "Ariel's Treasure Chest",
            },
        ),
        (
            "disney_legacy",
            {
                "chance_1": "Show Time",
                "chance_2": "Show Time",
                "chance_3": "Show Time",
                "community_chest_1": "Magic Moments",
                "community_chest_2": "Magic Moments",
                "community_chest_3": "Magic Moments",
            },
            {
                "chance": "Show Time",
                "community_chest": "Magic Moments",
            },
        ),
        (
            "disney_lightyear",
            {
                "chance_1": "Hyperspeed",
                "chance_2": "Hyperspeed",
                "chance_3": "Hyperspeed",
                "community_chest_1": "Crystallic Fusion",
                "community_chest_2": "Crystallic Fusion",
                "community_chest_3": "Crystallic Fusion",
                "income_tax": "Bugs",
                "luxury_tax": "Zyclops",
            },
            {
                "chance": "Hyperspeed",
                "community_chest": "Crystallic Fusion",
            },
        ),
        (
            "disney_lion_king",
            {
                "chance_1": "Destiny",
                "chance_2": "Destiny",
                "chance_3": "Destiny",
                "community_chest_1": "Destiny",
                "community_chest_2": "Destiny",
                "community_chest_3": "Destiny",
                "income_tax": "Water Fowl",
                "luxury_tax": "Wild Fire",
            },
            {
                "chance": "Destiny",
                "community_chest": "Destiny",
            },
        ),
        (
            "disney_mickey_friends",
            {
                "chance_1": "Friendship",
                "chance_2": "Friendship",
                "chance_3": "Friendship",
                "community_chest_1": "Magic Moments",
                "community_chest_2": "Magic Moments",
                "community_chest_3": "Magic Moments",
                "income_tax": "Hot Dog Snack Break",
                "luxury_tax": "Popcorn Snack Break",
            },
            {
                "chance": "Friendship",
                "community_chest": "Magic Moments",
            },
        ),
        (
            "disney_princesses",
            {
                "chance_1": "Sorte",
                "chance_2": "Sorte",
                "chance_3": "Sorte",
                "community_chest_1": "Magia",
                "community_chest_2": "Magia",
                "community_chest_3": "Magia",
                "income_tax": "Imposto",
                "luxury_tax": "Imposto",
            },
            {
                "chance": "Sorte",
                "community_chest": "Magia",
            },
        ),
        (
            "disney_star_wars_dark_side",
            {
                "chance_1": "The Empire",
                "chance_2": "The Empire",
                "chance_3": "The Empire",
                "community_chest_1": "The Dark Side",
                "community_chest_2": "The Dark Side",
                "community_chest_3": "The Dark Side",
                "income_tax": "Rebel Escape",
                "luxury_tax": "Rebel Attack",
            },
            {
                "chance": "The Empire",
                "community_chest": "The Dark Side",
            },
        ),
        (
            "disney_villains",
            {
                "chance_1": "Chance",
                "chance_2": "Chance",
                "chance_3": "Chance",
                "community_chest_1": "Poison Apple",
                "community_chest_2": "Poison Apple",
                "community_chest_3": "Poison Apple",
            },
            {
                "chance": "Chance",
                "community_chest": "Poison Apple",
            },
        ),
    ],
)
def test_disney_seed_applies_manual_action_labels_and_deck_metadata(
    board_id: str,
    expected_names: dict[str, str],
    expected_decks: dict[str, str],
) -> None:
    rule_set = load_manual_rule_set(board_id)
    by_space_id = {
        row["space_id"]: row["name"]
        for row in rule_set.board.get("spaces", [])
    }
    for space_id, expected_name in expected_names.items():
        assert by_space_id.get(space_id) == expected_name

    assert rule_set.mechanics.get("decks") == expected_decks


@pytest.mark.parametrize(
    ("board_id", "expected_names", "expected_decks"),
    [
        (
            "mario_celebration",
            {
                "chance_1": "Question Block",
                "chance_2": "Question Block",
                "chance_3": "Question Block",
                "community_chest_1": "Community Chest",
                "community_chest_2": "Community Chest",
                "community_chest_3": "Community Chest",
                "income_tax": "Chain Chomp",
                "luxury_tax": "Piranha Plant",
            },
            {
                "chance": "Question Block",
                "community_chest": "Community Chest",
            },
        ),
        (
            "mario_collectors",
            {
                "chance_1": "? Block",
                "chance_2": "? Block",
                "chance_3": "? Block",
                "community_chest_1": "Warp Pipe",
                "community_chest_2": "Warp Pipe",
                "community_chest_3": "Warp Pipe",
            },
            {
                "chance": "? Block",
                "community_chest": "Warp Pipe",
            },
        ),
        (
            "mario_kart",
            {
                "chance_1": "Power-Up",
                "chance_2": "Power-Up",
                "chance_3": "Power-Up",
                "community_chest_1": "Grand Prix",
                "community_chest_2": "Grand Prix",
                "community_chest_3": "Grand Prix",
            },
            {
                "chance": "Power-Up",
                "community_chest": "Grand Prix",
            },
        ),
        (
            "mario_movie",
            {
                "chance_1": "Question Block",
                "chance_2": "Question Block",
                "chance_3": "Question Block",
                "community_chest_1": "Bowser's Fury",
                "community_chest_2": "Bowser's Fury",
                "community_chest_3": "Bowser's Fury",
            },
            {
                "chance": "Question Block",
                "community_chest": "Bowser's Fury",
            },
        ),
    ],
)
def test_mario_seed_applies_manual_action_labels_and_deck_metadata(
    board_id: str,
    expected_names: dict[str, str],
    expected_decks: dict[str, str],
) -> None:
    rule_set = load_manual_rule_set(board_id)
    by_space_id = {
        row["space_id"]: row["name"]
        for row in rule_set.board.get("spaces", [])
    }
    for space_id, expected_name in expected_names.items():
        assert by_space_id.get(space_id) == expected_name
    assert rule_set.mechanics.get("decks") == expected_decks


def test_remaining_marvel_boards_without_deck_labels_are_known_exceptions() -> None:
    anchor_rows = _load_json(ANCHOR_INDEX_PATH)
    marvel_board_ids = sorted(
        row["board_id"]
        for row in anchor_rows
        if str(row.get("board_id", "")).startswith("marvel_")
    )
    missing_deck_ids: list[str] = []
    for board_id in marvel_board_ids:
        rule_set = load_manual_rule_set(board_id)
        if not isinstance(rule_set.mechanics.get("decks"), dict):
            missing_deck_ids.append(board_id)
    assert missing_deck_ids == ["marvel_avengers_legacy", "marvel_flip"]


def test_remaining_disney_boards_without_deck_labels_are_known_exceptions() -> None:
    anchor_rows = _load_json(ANCHOR_INDEX_PATH)
    disney_board_ids = sorted(
        row["board_id"]
        for row in anchor_rows
        if str(row.get("board_id", "")).startswith("disney_")
    )
    missing_deck_ids: list[str] = []
    for board_id in disney_board_ids:
        rule_set = load_manual_rule_set(board_id)
        if not isinstance(rule_set.mechanics.get("decks"), dict):
            missing_deck_ids.append(board_id)
    assert missing_deck_ids == ["disney_the_edition"]


def test_all_mario_boards_have_seeded_deck_labels() -> None:
    anchor_rows = _load_json(ANCHOR_INDEX_PATH)
    mario_board_ids = sorted(
        row["board_id"]
        for row in anchor_rows
        if str(row.get("board_id", "")).startswith("mario_")
    )
    missing_deck_ids: list[str] = []
    for board_id in mario_board_ids:
        rule_set = load_manual_rule_set(board_id)
        if not isinstance(rule_set.mechanics.get("decks"), dict):
            missing_deck_ids.append(board_id)
    assert missing_deck_ids == []
