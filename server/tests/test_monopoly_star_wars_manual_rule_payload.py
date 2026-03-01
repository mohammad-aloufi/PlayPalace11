"""Coverage for Star Wars-family manual rule payloads."""

from __future__ import annotations

import pytest

from server.games.monopoly.game import (
    CHANCE_CARD_IDS,
    COMMUNITY_CHEST_CARD_IDS,
    MonopolyGame,
    MonopolyOptions,
)
from server.games.monopoly.manual_rules.loader import load_manual_rule_set
from server.core.users.test_user import MockUser


STAR_WARS_FAMILY_BOARD_IDS = [
    "disney_star_wars_dark_side",
    "star_wars_40th",
    "star_wars_boba_fett",
    "star_wars_classic_edition",
    "star_wars_complete_saga",
    "star_wars_legacy",
    "star_wars_light_side",
    "star_wars_mandalorian",
    "star_wars_mandalorian_s2",
    "star_wars_saga",
    "star_wars_solo",
    "star_wars_the_child",
]


def _start_game(board_id: str) -> MonopolyGame:
    game = MonopolyGame(
        options=MonopolyOptions(
            preset_id="classic_standard",
            board_id=board_id,
            board_rules_mode="auto",
        )
    )
    game.add_player("Host", MockUser("Host"))
    game.add_player("Guest", MockUser("Guest"))
    game.host = "Host"
    game.on_start()
    return game


@pytest.mark.parametrize("board_id", STAR_WARS_FAMILY_BOARD_IDS)
def test_star_wars_manual_rule_payload_has_full_card_and_space_baseline(board_id: str):
    rule_set = load_manual_rule_set(board_id)

    spaces = rule_set.board.get("spaces", [])
    chance_rows = rule_set.cards.get("chance", [])
    community_rows = rule_set.cards.get("community_chest", [])

    assert len(spaces) == 40
    assert [row["id"] for row in chance_rows] == CHANCE_CARD_IDS
    assert [row["id"] for row in community_rows] == COMMUNITY_CHEST_CARD_IDS


@pytest.mark.parametrize(
    ("board_id", "card_id", "expected_amount"),
    [
        ("disney_star_wars_dark_side", "bank_dividend_50", 95),
        ("star_wars_classic_edition", "bank_dividend_50", 75),
        ("star_wars_complete_saga", "income_tax_refund_20", 80),
        ("star_wars_legacy", "income_tax_refund_20", 65),
        ("star_wars_mandalorian_s2", "bank_dividend_50", 85),
        ("star_wars_saga", "bank_error_collect_200", 205),
    ],
)
def test_star_wars_manual_rule_payload_encodes_card_amount_overrides(
    board_id: str,
    card_id: str,
    expected_amount: int,
):
    rule_set = load_manual_rule_set(board_id)
    rows = rule_set.cards.get("chance", []) + rule_set.cards.get("community_chest", [])
    row = next(row for row in rows if row.get("id") == card_id)
    effect = row.get("effect", {})

    assert effect.get("amount") == expected_amount


def test_star_wars_manual_rule_payload_executes_manual_effect_for_remapped_card(monkeypatch):
    game = _start_game("star_wars_40th")
    host = game.current_player
    assert host is not None

    host.position = 5
    monkeypatch.setattr(game, "_draw_card", lambda deck_type: "bank_dividend_50")
    rolls = iter([1, 1])
    monkeypatch.setattr("server.games.monopoly.game.random.randint", lambda a, b: next(rolls))

    original = game._apply_manual_card_effect
    seen_effect_types: list[str] = []

    def _wrapped_apply(player, effect_spec, *, depth, dice_total):
        effect_type = effect_spec.get("type")
        if isinstance(effect_type, str):
            seen_effect_types.append(effect_type)
        return original(player, effect_spec, depth=depth, dice_total=dice_total)

    monkeypatch.setattr(game, "_apply_manual_card_effect", _wrapped_apply)

    game.execute_action(host, "roll_dice")

    assert "move_absolute" in seen_effect_types
    assert host.position == 0
    assert host.cash == 1700


@pytest.mark.parametrize("board_id", STAR_WARS_FAMILY_BOARD_IDS)
@pytest.mark.parametrize(
    ("deck_type", "card_id", "expected_substring"),
    [
        ("chance", "advance_to_go", "GO"),
        ("chance", "go_to_jail", "In Jail"),
        ("community_chest", "go_to_jail", "In Jail"),
        ("community_chest", "get_out_of_jail_free", "Get Out of Jail Free"),
    ],
)
def test_star_wars_manual_rule_payload_includes_literal_card_text(
    board_id: str,
    deck_type: str,
    card_id: str,
    expected_substring: str,
) -> None:
    rule_set = load_manual_rule_set(board_id)
    deck_rows = rule_set.cards.get(deck_type, [])
    row = next(row for row in deck_rows if row.get("id") == card_id)
    literal_text = row.get("text")
    assert isinstance(literal_text, str)
    assert expected_substring in literal_text
