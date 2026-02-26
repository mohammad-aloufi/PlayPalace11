"""Tests for manual rule citation validation."""

from server.games.monopoly.manual_rules.models import ManualRuleSet
from server.games.monopoly.manual_rules.validator import validate_manual_rule_set


def _base_payload() -> dict[str, object]:
    return {
        "board_id": "mario_kart",
        "anchor_edition_id": "monopoly-e1870",
        "board": {"spaces": []},
        "economy": {"properties": {}},
        "cards": {"chance": [], "community_chest": []},
        "mechanics": {},
        "win_condition": {"type": "bankruptcy"},
    }


def test_validator_rejects_missing_rule_path_citation():
    payload = _base_payload()
    payload["citations"] = [
        {
            "rule_path": "board.spaces",
            "edition_id": "monopoly-e1870",
            "page_ref": "p.2",
            "confidence": "high",
        }
    ]

    rule_set = ManualRuleSet.from_dict(payload)
    errors = validate_manual_rule_set(rule_set)

    assert "missing citation for economy.properties" in errors


def test_validator_accepts_complete_required_citations():
    payload = _base_payload()
    payload["citations"] = [
        {
            "rule_path": "board.spaces",
            "edition_id": "monopoly-e1870",
            "page_ref": "p.2",
            "confidence": "high",
        },
        {
            "rule_path": "economy.properties",
            "edition_id": "monopoly-e1870",
            "page_ref": "p.4",
            "confidence": "high",
        },
        {
            "rule_path": "cards.chance",
            "edition_id": "monopoly-e1870",
            "page_ref": "p.7",
            "confidence": "high",
        },
        {
            "rule_path": "cards.community_chest",
            "edition_id": "monopoly-e1870",
            "page_ref": "p.8",
            "confidence": "high",
        },
        {
            "rule_path": "win_condition",
            "edition_id": "monopoly-e1870",
            "page_ref": "p.11",
            "confidence": "high",
        },
    ]

    rule_set = ManualRuleSet.from_dict(payload)

    assert validate_manual_rule_set(rule_set) == []
