"""Tests for Monopoly electronic banking profile resolver."""

from server.games.monopoly.electronic_banking_profile import (
    DEFAULT_ELECTRONIC_BANKING_PROFILE,
    resolve_electronic_banking_profile,
)


def test_resolve_profile_uses_anchor_defaults():
    profile = resolve_electronic_banking_profile("electronic_banking")
    assert profile.anchor_edition_id == "monopoly-00114"
    assert profile.starting_balance > 0
    assert profile.source_policy == "anchor-first"


def test_resolve_profile_falls_back_to_default_for_unknown_preset():
    profile = resolve_electronic_banking_profile("not-a-real-preset")
    assert profile == DEFAULT_ELECTRONIC_BANKING_PROFILE
