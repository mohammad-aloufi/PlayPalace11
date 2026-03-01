"""Integration tests for Wave 3 Monopoly board startup behavior."""

import pytest

from server.games.monopoly.game import MonopolyGame, MonopolyOptions
from server.core.users.test_user import MockUser

WAVE3_BOARD_IDS = [
    "disney_star_wars_dark_side",
    "disney_legacy",
    "disney_the_edition",
    "lord_of_the_rings_trilogy",
    "star_wars_saga",
    "marvel_avengers_legacy",
    "star_wars_legacy",
    "star_wars_classic_edition",
    "star_wars_solo",
    "game_of_thrones",
    "deadpool_collectors",
    "toy_story",
    "black_panther",
    "stranger_things_collectors",
    "ghostbusters",
    "marvel_eternals",
    "transformers",
    "stranger_things_netflix",
    "fortnite_collectors",
    "star_wars_mandalorian_s2",
    "transformers_beast_wars",
    "marvel_falcon_winter_soldier",
    "fortnite_flip",
    "marvel_flip",
    "pokemon",
]


def _start_two_player_game(options: MonopolyOptions) -> MonopolyGame:
    game = MonopolyGame(options=options)
    game.add_player("Host", MockUser("Host"))
    game.add_player("Guest", MockUser("Guest"))
    game.host = "Host"
    game.on_start()
    return game


@pytest.mark.parametrize("board_id", WAVE3_BOARD_IDS)
def test_wave3_board_starts_in_auto_board_rules(board_id: str):
    game = _start_two_player_game(
        MonopolyOptions(
            preset_id="classic_standard",
            board_id=board_id,
            board_rules_mode="auto",
        )
    )
    assert game.active_board_id == board_id
    assert game.active_board_effective_mode == "board_rules"


def test_wave3_board_autofixes_incompatible_preset():
    game = _start_two_player_game(
        MonopolyOptions(
            preset_id="city",
            board_id="disney_star_wars_dark_side",
            board_rules_mode="auto",
        )
    )
    assert game.active_board_id == "disney_star_wars_dark_side"
    assert game.active_preset_id == "classic_standard"
    assert game.active_board_effective_mode == "board_rules"
