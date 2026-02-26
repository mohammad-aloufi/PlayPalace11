"""Tests for Monopoly voice banking profile resolver."""

from server.games.monopoly.voice_banking_profile import (
    DEFAULT_VOICE_BANKING_PROFILE,
    resolve_voice_banking_profile,
)


def test_resolve_voice_profile_uses_anchor_defaults():
    profile = resolve_voice_banking_profile("voice_banking")
    assert profile.preset_id == "voice_banking"
    assert profile.anchor_edition_id == "monopoly-e4816"
    assert profile.source_policy == "anchor-first"
    assert profile.confirmation_required_for_transfers is True


def test_resolve_voice_profile_falls_back_to_default():
    profile = resolve_voice_banking_profile("unknown")
    assert profile == DEFAULT_VOICE_BANKING_PROFILE
