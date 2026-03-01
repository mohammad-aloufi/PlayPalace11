"""Tests for manual-rule-driven board space resolution."""

from server.games.monopoly.game import MonopolyGame, MonopolyOptions
from server.games.monopoly.manual_rules.models import ManualRuleSet
from server.core.users.test_user import MockUser


def _manual_rules_with_spaces(board_id: str) -> ManualRuleSet:
    return ManualRuleSet.from_dict(
        {
            "board_id": board_id,
            "anchor_edition_id": "monopoly-e1870",
            "board": {
                "spaces": [
                    {"position": 0, "space_id": "mk_go", "name": "GO", "kind": "start"},
                    {
                        "position": 1,
                        "space_id": "mario_kart_space_1",
                        "name": "Mushroom Cup",
                        "kind": "property",
                        "price": 120,
                        "rent": 8,
                        "color_group": "brown",
                        "house_cost": 50,
                        "rents": [8, 40, 120, 320, 450, 600],
                    },
                    {
                        "position": 2,
                        "space_id": "mk_chance",
                        "name": "Question Block",
                        "kind": "chance",
                    },
                ]
            },
            "economy": {"properties": {}},
            "cards": {"chance": [], "community_chest": []},
            "mechanics": {},
            "win_condition": {"type": "bankruptcy"},
            "citations": [
                {
                    "rule_path": "board.spaces",
                    "edition_id": "monopoly-e1870",
                    "page_ref": "p.2",
                    "confidence": "high",
                }
            ],
        }
    )


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


def test_manual_rule_space_lookup_uses_board_specific_space_ids(monkeypatch):
    monkeypatch.setattr(
        "server.games.monopoly.game.load_manual_rule_set",
        lambda board_id: _manual_rules_with_spaces(board_id),
    )

    game = _start_game("mario_kart")

    assert game.active_board_size == 3
    assert game._space_at(1).space_id == "mario_kart_space_1"
    assert game._space_label("mario_kart_space_1") == "Mushroom Cup"
