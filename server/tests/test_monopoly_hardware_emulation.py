"""Tests for Monopoly hardware/sound emulation framework."""

from server.games.monopoly.hardware_emulation import (
    HardwareEvent,
    resolve_hardware_sound_asset,
    resolve_hardware_event,
)


def test_hardware_event_is_inert_when_sound_mode_none():
    event = HardwareEvent(
        board_id="star_wars_mandalorian",
        event_id="play_theme",
        payload={},
    )

    result = resolve_hardware_event(event, sound_mode="none")

    assert result.status == "ignored"
    assert result.sound_asset == ""
    assert result.sound_asset_source == "none"


def test_hardware_event_is_emulatable_when_sound_mode_emulated(monkeypatch):
    monkeypatch.setattr(
        "server.games.monopoly.hardware_emulation._sound_asset_exists",
        lambda _relative_asset: False,
    )

    event = HardwareEvent(
        board_id="star_wars_mandalorian",
        event_id="play_theme",
        payload={},
    )

    result = resolve_hardware_event(event, sound_mode="emulated")

    assert result.status == "emulated"
    assert result.sound_asset == "game_monopoly_hardware/play_theme_placeholder.ogg"
    assert result.sound_asset_source == "placeholder"


def test_junior_coin_sound_event_is_emulatable_when_sound_mode_emulated(monkeypatch):
    monkeypatch.setattr(
        "server.games.monopoly.hardware_emulation._sound_asset_exists",
        lambda _relative_asset: False,
    )

    event = HardwareEvent(
        board_id="junior_super_mario",
        event_id="junior_coin_sound_powerup",
        payload={"power_up_die": 4, "outcome": "collect_2"},
    )

    result = resolve_hardware_event(event, sound_mode="emulated")

    assert result.status == "emulated"
    assert result.details == "junior_coin_sound_powerup"
    assert result.sound_asset == "game_monopoly_hardware/junior_coin_sound_placeholder.ogg"
    assert result.sound_asset_source == "placeholder"


def test_mario_question_block_event_is_emulatable_when_sound_mode_emulated(monkeypatch):
    monkeypatch.setattr(
        "server.games.monopoly.hardware_emulation._sound_asset_exists",
        lambda _relative_asset: False,
    )

    event = HardwareEvent(
        board_id="mario_celebration",
        event_id="mario_question_block_sound",
        payload={"deck_type": "chance", "card_id": "bank_dividend_50"},
    )

    result = resolve_hardware_event(event, sound_mode="emulated")

    assert result.status == "emulated"
    assert result.details == "mario_question_block_sound"
    assert result.sound_asset == "game_monopoly_hardware/mario_question_block_sound_placeholder.ogg"
    assert result.sound_asset_source == "placeholder"


def test_jurassic_park_gate_theme_event_is_emulatable_when_sound_mode_emulated(monkeypatch):
    monkeypatch.setattr(
        "server.games.monopoly.hardware_emulation._sound_asset_exists",
        lambda _relative_asset: False,
    )

    event = HardwareEvent(
        board_id="jurassic_park",
        event_id="jurassic_park_gate_theme",
        payload={"pass_go_cash": 200},
    )

    result = resolve_hardware_event(event, sound_mode="emulated")

    assert result.status == "emulated"
    assert result.details == "jurassic_park_gate_theme"
    assert result.sound_asset == "game_monopoly_hardware/jurassic_park_gate_theme_placeholder.ogg"
    assert result.sound_asset_source == "placeholder"


def test_jurassic_park_gate_roar_event_is_emulatable_when_sound_mode_emulated(monkeypatch):
    monkeypatch.setattr(
        "server.games.monopoly.hardware_emulation._sound_asset_exists",
        lambda _relative_asset: False,
    )

    event = HardwareEvent(
        board_id="jurassic_park",
        event_id="jurassic_park_gate_roar",
        payload={"pass_go_cash": 100},
    )

    result = resolve_hardware_event(event, sound_mode="emulated")

    assert result.status == "emulated"
    assert result.details == "jurassic_park_gate_roar"
    assert result.sound_asset == "game_monopoly_hardware/jurassic_park_gate_roar_placeholder.ogg"
    assert result.sound_asset_source == "placeholder"


def test_hardware_event_excludes_pacman_game_unit_emulation():
    event = HardwareEvent(
        board_id="pacman",
        event_id="unit_signal",
        payload={},
    )

    result = resolve_hardware_event(event, sound_mode="emulated")

    assert result.status == "ignored"
    assert result.sound_asset == ""
    assert result.sound_asset_source == "none"


