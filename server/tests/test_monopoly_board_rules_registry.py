"""Tests for Monopoly board rules registry."""

from server.games.monopoly.board_rules_registry import (
    get_card_cash_override,
    get_card_id_remap,
    get_rule_pack,
    supports_capability,
)


def test_wave1_mario_packs_are_registered():
    assert get_rule_pack("mario_kart") is not None
    assert get_rule_pack("mario_movie") is not None


def test_capability_lookup_handles_missing_pack():
    assert supports_capability("missing", "pass_go_credit") is False


def test_mario_kart_card_id_remap_contract():
    assert get_card_id_remap("mario_kart", "chance", "bank_dividend_50") == "advance_to_go"


def test_card_id_remap_falls_back_to_original_card():
    assert get_card_id_remap("mario_kart", "chance", "does_not_exist") == "does_not_exist"


def test_mario_movie_card_cash_override_contract():
    assert get_card_cash_override("mario_movie", "bank_dividend_50") == 120


def test_card_cash_override_returns_none_when_missing():
    assert get_card_cash_override("mario_movie", "advance_to_go") is None
