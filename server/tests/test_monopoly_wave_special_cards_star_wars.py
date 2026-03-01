"""Wave special-card behavior tests for first Star Wars board promotions."""

from server.games.monopoly.board_parity import get_board_parity_profile
from server.games.monopoly.game import MonopolyGame, MonopolyOptions
from server.core.users.test_user import MockUser


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


def test_star_wars_mandalorian_board_rules_remaps_card_effect(monkeypatch):
    game = _start_board("star_wars_mandalorian")
    host = game.current_player
    assert host is not None

    host.position = 5
    monkeypatch.setattr(game, "_draw_card", lambda deck_type: "bank_dividend_50")
    rolls = iter([1, 1])
    monkeypatch.setattr("server.games.monopoly.game.random.randint", lambda a, b: next(rolls))

    game.execute_action(host, "roll_dice")

    assert host.position == 4
    assert host.cash == 1300


def test_star_wars_mandalorian_skin_only_keeps_classic_card_effect(monkeypatch):
    game = _start_board("star_wars_mandalorian", board_rules_mode="skin_only")
    host = game.current_player
    assert host is not None

    host.position = 5
    monkeypatch.setattr(game, "_draw_card", lambda deck_type: "bank_dividend_50")
    rolls = iter([1, 1])
    monkeypatch.setattr("server.games.monopoly.game.random.randint", lambda a, b: next(rolls))

    game.execute_action(host, "roll_dice")

    assert host.position == 7
    assert host.cash == 1550


def test_star_wars_complete_saga_board_rules_applies_card_cash_override(monkeypatch):
    game = _start_board("star_wars_complete_saga")
    host = game.current_player
    assert host is not None

    host.position = 0
    monkeypatch.setattr(game, "_draw_card", lambda deck_type: "bank_error_collect_200")
    rolls = iter([1, 1])
    monkeypatch.setattr("server.games.monopoly.game.random.randint", lambda a, b: next(rolls))

    game.execute_action(host, "roll_dice")

    assert host.position == 2
    assert host.cash == 1580


def test_star_wars_wave_profiles_use_board_specific_deck_mode():
    mandalorian = get_board_parity_profile("star_wars_mandalorian")
    complete_saga = get_board_parity_profile("star_wars_complete_saga")

    assert mandalorian is not None
    assert complete_saga is not None
    assert mandalorian.deck_mode == "board_specific"
    assert complete_saga.deck_mode == "board_specific"
