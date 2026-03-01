"""Wave special-card behavior tests for long-tail board promotions."""

from server.games.monopoly.board_parity import get_board_parity_profile
from server.games.monopoly.game import MonopolyGame, MonopolyOptions
from server.core.users.test_user import MockUser


def _start_board(board_id: str) -> MonopolyGame:
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


def test_harry_potter_board_rules_uses_board_specific_card_content(monkeypatch):
    game = _start_board("harry_potter")
    host = game.current_player
    assert host is not None

    host.position = 5
    monkeypatch.setattr(game, "_draw_card", lambda deck_type: "go_back_three")
    rolls = iter([1, 1])
    monkeypatch.setattr("server.games.monopoly.game.random.randint", lambda a, b: next(rolls))

    game.execute_action(host, "roll_dice")

    assert host.position == 7
    assert host.cash == 1570


def test_fortnite_board_rules_uses_board_specific_card_content(monkeypatch):
    game = _start_board("fortnite")
    host = game.current_player
    assert host is not None

    host.position = 0
    monkeypatch.setattr(game, "_draw_card", lambda deck_type: "doctor_fee_pay_50")
    rolls = iter([1, 1])
    monkeypatch.setattr("server.games.monopoly.game.random.randint", lambda a, b: next(rolls))

    game.execute_action(host, "roll_dice")

    assert host.position == 2
    assert host.cash == 1565


def test_stranger_things_board_rules_uses_board_specific_card_content(monkeypatch):
    game = _start_board("stranger_things")
    host = game.current_player
    assert host is not None

    host.position = 5
    monkeypatch.setattr(game, "_draw_card", lambda deck_type: "bank_dividend_50")
    rolls = iter([1, 1])
    monkeypatch.setattr("server.games.monopoly.game.random.randint", lambda a, b: next(rolls))

    game.execute_action(host, "roll_dice")

    assert host.position == 10
    assert host.in_jail is True


def test_long_tail_special_boards_have_board_specific_deck_mode():
    board_ids = ["harry_potter", "fortnite", "stranger_things"]

    for board_id in board_ids:
        profile = get_board_parity_profile(board_id)
        assert profile is not None
        assert profile.deck_mode == "board_specific"
        assert any(
            capability_id in {"card_id_remap", "card_cash_override"}
            for capability_id in profile.capability_ids
        )
