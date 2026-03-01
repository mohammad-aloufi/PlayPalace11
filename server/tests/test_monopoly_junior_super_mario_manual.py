"""Manual-core behavior tests for Monopoly Junior Super Mario board rules."""

from __future__ import annotations

import pytest

from server.games.monopoly.game import (
    CLASSIC_STANDARD_BOARD,
    PURCHASABLE_KINDS,
    MonopolyGame,
    MonopolyOptions,
)
from server.core.users.test_user import MockUser


def _start_manual_board_game(player_count: int = 2) -> MonopolyGame:
    """Start a junior Super Mario board-rules game with N players."""
    game = MonopolyGame(
        options=MonopolyOptions(
            preset_id="classic_standard",
            board_id="junior_super_mario",
            board_rules_mode="auto",
        )
    )
    for index in range(player_count):
        name = f"P{index + 1}"
        game.add_player(name, MockUser(name))
    game.host = "P1"
    game.on_start()
    return game


@pytest.mark.parametrize(
    ("player_count", "expected_cash"),
    (
        (2, 20),
        (3, 18),
        (4, 16),
    ),
)
def test_junior_super_mario_starting_cash_uses_player_count_table(
    player_count: int, expected_cash: int
):
    game = _start_manual_board_game(player_count)

    for player in game.turn_players:
        assert player.cash == expected_cash


def test_junior_super_mario_roll_moves_by_numbered_die_only(monkeypatch):
    game = _start_manual_board_game(2)
    host = game.current_player
    assert host is not None

    host.position = 9
    rolls = iter([4, 6])  # numbered die, power-up die
    monkeypatch.setattr("server.games.monopoly.game.random.randint", lambda a, b: next(rolls))

    game.execute_action(host, "roll_dice")

    assert host.position == 13
    assert game.turn_last_roll == [4, 6]


def test_junior_super_mario_zero_coin_player_does_not_enter_timeout(monkeypatch):
    game = _start_manual_board_game(2)
    host = game.current_player
    assert host is not None

    host.cash = 0
    host.position = 29
    rolls = iter([1, 6])  # land on go_to_jail space, no power-up effect
    monkeypatch.setattr("server.games.monopoly.game.random.randint", lambda a, b: next(rolls))

    game.execute_action(host, "roll_dice")

    assert host.in_jail is False
    assert host.position == 30


def test_junior_super_mario_timeout_exit_by_one_coin_then_roll(monkeypatch):
    game = _start_manual_board_game(2)
    host = game.current_player
    assert host is not None

    host.in_jail = True
    host.position = 10
    host.cash = 3
    rolls = iter([2, 6])  # numbered die, no power-up effect
    monkeypatch.setattr("server.games.monopoly.game.random.randint", lambda a, b: next(rolls))

    game.execute_action(host, "roll_dice")

    assert host.in_jail is False
    assert host.cash == 2
    assert host.position == 12


def test_junior_super_mario_auto_buys_affordable_property(monkeypatch):
    game = _start_manual_board_game(2)
    host = game.current_player
    assert host is not None

    host.position = 0
    host.cash = 500
    rolls = iter([1, 6])  # Mediterranean Avenue, no power-up effect
    monkeypatch.setattr("server.games.monopoly.game.random.randint", lambda a, b: next(rolls))

    game.execute_action(host, "roll_dice")

    assert "mediterranean_avenue" in host.owned_space_ids
    assert game.property_owners["mediterranean_avenue"] == host.id
    assert game.turn_pending_purchase_space_id == ""


def test_junior_super_mario_no_auction_when_unaffordable(monkeypatch):
    game = _start_manual_board_game(2)
    host = game.current_player
    assert host is not None

    host.position = 0
    host.cash = 1
    rolls = iter([1, 6])  # Mediterranean Avenue, no power-up effect
    monkeypatch.setattr("server.games.monopoly.game.random.randint", lambda a, b: next(rolls))

    game.execute_action(host, "roll_dice")

    assert "mediterranean_avenue" not in host.owned_space_ids
    assert "mediterranean_avenue" not in game.property_owners
    assert game.turn_pending_purchase_space_id == ""


def test_junior_super_mario_rent_partial_pay_does_not_bankrupt(monkeypatch):
    game = _start_manual_board_game(2)
    host = game.players[0]
    guest = game.players[1]

    host.owned_space_ids.append("mediterranean_avenue")
    game.property_owners["mediterranean_avenue"] = host.id
    guest.position = 0
    guest.cash = 1
    game.turn_index = 1
    game.turn_has_rolled = False
    game.turn_pending_purchase_space_id = ""

    rolls = iter([1, 6])  # land on Mediterranean Avenue, no power-up effect
    monkeypatch.setattr("server.games.monopoly.game.random.randint", lambda a, b: next(rolls))

    game.execute_action(guest, "roll_dice")

    assert guest.bankrupt is False
    assert guest.cash == 0
    assert host.cash == 21


def test_junior_super_mario_card_fee_partial_pay_does_not_bankrupt(monkeypatch):
    game = _start_manual_board_game(2)
    host = game.current_player
    assert host is not None

    host.cash = 1
    host.position = 0
    monkeypatch.setattr(game, "_draw_card", lambda deck_type: "doctor_fee_pay_50")
    rolls = iter([2, 6])  # Community Chest, no power-up effect
    monkeypatch.setattr("server.games.monopoly.game.random.randint", lambda a, b: next(rolls))

    game.execute_action(host, "roll_dice")

    assert host.bankrupt is False
    assert host.cash == 0


def test_junior_super_mario_finishes_when_all_properties_owned():
    game = _start_manual_board_game(2)
    host = game.players[0]

    for space in CLASSIC_STANDARD_BOARD:
        if space.kind not in PURCHASABLE_KINDS:
            continue
        game.property_owners[space.space_id] = host.id
        if space.space_id not in host.owned_space_ids:
            host.owned_space_ids.append(space.space_id)

    assert game._check_junior_endgame() is True
    assert game.status == "finished"
    assert game.game_active is False


def test_junior_super_mario_tie_break_uses_property_count():
    game = _start_manual_board_game(2)
    host = game.players[0]
    guest = game.players[1]

    host.cash = 10
    guest.cash = 10
    host.position = 30
    guest.position = 0

    purchasable = [space for space in CLASSIC_STANDARD_BOARD if space.kind in PURCHASABLE_KINDS]
    for index, space in enumerate(purchasable):
        owner = host if index != len(purchasable) - 1 else guest
        game.property_owners[space.space_id] = owner.id
        if space.space_id not in owner.owned_space_ids:
            owner.owned_space_ids.append(space.space_id)

    assert game._check_junior_endgame() is True
    assert game.current_player is not None
    assert game.current_player.name == "P1"


def test_junior_super_mario_powerup_no_sound_mapping_collects_coins(monkeypatch):
    game = _start_manual_board_game(2)
    host = game.current_player
    assert host is not None

    host.position = 9
    host.cash = 20
    rolls = iter([4, 2])  # numbered die, power-up die collect-1
    monkeypatch.setattr("server.games.monopoly.game.random.randint", lambda a, b: next(rolls))

    game.execute_action(host, "roll_dice")

    assert host.position == 13
    assert host.cash == 21


def test_junior_super_mario_powerup_sound_hook_is_inert_by_default():
    game = _start_manual_board_game(2)

    assert game._resolve_junior_super_mario_powerup_sound_outcome(4) is None
