"""Tests for manual-rule deck initialization and fallback behavior."""

from server.games.monopoly.game import CHANCE_CARD_IDS, MonopolyGame, MonopolyOptions
from server.games.monopoly.manual_rules.models import ManualRuleSet
from server.core.users.test_user import MockUser


def _manual_rules_with_decks(board_id: str) -> ManualRuleSet:
    return ManualRuleSet.from_dict(
        {
            "board_id": board_id,
            "anchor_edition_id": "monopoly-e1870",
            "board": {"spaces": [{"position": 0, "space_id": "go", "name": "GO", "kind": "start"}]},
            "economy": {"properties": {}},
            "cards": {
                "chance": [{"id": "mk_card_1"}, {"id": "mk_card_2"}],
                "community_chest": [{"id": "mk_cc_1"}],
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


def _manual_rules_with_native_decks(board_id: str) -> ManualRuleSet:
    chance_rows = [
        {
            "id": "event_advance_to_go",
            "legacy_id": "advance_to_go",
            "effect": {"type": "move_absolute", "position": 0, "collect_pass_go": True},
        },
        {
            "id": "event_bank_dividend_50",
            "legacy_id": "bank_dividend_50",
            "effect": {"type": "credit", "amount": 50},
        },
        {
            "id": "event_go_back_three",
            "legacy_id": "go_back_three",
            "effect": {"type": "move_relative", "steps": -3, "collect_pass_go": False},
        },
        {
            "id": "event_go_to_jail",
            "legacy_id": "go_to_jail",
            "effect": {"type": "go_to_jail"},
        },
        {
            "id": "event_poor_tax_15",
            "legacy_id": "poor_tax_15",
            "effect": {"type": "debit", "amount": 15},
        },
    ]
    chest_rows = [
        {
            "id": "team_up_bank_error_collect_200",
            "legacy_id": "bank_error_collect_200",
            "effect": {"type": "credit", "amount": 200},
        },
        {
            "id": "team_up_doctor_fee_pay_50",
            "legacy_id": "doctor_fee_pay_50",
            "effect": {"type": "debit", "amount": 50},
        },
        {
            "id": "team_up_income_tax_refund_20",
            "legacy_id": "income_tax_refund_20",
            "effect": {"type": "credit", "amount": 20},
        },
        {
            "id": "team_up_go_to_jail",
            "legacy_id": "go_to_jail",
            "effect": {"type": "go_to_jail"},
        },
        {
            "id": "team_up_get_out_of_jail_free",
            "legacy_id": "get_out_of_jail_free",
            "effect": {"type": "no_effect"},
        },
    ]
    return ManualRuleSet.from_dict(
        {
            "board_id": board_id,
            "anchor_edition_id": "monopoly-e1870",
            "board": {"spaces": [{"position": 0, "space_id": "go", "name": "GO", "kind": "start"}]},
            "economy": {"properties": {}},
            "cards": {
                "chance": chance_rows,
                "community_chest": chest_rows,
            },
            "mechanics": {"decks": {"chance": "Event", "community_chest": "Team-Up"}},
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


def test_manual_rule_decks_replace_classic_deck_ids(monkeypatch):
    monkeypatch.setattr(
        "server.games.monopoly.game.load_manual_rule_set",
        lambda board_id: _manual_rules_with_decks(board_id),
    )

    game = _start_game("mario_kart")

    assert game.chance_deck_order == ["mk_card_1", "mk_card_2"]
    assert game.community_chest_deck_order == ["mk_cc_1"]


def test_missing_manual_rule_decks_fall_back_to_classic_ids():
    game = _start_game("mario_kart")

    assert sorted(game.chance_deck_order) == sorted(CHANCE_CARD_IDS)


def test_native_manual_deck_ids_still_resolve_legacy_compatibility_card_ids(monkeypatch):
    monkeypatch.setattr(
        "server.games.monopoly.game.load_manual_rule_set",
        lambda board_id: _manual_rules_with_native_decks(board_id),
    )

    game = _start_game("mario_movie")
    host = game.current_player
    assert host is not None

    host.position = 3
    resolved_card_id = game._resolve_board_card_id("chance", "advance_to_go")
    assert resolved_card_id == "event_advance_to_go"

    result = game._resolve_card_effect(host, "chance", "advance_to_go", depth=0, dice_total=2)
    assert result == "resolved"
    assert host.position == 0
    assert host.cash == 1700
