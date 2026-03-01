"""Tests for manual card effect execution in Monopoly runtime."""

from server.games.monopoly.game import MonopolyGame, MonopolyOptions
from server.games.monopoly.manual_rules.models import ManualRuleSet
from server.core.users.test_user import MockUser


def _manual_rules_with_credit_card(board_id: str) -> ManualRuleSet:
    return ManualRuleSet.from_dict(
        {
            "board_id": board_id,
            "anchor_edition_id": "monopoly-e1870",
            "board": {
                "spaces": [
                    {"position": 0, "space_id": "mk_go", "name": "GO", "kind": "start"},
                    {
                        "position": 1,
                        "space_id": "mk_property",
                        "name": "Mushroom Cup",
                        "kind": "property",
                        "price": 100,
                        "rent": 10,
                        "color_group": "brown",
                        "house_cost": 50,
                        "rents": [10, 50, 150, 450, 625, 750],
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
            "cards": {
                "chance": [
                    {
                        "id": "mk_collect_100",
                        "text_key": "monopoly-card-bank-dividend-50",
                        "effect": {"type": "credit", "amount": 100},
                    }
                ],
                "community_chest": [],
            },
            "mechanics": {},
            "win_condition": {"type": "bankruptcy"},
            "citations": [
                {
                    "rule_path": "cards.chance",
                    "edition_id": "monopoly-e1870",
                    "page_ref": "p.7",
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


def test_manual_rule_card_effect_spec_applies_credit(monkeypatch):
    monkeypatch.setattr(
        "server.games.monopoly.game.load_manual_rule_set",
        lambda board_id: _manual_rules_with_credit_card(board_id),
    )
    game = _start_game("mario_kart")
    host = game.current_player
    assert host is not None

    host.position = 0
    monkeypatch.setattr(game, "_draw_card", lambda deck_type: "mk_collect_100")
    rolls = iter([1, 1])
    monkeypatch.setattr("server.games.monopoly.game.random.randint", lambda a, b: next(rolls))

    game.execute_action(host, "roll_dice")

    assert host.cash == 1600
