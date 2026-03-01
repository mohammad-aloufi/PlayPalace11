"""Expanded Star Wars-family special card behavior tests."""

import pytest

from server.games.monopoly.board_parity import get_board_parity_profile
from server.games.monopoly.game import MonopolyGame, MonopolyOptions
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

STAR_WARS_EXPANDED_CASES = [
    ("disney_star_wars_dark_side", 5, "poor_tax_15", 7, 1595, False),
    ("star_wars_40th", 5, "bank_dividend_50", 0, 1700, False),
    ("star_wars_boba_fett", 5, "bank_dividend_50", 4, 1300, False),
    ("star_wars_classic_edition", 5, "go_back_three", 7, 1575, False),
    ("star_wars_legacy", 0, "doctor_fee_pay_50", 2, 1565, False),
    ("star_wars_light_side", 5, "bank_dividend_50", 10, 1500, True),
    ("star_wars_mandalorian_s2", 5, "poor_tax_15", 7, 1585, False),
    ("star_wars_saga", 0, "doctor_fee_pay_50", 2, 1705, False),
    ("star_wars_solo", 5, "go_back_three", 0, 1700, False),
    ("star_wars_the_child", 5, "bank_dividend_50", 10, 1500, True),
]


def _start_board(board_id: str, board_rules_mode: str = "auto") -> MonopolyGame:
    game = MonopolyGame(
        options=MonopolyOptions(
            preset_id="classic_standard",
            board_id=board_id,
            board_rules_mode=board_rules_mode,
        )
    )
    game.add_player("Host", MockUser("Host"))
    game.add_player("Guest", MockUser("Guest"))
    game.host = "Host"
    game.on_start()
    return game


@pytest.mark.parametrize(
    ("board_id", "start_position", "drawn_card", "expected_position", "expected_cash", "expected_in_jail"),
    STAR_WARS_EXPANDED_CASES,
)
def test_star_wars_family_board_rules_uses_board_specific_card_content(
    board_id: str,
    start_position: int,
    drawn_card: str,
    expected_position: int,
    expected_cash: int,
    expected_in_jail: bool,
    monkeypatch,
):
    game = _start_board(board_id)
    host = game.current_player
    assert host is not None

    host.position = start_position
    monkeypatch.setattr(game, "_draw_card", lambda deck_type: drawn_card)
    rolls = iter([1, 1])
    monkeypatch.setattr("server.games.monopoly.game.random.randint", lambda a, b: next(rolls))

    game.execute_action(host, "roll_dice")

    assert host.position == expected_position
    assert host.cash == expected_cash
    assert host.in_jail is expected_in_jail


def test_star_wars_family_skin_only_keeps_classic_card_content(monkeypatch):
    game = _start_board("star_wars_40th", board_rules_mode="skin_only")
    host = game.current_player
    assert host is not None

    host.position = 5
    monkeypatch.setattr(game, "_draw_card", lambda deck_type: "bank_dividend_50")
    rolls = iter([1, 1])
    monkeypatch.setattr("server.games.monopoly.game.random.randint", lambda a, b: next(rolls))

    game.execute_action(host, "roll_dice")

    assert host.position == 7
    assert host.cash == 1550


def test_star_wars_family_profiles_use_board_specific_deck_mode():
    for board_id in STAR_WARS_FAMILY_BOARD_IDS:
        profile = get_board_parity_profile(board_id)
        assert profile is not None
        assert profile.deck_mode == "board_specific"
