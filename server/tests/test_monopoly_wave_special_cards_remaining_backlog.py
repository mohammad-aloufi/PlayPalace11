"""Wave tests for remaining special-board card parity promotions."""

import pytest

from server.games.monopoly.board_parity import get_board_parity_profile
from server.games.monopoly.game import MonopolyGame, MonopolyOptions
from server.core.users.test_user import MockUser


REMAINING_SPECIAL_BOARD_IDS = [
    "animal_crossing",
    "barbie",
    "black_panther",
    "deadpool_collectors",
    "fortnite_collectors",
    "fortnite_flip",
    "game_of_thrones",
    "ghostbusters",
    "jurassic_park",
    "lord_of_the_rings",
    "lord_of_the_rings_trilogy",
    "pokemon",
    "stranger_things_collectors",
    "stranger_things_netflix",
    "toy_story",
    "transformers",
    "transformers_beast_wars",
]

REMAINING_SPECIAL_CASES = [
    ("animal_crossing", 5, "poor_tax_15", 7, 1586, False),
    ("barbie", 5, "bank_dividend_50", 10, 1500, True),
    ("black_panther", 0, "doctor_fee_pay_50", 2, 1572, False),
    ("deadpool_collectors", 5, "go_back_three", 0, 1700, False),
    ("fortnite_collectors", 0, "doctor_fee_pay_50", 2, 1568, False),
    ("fortnite_flip", 5, "bank_dividend_50", 10, 1500, True),
    ("game_of_thrones", 0, "doctor_fee_pay_50", 2, 1708, False),
    ("ghostbusters", 5, "poor_tax_15", 7, 1582, False),
    ("jurassic_park", 5, "bank_dividend_50", 4, 1300, False),
    ("lord_of_the_rings", 5, "go_back_three", 0, 1700, False),
    ("lord_of_the_rings_trilogy", 0, "doctor_fee_pay_50", 2, 1574, False),
    ("pokemon", 5, "bank_dividend_50", 0, 1700, False),
    ("stranger_things_collectors", 5, "bank_dividend_50", 10, 1500, True),
    ("stranger_things_netflix", 5, "poor_tax_15", 7, 1584, False),
    ("toy_story", 5, "bank_dividend_50", 4, 1300, False),
    ("transformers", 0, "doctor_fee_pay_50", 2, 1712, False),
    ("transformers_beast_wars", 5, "go_back_three", 0, 1700, False),
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
    REMAINING_SPECIAL_CASES,
)
def test_remaining_special_boards_use_board_specific_card_content(
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


def test_remaining_special_skin_only_keeps_classic_card_content(monkeypatch):
    game = _start_board("barbie", board_rules_mode="skin_only")
    host = game.current_player
    assert host is not None

    host.position = 5
    monkeypatch.setattr(game, "_draw_card", lambda deck_type: "bank_dividend_50")
    rolls = iter([1, 1])
    monkeypatch.setattr("server.games.monopoly.game.random.randint", lambda a, b: next(rolls))

    game.execute_action(host, "roll_dice")

    assert host.position == 7
    assert host.cash == 1550
    assert host.in_jail is False


def test_remaining_special_profiles_use_board_specific_deck_mode():
    for board_id in REMAINING_SPECIAL_BOARD_IDS:
        profile = get_board_parity_profile(board_id)
        assert profile is not None
        assert profile.deck_mode == "board_specific"
        assert any(
            capability_id in {"card_id_remap", "card_cash_override"}
            for capability_id in profile.capability_ids
        )
