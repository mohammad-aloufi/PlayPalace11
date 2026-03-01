"""Wave special-audio behavior tests for Disney Lion King Pride Rock hardware mapping."""

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
    """Move the current player so they pass GO and trigger Pride Rock resolution."""
    host = game.current_player
    assert host is not None

    # Place player near end of board so rolling moves them past GO
    host.position = game.active_board_size - 2
    rolls = iter([1, 2])
    monkeypatch.setattr("server.games.monopoly.game.random.randint", lambda a, b: next(rolls))
    game.execute_action(host, "roll_dice")


def test_lion_king_pride_rock_emits_event_in_emulated_mode(monkeypatch):
    game = _start_board("disney_lion_king", sound_mode="emulated")
    played: list[str] = []
    monkeypatch.setattr(game, "play_sound", lambda name, volume=100, pan=0, pitch=100: played.append(name))

    _force_pass_go(game, monkeypatch)

    expected_asset, expected_source = resolve_hardware_sound_asset("pride_rock_celebration")

    assert game.last_hardware_event_id == "pride_rock_celebration"
    assert game.last_hardware_event_status == "emulated"
    assert expected_asset in played
    assert expected_source in {"original", "placeholder"}


def test_lion_king_pride_rock_event_is_ignored_in_none_sound_mode(monkeypatch):
    game = _start_board("disney_lion_king", sound_mode="none")
    played: list[str] = []
    monkeypatch.setattr(game, "play_sound", lambda name, volume=100, pan=0, pitch=100: played.append(name))

    _force_pass_go(game, monkeypatch)

    # Sound event is emitted but ignored (no sound plays)
    assert game.last_hardware_event_id == "pride_rock_celebration"
    assert game.last_hardware_event_status == "ignored"
    assert played == []


def test_lion_king_pride_rock_does_not_affect_cash(monkeypatch):
    game = _start_board("disney_lion_king", sound_mode="emulated")
    played: list[str] = []
    monkeypatch.setattr(game, "play_sound", lambda name, volume=100, pan=0, pitch=100: played.append(name))

    host = game.current_player
    assert host is not None
    cash_before = host.cash

    _force_pass_go(game, monkeypatch)

    # Pride Rock is purely celebratory — cash is standard $200
    assert host.cash == cash_before + 200


def test_non_pride_rock_board_does_not_emit_event(monkeypatch):
    game = _start_board("star_wars_mandalorian", sound_mode="emulated")
    played: list[str] = []
    monkeypatch.setattr(game, "play_sound", lambda name, volume=100, pan=0, pitch=100: played.append(name))

    _force_pass_go(game, monkeypatch)

    # Pride Rock events should not fire on non-lion-king boards
    assert game.last_hardware_event_id != "pride_rock_celebration"
