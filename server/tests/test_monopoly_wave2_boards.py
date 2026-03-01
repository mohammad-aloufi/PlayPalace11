"""Integration tests for Wave 2 Monopoly board startup behavior."""

import pytest

from server.games.monopoly.game import MonopolyGame, MonopolyOptions
from server.core.users.test_user import MockUser

WAVE2_BOARD_IDS = [
    "disney_princesses",
    "disney_animation",
    "disney_lion_king",
    "disney_mickey_friends",
    "disney_villains",
    "disney_lightyear",
    "marvel_80_years",
    "marvel_avengers",
    "marvel_spider_man",
    "marvel_black_panther_wf",
    "marvel_super_villains",
    "marvel_deadpool",
    "star_wars_40th",
    "star_wars_boba_fett",
    "star_wars_light_side",
    "star_wars_the_child",
    "star_wars_mandalorian",
    "star_wars_complete_saga",
    "harry_potter",
    "fortnite",
    "stranger_things",
    "jurassic_park",
    "lord_of_the_rings",
    "animal_crossing",
    "barbie",
]


def _start_two_player_game(options: MonopolyOptions) -> MonopolyGame:
    game = MonopolyGame(options=options)
    game.add_player("Host", MockUser("Host"))
    game.add_player("Guest", MockUser("Guest"))
    game.host = "Host"
    game.on_start()
    return game


@pytest.mark.parametrize("board_id", WAVE2_BOARD_IDS)
def test_wave2_board_starts_in_auto_board_rules(board_id: str):
    game = _start_two_player_game(
        MonopolyOptions(
            preset_id="classic_standard",
            board_id=board_id,
            board_rules_mode="auto",
        )
    )
    assert game.active_board_id == board_id
    assert game.active_board_effective_mode == "board_rules"


def test_wave2_board_autofixes_incompatible_preset():
    game = _start_two_player_game(
        MonopolyOptions(
            preset_id="city",
            board_id="disney_princesses",
            board_rules_mode="auto",
        )
    )
    assert game.active_board_id == "disney_princesses"
    assert game.active_preset_id == "classic_standard"
    assert game.active_board_effective_mode == "board_rules"
