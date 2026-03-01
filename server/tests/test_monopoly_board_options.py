"""Tests for Monopoly board-related lobby options."""

from server.games.monopoly.game import MonopolyGame
from server.core.users.test_user import MockUser


def test_monopoly_options_include_board_and_mode_selectors():
    game = MonopolyGame()
    host_user = MockUser("Host")
    game.add_player("Host", host_user)
    game.host = "Host"
    host_player = game.players[0]

    options_action_set = game.get_action_set(host_player, "options")
    assert options_action_set is not None
    assert options_action_set.get_action("set_board_id") is not None
    assert options_action_set.get_action("set_board_rules_mode") is not None
