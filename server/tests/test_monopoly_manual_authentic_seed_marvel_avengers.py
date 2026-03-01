"""Manual-authentic phase seed coverage for Marvel Avengers board."""

from server.games.monopoly.game import MonopolyGame, MonopolyOptions
from server.games.monopoly.manual_rules.loader import load_manual_rule_set
from server.core.users.test_user import MockUser


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


def test_marvel_avengers_manual_authentic_seed_metadata():
    rule_set = load_manual_rule_set("marvel_avengers")

    mechanics = rule_set.mechanics
    citations = {row.rule_path for row in rule_set.citations}

    assert mechanics.get("mode") == "manual_authentic_phase1"
    assert mechanics.get("decks") == {
        "chance": "Stark Industries",
        "community_chest": "Infinity Gauntlet",
    }
    assert mechanics.get("special_spaces", {}).get("battle_spaces") == "Children of Thanos"
    assert "board.spaces.chance.name" in citations
    assert "board.spaces.community_chest.name" in citations
    assert "board.spaces.tax.name" in citations
    assert "mechanics.decks" in citations


def test_marvel_avengers_manual_authentic_seed_updates_space_labels():
    game = _start_game("marvel_avengers")

    assert game.active_space_by_id["chance_1"].name == "Stark Industries"
    assert game.active_space_by_id["community_chest_1"].name == "Infinity Gauntlet"
    assert game.active_space_by_id["income_tax"].name == "Ultron"
    assert game.active_space_by_id["luxury_tax"].name == "Hela"
