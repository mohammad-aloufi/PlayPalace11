"""Wave special-audio behavior tests for Jurassic Park Electronic Gate hardware mapping."""

from server.games.monopoly.game import MonopolyGame, MonopolyOptions
from server.games.monopoly.hardware_emulation import resolve_hardware_sound_asset
from server.core.users.test_user import MockUser


def _start_board(board_id: str, sound_mode: str) -> MonopolyGame:
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
    game.active_sound_mode = sound_mode
    return game


def _force_pass_go(game: MonopolyGame, monkeypatch) -> None:
    """Move the current player so they pass GO and trigger gate resolution."""
    host = game.current_player
    assert host is not None

    # Place player near end of board so rolling moves them past GO
    host.position = game.active_board_size - 2
    rolls = iter([1, 2])
    monkeypatch.setattr("server.games.monopoly.game.random.randint", lambda a, b: next(rolls))
    game.execute_action(host, "roll_dice")


def test_jurassic_park_gate_emits_theme_event_in_emulated_mode(monkeypatch):
    game = _start_board("jurassic_park", sound_mode="emulated")
    played: list[str] = []
    monkeypatch.setattr(game, "play_sound", lambda name, volume=100, pan=0, pitch=100: played.append(name))

    # Force gate to return theme outcome (random < 0.5)
    monkeypatch.setattr("server.games.monopoly.game.random.random", lambda: 0.1)
    _force_pass_go(game, monkeypatch)

    expected_asset, expected_source = resolve_hardware_sound_asset("jurassic_park_gate_theme")

    assert game.last_hardware_event_id == "jurassic_park_gate_theme"
    assert game.last_hardware_event_status == "emulated"
    assert expected_asset in played
    assert expected_source in {"original", "placeholder"}


def test_jurassic_park_gate_emits_roar_event_in_emulated_mode(monkeypatch):
    game = _start_board("jurassic_park", sound_mode="emulated")
    played: list[str] = []
    monkeypatch.setattr(game, "play_sound", lambda name, volume=100, pan=0, pitch=100: played.append(name))

    # Force gate to return roar outcome (random >= 0.5)
    monkeypatch.setattr("server.games.monopoly.game.random.random", lambda: 0.9)
    _force_pass_go(game, monkeypatch)

    expected_asset, expected_source = resolve_hardware_sound_asset("jurassic_park_gate_roar")

    assert game.last_hardware_event_id == "jurassic_park_gate_roar"
    assert game.last_hardware_event_status == "emulated"
    assert expected_asset in played
    assert expected_source in {"original", "placeholder"}


def test_jurassic_park_gate_event_is_ignored_in_none_sound_mode_but_credit_randomized(monkeypatch):
    game = _start_board("jurassic_park", sound_mode="none")
    played: list[str] = []
    monkeypatch.setattr(game, "play_sound", lambda name, volume=100, pan=0, pitch=100: played.append(name))

    # Force gate to return roar outcome ($100)
    monkeypatch.setattr("server.games.monopoly.game.random.random", lambda: 0.9)
    host = game.current_player
    assert host is not None
    cash_before = host.cash

    _force_pass_go(game, monkeypatch)

    # Sound event is emitted but ignored (no sound plays)
    assert game.last_hardware_event_id == "jurassic_park_gate_roar"
    assert game.last_hardware_event_status == "ignored"
    assert played == []
    # Credit is still randomized to $100 (roar), not $200
    assert host.cash == cash_before + 100


def test_jurassic_park_gate_theme_credits_200(monkeypatch):
    game = _start_board("jurassic_park", sound_mode="emulated")
    played: list[str] = []
    monkeypatch.setattr(game, "play_sound", lambda name, volume=100, pan=0, pitch=100: played.append(name))

    # Force gate to return theme outcome ($200)
    monkeypatch.setattr("server.games.monopoly.game.random.random", lambda: 0.1)
    host = game.current_player
    assert host is not None
    cash_before = host.cash

    _force_pass_go(game, monkeypatch)

    assert host.cash == cash_before + 200


def test_jurassic_park_gate_roar_credits_100(monkeypatch):
    game = _start_board("jurassic_park", sound_mode="emulated")
    played: list[str] = []
    monkeypatch.setattr(game, "play_sound", lambda name, volume=100, pan=0, pitch=100: played.append(name))

    # Force gate to return roar outcome ($100)
    monkeypatch.setattr("server.games.monopoly.game.random.random", lambda: 0.9)
    host = game.current_player
    assert host is not None
    cash_before = host.cash

    _force_pass_go(game, monkeypatch)

    assert host.cash == cash_before + 100


def test_non_gate_board_does_not_emit_gate_event(monkeypatch):
    game = _start_board("star_wars_mandalorian", sound_mode="emulated")
    played: list[str] = []
    monkeypatch.setattr(game, "play_sound", lambda name, volume=100, pan=0, pitch=100: played.append(name))

    _force_pass_go(game, monkeypatch)

    # Gate events should not fire on non-jurassic_park boards
    assert game.last_hardware_event_id != "jurassic_park_gate_theme"
    assert game.last_hardware_event_id != "jurassic_park_gate_roar"
