"""Tests for Monopoly Junior modern and legacy preset behavior."""

from server.game_utils.actions import Visibility
from server.games.monopoly.game import (
    CLASSIC_STANDARD_BOARD,
    PURCHASABLE_KINDS,
    MonopolyGame,
    MonopolyOptions,
)
from server.core.users.test_user import MockUser


def _create_two_player_game(options: MonopolyOptions | None = None) -> MonopolyGame:
    """Create a Monopoly game with two human players."""
    game = MonopolyGame(options=options or MonopolyOptions())
    host_user = MockUser("Host")
    guest_user = MockUser("Guest")
    game.add_player("Host", host_user)
    game.add_player("Guest", guest_user)
    game.host = "Host"
    return game


def _start_two_player_game(options: MonopolyOptions | None = None) -> MonopolyGame:
    """Create and start a two player Monopoly game."""
    game = _create_two_player_game(options)
    game.on_start()
    return game


def test_junior_presets_use_distinct_starting_cash():
    modern = _start_two_player_game(MonopolyOptions(preset_id="junior_modern"))
    legacy = _start_two_player_game(MonopolyOptions(preset_id="junior_legacy"))

    assert modern.players[0].cash == 31
    assert legacy.players[0].cash == 20


def test_junior_roll_uses_one_die(monkeypatch):
    game = _start_two_player_game(MonopolyOptions(preset_id="junior_modern"))
    host = game.current_player
    assert host is not None

    rolls = iter([3])  # one die only
    monkeypatch.setattr("server.games.monopoly.game.random.randint", lambda a, b: next(rolls))
    game.execute_action(host, "roll_dice")

    assert game.turn_last_roll == [3]


def test_junior_hides_incompatible_actions():
    game = _start_two_player_game(MonopolyOptions(preset_id="junior_modern"))
    host = game.current_player
    assert host is not None

    assert game._is_build_house_hidden(host) == Visibility.HIDDEN
    assert game._is_mortgage_property_hidden(host) == Visibility.HIDDEN
    assert game._is_offer_trade_hidden(host) == Visibility.HIDDEN


def test_junior_bot_uses_junior_turn_path():
    game = _start_two_player_game(MonopolyOptions(preset_id="junior_modern"))
    host = game.current_player
    assert host is not None
    host.is_bot = True

    assert game.bot_think(host) == "roll_dice"


def test_junior_rent_mode_differs_between_modern_and_legacy(monkeypatch):
    monkeypatch.setattr("server.games.monopoly.game.random.randint", lambda a, b: 3)

    modern = _start_two_player_game(MonopolyOptions(preset_id="junior_modern"))
    modern_host = modern.players[0]
    modern_guest = modern.players[1]
    for space_id in ("mediterranean_avenue", "baltic_avenue"):
        modern_host.owned_space_ids.append(space_id)
        modern.property_owners[space_id] = modern_host.id
    modern.current_player = modern_guest
    modern.turn_has_rolled = False
    modern.turn_pending_purchase_space_id = ""
    modern_guest.position = 0
    modern.execute_action(modern_guest, "roll_dice")

    legacy = _start_two_player_game(MonopolyOptions(preset_id="junior_legacy"))
    legacy_host = legacy.players[0]
    legacy_guest = legacy.players[1]
    for space_id in ("mediterranean_avenue", "baltic_avenue"):
        legacy_host.owned_space_ids.append(space_id)
        legacy.property_owners[space_id] = legacy_host.id
    legacy.current_player = legacy_guest
    legacy.turn_has_rolled = False
    legacy.turn_pending_purchase_space_id = ""
    legacy_guest.position = 0
    legacy.execute_action(legacy_guest, "roll_dice")

    modern_paid = 31 - modern_guest.cash
    legacy_paid = 20 - legacy_guest.cash
    assert modern_paid == 5
    assert legacy_paid == 8


def test_junior_modern_endgame_triggers_when_all_properties_owned():
    game = _start_two_player_game(MonopolyOptions(preset_id="junior_modern"))
    host = game.players[0]

    purchasable_ids = [
        space.space_id for space in CLASSIC_STANDARD_BOARD if space.kind in PURCHASABLE_KINDS
    ]
    for space_id in purchasable_ids:
        game.property_owners[space_id] = host.id
        if space_id not in host.owned_space_ids:
            host.owned_space_ids.append(space_id)

    assert game._check_junior_endgame() is True
    assert game.status == "finished"
    assert game.game_active is False
    assert game.current_player is not None
    assert game.current_player.name == "Host"
