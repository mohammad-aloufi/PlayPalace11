"""Wave special-audio behavior tests for Mario Celebration Question Block hardware mechanic."""

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


def _land_on_chance(game: MonopolyGame, monkeypatch, qb_roll: int, extra_rolls: list[int] | None = None) -> None:
    """Move the current player to a chance space, controlling the Question Block die roll.

    qb_roll: the value returned by the first randint(1, 6) inside _resolve_question_block_outcome.
    extra_rolls: additional randint results needed (e.g. coin ping count, power-up movement die).
    """
    host = game.current_player
    assert host is not None

    # Position player 2 steps before chance_1 (position 7), dice 1+1 = 2 steps
    host.position = 5
    all_rolls = [1, 1, qb_roll]
    if extra_rolls:
        all_rolls.extend(extra_rolls)
    roll_iter = iter(all_rolls)
    monkeypatch.setattr("server.games.monopoly.game.random.randint", lambda a, b: next(roll_iter))
    game.execute_action(host, "roll_dice")


def test_question_block_coin_ping_credits_player(monkeypatch):
    game = _start_board("mario_celebration", sound_mode="emulated")
    played: list[str] = []
    monkeypatch.setattr(game, "play_sound", lambda name, volume=100, pan=0, pitch=100: played.append(name))

    host = game.current_player
    assert host is not None
    cash_before = host.cash

    # qb_roll=1 -> coin_ping, coin_count=3 -> $300
    _land_on_chance(game, monkeypatch, qb_roll=1, extra_rolls=[3])

    expected_asset, expected_source = resolve_hardware_sound_asset("mario_question_block_coin_ping")

    assert game.last_hardware_event_id == "mario_question_block_coin_ping"
    assert game.last_hardware_event_status == "emulated"
    assert expected_asset in played
    assert expected_source in {"original", "placeholder"}
    assert host.cash == cash_before + 300


def test_question_block_bowser_debits_500(monkeypatch):
    game = _start_board("mario_celebration", sound_mode="emulated")
    played: list[str] = []
    monkeypatch.setattr(game, "play_sound", lambda name, volume=100, pan=0, pitch=100: played.append(name))

    host = game.current_player
    assert host is not None
    cash_before = host.cash

    # qb_roll=3 -> bowser, $500 debit
    _land_on_chance(game, monkeypatch, qb_roll=3)

    expected_asset, expected_source = resolve_hardware_sound_asset("mario_question_block_bowser")

    assert game.last_hardware_event_id == "mario_question_block_bowser"
    assert game.last_hardware_event_status == "emulated"
    assert expected_asset in played
    assert host.cash == cash_before - 500


def test_question_block_game_over_debits_1000(monkeypatch):
    game = _start_board("mario_celebration", sound_mode="emulated")
    played: list[str] = []
    monkeypatch.setattr(game, "play_sound", lambda name, volume=100, pan=0, pitch=100: played.append(name))

    host = game.current_player
    assert host is not None
    cash_before = host.cash

    # qb_roll=6 -> game_over, $1000 debit
    _land_on_chance(game, monkeypatch, qb_roll=6)

    expected_asset, expected_source = resolve_hardware_sound_asset("mario_question_block_game_over")

    assert game.last_hardware_event_id == "mario_question_block_game_over"
    assert game.last_hardware_event_status == "emulated"
    assert expected_asset in played
    assert host.cash == cash_before - 1000


def test_question_block_power_up_moves_player(monkeypatch):
    game = _start_board("mario_celebration", sound_mode="emulated")
    played: list[str] = []
    monkeypatch.setattr(game, "play_sound", lambda name, volume=100, pan=0, pitch=100: played.append(name))

    host = game.current_player
    assert host is not None

    # qb_roll=5 -> power_up, then movement die=3
    _land_on_chance(game, monkeypatch, qb_roll=5, extra_rolls=[3])

    expected_asset, expected_source = resolve_hardware_sound_asset("mario_question_block_power_up")

    assert game.last_hardware_event_id == "mario_question_block_power_up"
    assert expected_asset in played
    # Player should have moved from chance_1 (pos 7) + 3 = pos 10
    assert host.position == 10


def test_question_block_event_ignored_in_none_mode_but_effect_still_applied(monkeypatch):
    game = _start_board("mario_celebration", sound_mode="none")
    played: list[str] = []
    monkeypatch.setattr(game, "play_sound", lambda name, volume=100, pan=0, pitch=100: played.append(name))

    host = game.current_player
    assert host is not None
    cash_before = host.cash

    # qb_roll=1 -> coin_ping, coin_count=2 -> $200
    _land_on_chance(game, monkeypatch, qb_roll=1, extra_rolls=[2])

    # Sound event emitted but ignored (no audio plays)
    assert game.last_hardware_event_id == "mario_question_block_coin_ping"
    assert game.last_hardware_event_status == "ignored"
    assert played == []
    # Gameplay effect still applies
    assert host.cash == cash_before + 200


def test_non_question_block_board_draws_chance_normally(monkeypatch):
    game = _start_board("mario_movie", sound_mode="emulated")
    played: list[str] = []
    monkeypatch.setattr(game, "play_sound", lambda name, volume=100, pan=0, pitch=100: played.append(name))

    host = game.current_player
    assert host is not None

    host.position = 5
    monkeypatch.setattr(game, "_draw_card", lambda deck_type: "bank_dividend_50")
    rolls = iter([1, 1])
    monkeypatch.setattr("server.games.monopoly.game.random.randint", lambda a, b: next(rolls))
    game.execute_action(host, "roll_dice")

    # Should not have any question block event
    assert game.last_hardware_event_id != "mario_question_block_coin_ping"
    assert game.last_hardware_event_id != "mario_question_block_bowser"
    assert game.last_hardware_event_id != "mario_question_block_power_up"
    assert game.last_hardware_event_id != "mario_question_block_game_over"


def test_question_block_does_not_advance_chance_deck(monkeypatch):
    game = _start_board("mario_celebration", sound_mode="emulated")
    played: list[str] = []
    monkeypatch.setattr(game, "play_sound", lambda name, volume=100, pan=0, pitch=100: played.append(name))

    deck_index_before = game.chance_deck_index

    # qb_roll=3 -> bowser (no card draw)
    _land_on_chance(game, monkeypatch, qb_roll=3)

    # Chance deck should not have advanced
    assert game.chance_deck_index == deck_index_before
