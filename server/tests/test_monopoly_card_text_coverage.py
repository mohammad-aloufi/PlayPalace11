"""Tests for card text and cash-override evidence coverage across all Monopoly boards."""

import importlib
import json
from pathlib import Path

import pytest


DATA_DIR = Path(__file__).resolve().parent.parent / "games" / "monopoly" / "manual_rules" / "data"
BOARD_RULES_DIR = Path(__file__).resolve().parent.parent / "games" / "monopoly" / "board_rules"

# Universal card IDs that every board should have text on.
UNIVERSAL_CARD_TEXT_IDS = {
    ("chance", "advance_to_go"),
    ("chance", "go_to_jail"),
    ("community_chest", "go_to_jail"),
    ("community_chest", "get_out_of_jail_free"),
}

# All special board IDs (every JSON file in the data directory).
ALL_BOARD_IDS = sorted(p.stem for p in DATA_DIR.glob("*.json"))


def _load_raw_json(board_id: str) -> dict:
    path = DATA_DIR / f"{board_id}.json"
    return json.loads(path.read_text(encoding="utf-8"))


def _find_card(cards_section: dict, deck: str, card_id: str) -> dict | None:
    """Find a card by id or legacy_id within a deck."""
    for card in cards_section.get(deck, []):
        if card.get("id") == card_id or card.get("legacy_id") == card_id:
            return card
    return None


def _get_card_cash_overrides(board_id: str) -> dict:
    """Load CARD_CASH_OVERRIDES from a board_rules module, if it exists."""
    module_path = BOARD_RULES_DIR / f"{board_id}.py"
    if not module_path.exists():
        return {}
    spec = importlib.util.spec_from_file_location(
        f"board_rules_{board_id}", module_path
    )
    if spec is None or spec.loader is None:
        return {}
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    except Exception:
        return {}
    overrides = getattr(mod, "CARD_CASH_OVERRIDES", None)
    return overrides if isinstance(overrides, dict) else {}


# ── Part A: every special board has universal card text ──────────────


@pytest.mark.parametrize("board_id", ALL_BOARD_IDS)
def test_all_boards_have_universal_card_text(board_id: str) -> None:
    data = _load_raw_json(board_id)
    cards = data.get("cards", {})

    for deck, card_id in UNIVERSAL_CARD_TEXT_IDS:
        card = _find_card(cards, deck, card_id)
        assert card is not None, (
            f"{board_id}: missing card {deck}/{card_id}"
        )
        assert "text" in card and card["text"], (
            f"{board_id}: card {deck}/{card_id} has no 'text' field"
        )


# ── Part B: boards with cash overrides have evidence text_note ───────


@pytest.mark.parametrize("board_id", ALL_BOARD_IDS)
def test_cash_override_boards_have_evidence_notes(board_id: str) -> None:
    overrides = _get_card_cash_overrides(board_id)
    if not overrides:
        pytest.skip(f"{board_id} has no CARD_CASH_OVERRIDES")

    data = _load_raw_json(board_id)
    cards = data.get("cards", {})

    for card_id in overrides:
        # Card lives in either chance or community_chest deck.
        card = _find_card(cards, "chance", card_id) or _find_card(
            cards, "community_chest", card_id
        )
        assert card is not None, (
            f"{board_id}: overridden card {card_id} not found in JSON"
        )
        assert "text_note" in card and card["text_note"], (
            f"{board_id}: overridden card {card_id} missing 'text_note' evidence"
        )