def test_resolve_hardware_sound_asset_prefers_original_when_present(monkeypatch):
    monkeypatch.setattr(
        "server.games.monopoly.hardware_emulation._sound_asset_exists",
        lambda relative_asset: relative_asset
        == "game_monopoly_hardware/original/play_theme.ogg",
    )

    sound_asset, sound_asset_source = resolve_hardware_sound_asset("play_theme")

    assert sound_asset == "game_monopoly_hardware/original/play_theme.ogg"
    assert sound_asset_source == "original"


def test_mario_question_block_coin_ping_event_is_emulatable(monkeypatch):
    monkeypatch.setattr(
        "server.games.monopoly.hardware_emulation._sound_asset_exists",
        lambda _relative_asset: False,
    )

    event = HardwareEvent(
        board_id="mario_celebration",
        event_id="mario_question_block_coin_ping",
        payload={"outcome": "coin_ping", "amount": 200},
    )

    result = resolve_hardware_event(event, sound_mode="emulated")

    assert result.status == "emulated"
    assert result.details == "mario_question_block_coin_ping"
    assert result.sound_asset == "game_monopoly_hardware/mario_question_block_coin_ping_placeholder.ogg"
    assert result.sound_asset_source == "placeholder"


def test_mario_question_block_power_up_event_is_emulatable(monkeypatch):
    monkeypatch.setattr(
        "server.games.monopoly.hardware_emulation._sound_asset_exists",
        lambda _relative_asset: False,
    )

    event = HardwareEvent(
        board_id="mario_celebration",
        event_id="mario_question_block_power_up",
        payload={"outcome": "power_up", "amount": 0},
    )

    result = resolve_hardware_event(event, sound_mode="emulated")

    assert result.status == "emulated"
    assert result.details == "mario_question_block_power_up"
    assert result.sound_asset == "game_monopoly_hardware/mario_question_block_power_up_placeholder.ogg"
    assert result.sound_asset_source == "placeholder"


def test_mario_question_block_bowser_event_is_emulatable(monkeypatch):
    monkeypatch.setattr(
        "server.games.monopoly.hardware_emulation._sound_asset_exists",
        lambda _relative_asset: False,
    )

    event = HardwareEvent(
        board_id="mario_celebration",
        event_id="mario_question_block_bowser",
        payload={"outcome": "bowser", "amount": 500},
    )

    result = resolve_hardware_event(event, sound_mode="emulated")

    assert result.status == "emulated"
    assert result.details == "mario_question_block_bowser"
    assert result.sound_asset == "game_monopoly_hardware/mario_question_block_bowser_placeholder.ogg"
    assert result.sound_asset_source == "placeholder"


def test_mario_question_block_game_over_event_is_emulatable(monkeypatch):
    monkeypatch.setattr(
        "server.games.monopoly.hardware_emulation._sound_asset_exists",
        lambda _relative_asset: False,
    )

    event = HardwareEvent(
        board_id="mario_celebration",
        event_id="mario_question_block_game_over",
        payload={"outcome": "game_over", "amount": 1000},
    )

    result = resolve_hardware_event(event, sound_mode="emulated")

    assert result.status == "emulated"
    assert result.details == "mario_question_block_game_over"
    assert result.sound_asset == "game_monopoly_hardware/mario_question_block_game_over_placeholder.ogg"
    assert result.sound_asset_source == "placeholder"


def test_pride_rock_celebration_event_is_emulatable_when_sound_mode_emulated(monkeypatch):
    monkeypatch.setattr(
        "server.games.monopoly.hardware_emulation._sound_asset_exists",
        lambda _relative_asset: False,
    )

    event = HardwareEvent(
        board_id="disney_lion_king",
        event_id="pride_rock_celebration",
        payload={"pass_go_cash": 200},
    )

    result = resolve_hardware_event(event, sound_mode="emulated")

    assert result.status == "emulated"
    assert result.details == "pride_rock_celebration"
    assert result.sound_asset == "game_monopoly_hardware/pride_rock_celebration_placeholder.ogg"
    assert result.sound_asset_source == "placeholder"


def test_resolve_hardware_sound_asset_falls_back_to_placeholder(monkeypatch):
    monkeypatch.setattr(
        "server.games.monopoly.hardware_emulation._sound_asset_exists",
        lambda _relative_asset: False,
    )

    sound_asset, sound_asset_source = resolve_hardware_sound_asset("star_wars_theme")

    assert sound_asset == "game_monopoly_hardware/star_wars_theme_placeholder.ogg"
    assert sound_asset_source == "placeholder"
