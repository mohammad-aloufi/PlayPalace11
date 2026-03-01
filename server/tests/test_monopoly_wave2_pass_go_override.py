"""Integration test for Wave 2 pass-GO override capability path."""

from server.games.monopoly.game import MonopolyGame, MonopolyOptions
from server.core.users.test_user import MockUser


def test_wave2_board_pass_go_override_path(monkeypatch):
    game = MonopolyGame(
        options=MonopolyOptions(
            preset_id="classic_standard",
            board_id="disney_princesses",
            board_rules_mode="auto",
        )
    )
    game.add_player("Host", MockUser("Host"))
    game.add_player("Guest", MockUser("Guest"))
    game.host = "Host"
    game.on_start()

    host = game.current_player
    assert host is not None

    monkeypatch.setattr(
        "server.games.monopoly.board_rules.disney_princesses.PASS_GO_CREDIT_OVERRIDE",
        275,
    )
    host.position = 39
    rolls = iter([1, 1])
    monkeypatch.setattr("server.games.monopoly.game.random.randint", lambda a, b: next(rolls))

    game.execute_action(host, "roll_dice")

    assert host.cash == 1775
