"""Wave special-card behavior tests for first Marvel + Disney promotions."""

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


def test_disney_princesses_board_rules_uses_anchor_card_content(monkeypatch):
    game = _start_board("disney_princesses")
    host = game.current_player
    assert host is not None

    host.position = 5
    monkeypatch.setattr(game, "_draw_card", lambda deck_type: "poor_tax_15")
    rolls = iter([1, 1])
    monkeypatch.setattr("server.games.monopoly.game.random.randint", lambda a, b: next(rolls))

    game.execute_action(host, "roll_dice")

    assert host.position == 7
    assert host.cash == 1590


def test_disney_princesses_skin_only_keeps_classic_card_content(monkeypatch):
    game = _start_board("disney_princesses", board_rules_mode="skin_only")
    host = game.current_player
    assert host is not None

    host.position = 5
    monkeypatch.setattr(game, "_draw_card", lambda deck_type: "poor_tax_15")
    rolls = iter([1, 1])
    monkeypatch.setattr("server.games.monopoly.game.random.randint", lambda a, b: next(rolls))

    game.execute_action(host, "roll_dice")

    assert host.position == 7
    assert host.cash == 1485


def test_marvel_avengers_board_rules_uses_anchor_card_content(monkeypatch):
    game = _start_board("marvel_avengers")
    host = game.current_player
    assert host is not None

    host.position = 0
    monkeypatch.setattr(game, "_draw_card", lambda deck_type: "doctor_fee_pay_50")
    rolls = iter([1, 1])
    monkeypatch.setattr("server.games.monopoly.game.random.randint", lambda a, b: next(rolls))

    game.execute_action(host, "roll_dice")

    assert host.position == 2
    assert host.cash == 1720


def test_marvel_disney_wave_profiles_use_board_specific_deck_mode():
    disney = get_board_parity_profile("disney_princesses")
    marvel = get_board_parity_profile("marvel_avengers")

    assert disney is not None
    assert marvel is not None
    assert disney.deck_mode == "board_specific"
    assert marvel.deck_mode == "board_specific"
