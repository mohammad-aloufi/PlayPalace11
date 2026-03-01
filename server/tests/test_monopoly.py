"""Tests for Monopoly scaffold and preset wiring."""

from server.games.monopoly.game import (
    MonopolyGame,
    MonopolyOptions,
    MonopolyTradeOffer,
    STARTING_CASH,
    PASS_GO_CASH,
    BAIL_AMOUNT,
    SPACE_BY_ID,
)
from server.games.monopoly.presets import (
    DEFAULT_PRESET_ID,
    get_available_preset_ids,
    get_default_preset_id,
    get_preset,
)
from server.games.registry import get_game_class
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


def _find_trade_option(game: MonopolyGame, player, text: str) -> str | None:
    """Return first trade option containing the provided text."""
    for option in game._options_for_offer_trade(player):
        if text in option:
            return option
    return None


def test_monopoly_game_creation():
    game = MonopolyGame()
    assert game.get_name() == "Monopoly"
    assert game.get_name_key() == "game-name-monopoly"
    assert game.get_type() == "monopoly"
    assert game.get_category() == "category-uncategorized"
    assert game.get_min_players() == 2
    assert game.get_max_players() == 6
    assert game.options.preset_id == DEFAULT_PRESET_ID


def test_monopoly_registered():
    assert get_game_class("monopoly") is MonopolyGame


def test_monopoly_preset_catalog_includes_classic():
    preset_ids = get_available_preset_ids()
    assert DEFAULT_PRESET_ID in preset_ids

    default_preset = get_preset(get_default_preset_id())
    assert default_preset is not None
    assert default_preset.edition_count > 0


def test_monopoly_options_present_catalog_preset_choices():
    game = _create_two_player_game()
    host_player = game.players[0]
    options_action_set = game.get_action_set(host_player, "options")
    assert options_action_set is not None

    set_preset_action = options_action_set.get_action("set_preset_id")
    assert set_preset_action is not None

    menu_options = game._get_menu_options_for_action(set_preset_action, host_player)
    assert menu_options is not None
    assert DEFAULT_PRESET_ID in menu_options
    assert "junior_modern" in menu_options
    assert "junior_legacy" in menu_options
    assert "free_parking_jackpot" in menu_options
    assert "sore_losers" in menu_options


def test_monopoly_on_start_uses_selected_preset():
    game = _start_two_player_game(MonopolyOptions(preset_id="junior"))

    assert game.status == "playing"
    assert game.game_active is True
    assert game.active_preset_id == "junior"
    assert game.active_preset_name
    assert game.active_edition_ids
    assert len(game.team_manager.teams) == 2


def test_monopoly_on_start_falls_back_to_default_preset():
    game = _start_two_player_game(MonopolyOptions(preset_id="not-a-real-preset"))

    assert game.active_preset_id == get_default_preset_id()
    assert game.options.preset_id == get_default_preset_id()


def test_monopoly_on_start_supports_non_catalog_alias_preset():
    game = _start_two_player_game(MonopolyOptions(preset_id="sore_losers"))

    assert game.active_preset_id == "sore_losers"
    assert game.options.preset_id == "sore_losers"
    assert game.active_edition_ids


def test_monopoly_on_start_supports_junior_modern_alias():
    game = _start_two_player_game(MonopolyOptions(preset_id="junior_modern"))

    assert game.active_preset_id == "junior_modern"
    assert game.options.preset_id == "junior_modern"
    assert game.active_anchor_edition_id == "monopoly-f8562"


def test_monopoly_on_start_supports_junior_legacy_alias():
    game = _start_two_player_game(MonopolyOptions(preset_id="junior_legacy"))

    assert game.active_preset_id == "junior_legacy"
    assert game.options.preset_id == "junior_legacy"
    assert game.active_anchor_edition_id == "monopoly-00441"


def test_monopoly_on_start_initializes_cash_positions_and_scores():
    game = _start_two_player_game()

    assert game.current_player is not None
    assert game.current_player.name == "Host"
    assert game.turn_has_rolled is False
    assert game.turn_pending_purchase_space_id == ""
    assert len(game.property_owners) == 0

    for player in game.players:
        assert player.position == 0
        assert player.cash == STARTING_CASH
        assert player.owned_space_ids == []

    assert len(game.team_manager.teams) == 2
    assert sorted(team.total_score for team in game.team_manager.teams) == [
        STARTING_CASH,
        STARTING_CASH,
    ]


def test_monopoly_speed_preset_uses_profile_starting_cash():
    game = _start_two_player_game(MonopolyOptions(preset_id="speed"))

    for player in game.players:
        assert player.cash == 1000


def test_monopoly_roll_sets_pending_property_when_unowned(monkeypatch):
    game = _start_two_player_game()
    host = game.current_player
    assert host is not None

    rolls = iter([1, 2])  # total = 3 -> Baltic Avenue
    monkeypatch.setattr("server.games.monopoly.game.random.randint", lambda a, b: next(rolls))

    game.execute_action(host, "roll_dice")

    assert host.position == 3
    assert game.turn_has_rolled is True
    assert game.turn_pending_purchase_space_id == "baltic_avenue"
    assert host.cash == STARTING_CASH


def test_monopoly_buy_property_deducts_cash_and_assigns_owner(monkeypatch):
    game = _start_two_player_game()
    host = game.current_player
    assert host is not None

    rolls = iter([1, 2])  # total = 3 -> Baltic Avenue ($60)
    monkeypatch.setattr("server.games.monopoly.game.random.randint", lambda a, b: next(rolls))

    game.execute_action(host, "roll_dice")
    game.execute_action(host, "buy_property")

    assert game.property_owners["baltic_avenue"] == host.id
    assert host.cash == STARTING_CASH - 60
    assert "baltic_avenue" in host.owned_space_ids
    assert game.turn_pending_purchase_space_id == ""


def test_monopoly_end_turn_advances_and_resets_turn_state(monkeypatch):
    game = _start_two_player_game()
    host = game.current_player
    assert host is not None
    game.chance_deck_order = ["bank_dividend_50"]
    game.chance_deck_index = 0

    rolls = iter([3, 4])  # total = 7 -> chance (safe card)
    monkeypatch.setattr("server.games.monopoly.game.random.randint", lambda a, b: next(rolls))
    game.execute_action(host, "roll_dice")
    assert game.turn_has_rolled is True

    game.execute_action(host, "end_turn")

    assert game.current_player is not None
    assert game.current_player.name == "Guest"
    assert game.turn_has_rolled is False
    assert game.turn_last_roll == []
    assert game.turn_pending_purchase_space_id == ""


def test_monopoly_pass_go_awards_cash(monkeypatch):
    game = _start_two_player_game()
    host = game.current_player
    assert host is not None
    host.position = 39

    rolls = iter([1, 1])  # total = 2 -> wraps around
    monkeypatch.setattr("server.games.monopoly.game.random.randint", lambda a, b: next(rolls))

    game.execute_action(host, "roll_dice")

    assert host.position == 1
    assert host.cash == STARTING_CASH + PASS_GO_CASH


def test_monopoly_speed_pass_go_awards_profile_cash(monkeypatch):
    game = _start_two_player_game(MonopolyOptions(preset_id="speed"))
    host = game.current_player
    assert host is not None
    host.position = 38

    rolls = iter([1, 1])  # total = 2 -> GO
    monkeypatch.setattr("server.games.monopoly.game.random.randint", lambda a, b: next(rolls))

    game.execute_action(host, "roll_dice")

    assert host.position == 0
    assert host.cash == 1100


def test_monopoly_rent_transfers_cash_to_owner(monkeypatch):
    game = _start_two_player_game()
    host = game.current_player
    assert host is not None

    # Host lands on Baltic (3), buys it, then ends turn.
    # Guest lands on Baltic and pays rent (4).
    rolls = iter([1, 2, 1, 2])
    monkeypatch.setattr("server.games.monopoly.game.random.randint", lambda a, b: next(rolls))

    game.execute_action(host, "roll_dice")
    game.execute_action(host, "buy_property")
    game.execute_action(host, "end_turn")

    guest = game.current_player
    assert guest is not None
    game.execute_action(guest, "roll_dice")

    assert host.cash == STARTING_CASH - 60 + 4
    assert guest.cash == STARTING_CASH - 4


def test_monopoly_income_tax_space_deducts_cash(monkeypatch):
    game = _start_two_player_game()
    host = game.current_player
    assert host is not None

    rolls = iter([2, 2])  # total = 4 -> Income Tax
    monkeypatch.setattr("server.games.monopoly.game.random.randint", lambda a, b: next(rolls))

    game.execute_action(host, "roll_dice")

    assert host.position == 4
    assert host.cash == STARTING_CASH - 200
    assert game.turn_pending_purchase_space_id == ""


def test_monopoly_free_parking_jackpot_preset_collects_bank_payments(monkeypatch):
    game = _start_two_player_game(MonopolyOptions(preset_id="free_parking_jackpot"))
    host = game.current_player
    assert host is not None
    guest = game.players[1]

    rolls = iter([1, 3])  # host to Income Tax (200)
    monkeypatch.setattr("server.games.monopoly.game.random.randint", lambda a, b: next(rolls))
    game.execute_action(host, "roll_dice")

    assert host.cash == STARTING_CASH - 200
    assert game.free_parking_pool == 200

    game.execute_action(host, "end_turn")
    guest.position = 17
    rolls = iter([1, 2])  # guest to Free Parking
    monkeypatch.setattr("server.games.monopoly.game.random.randint", lambda a, b: next(rolls))
    game.execute_action(guest, "roll_dice")

    assert guest.position == 20
    assert guest.cash == STARTING_CASH + 200
    assert game.free_parking_pool == 0


def test_monopoly_sore_losers_rebate_applies_to_tax_payment(monkeypatch):
    game = _start_two_player_game(MonopolyOptions(preset_id="sore_losers"))
    host = game.current_player
    assert host is not None

    rolls = iter([2, 2])  # total = 4 -> Income Tax
    monkeypatch.setattr("server.games.monopoly.game.random.randint", lambda a, b: next(rolls))
    game.execute_action(host, "roll_dice")

    assert host.position == 4
    assert host.cash == STARTING_CASH - 200 + 10


def test_monopoly_sore_losers_rebate_applies_to_rent(monkeypatch):
    game = _start_two_player_game(MonopolyOptions(preset_id="sore_losers"))
    host = game.current_player
    assert host is not None

    rolls = iter([1, 2, 1, 2])  # host buys Baltic, guest pays rent on Baltic
    monkeypatch.setattr("server.games.monopoly.game.random.randint", lambda a, b: next(rolls))

    game.execute_action(host, "roll_dice")
    game.execute_action(host, "buy_property")
    game.execute_action(host, "end_turn")

    guest = game.current_player
    assert guest is not None
    game.execute_action(guest, "roll_dice")

    assert host.cash == STARTING_CASH - 60 + 4
    assert guest.cash == STARTING_CASH


def test_monopoly_go_to_jail_space_moves_player_to_jail(monkeypatch):
    game = _start_two_player_game()
    host = game.current_player
    assert host is not None
    host.position = 28

    rolls = iter([1, 1])  # total = 2 -> Go to Jail
    monkeypatch.setattr("server.games.monopoly.game.random.randint", lambda a, b: next(rolls))

    game.execute_action(host, "roll_dice")

    assert host.position == 10
    assert game.turn_pending_purchase_space_id == ""


def test_monopoly_rent_shortfall_triggers_auto_liquidation_before_payment(monkeypatch):
    game = _start_two_player_game()
    host = game.players[0]
    guest = game.players[1]

    host.owned_space_ids.append("boardwalk")
    game.property_owners["boardwalk"] = host.id
    guest.owned_space_ids.append("baltic_avenue")
    game.property_owners["baltic_avenue"] = guest.id
    guest.cash = 30
    guest.position = 36
    game.current_player = guest
    game.turn_has_rolled = False
    game.turn_pending_purchase_space_id = ""

    rolls = iter([1, 2])  # total = 3 -> Boardwalk (rent 50)
    monkeypatch.setattr("server.games.monopoly.game.random.randint", lambda a, b: next(rolls))

    game.execute_action(guest, "roll_dice")

    assert guest.bankrupt is False
    assert host.cash == STARTING_CASH + 50
    assert guest.cash == 10
    assert "baltic_avenue" in guest.owned_space_ids
    assert "baltic_avenue" in game.mortgaged_space_ids


def test_monopoly_bankrupt_when_liquidation_cannot_cover_rent(monkeypatch):
    game = _start_two_player_game()
    host = game.players[0]
    guest = game.players[1]

    host.owned_space_ids.append("boardwalk")
    game.property_owners["boardwalk"] = host.id
    guest.cash = 30
    guest.position = 36
    game.current_player = guest
    game.turn_has_rolled = False
    game.turn_pending_purchase_space_id = ""

    rolls = iter([1, 2])  # total = 3 -> Boardwalk (rent 50)
    monkeypatch.setattr("server.games.monopoly.game.random.randint", lambda a, b: next(rolls))

    game.execute_action(guest, "roll_dice")

    assert guest.bankrupt is True
    assert game.status == "finished"
    assert game.game_active is False
    assert game.current_player is not None
    assert game.current_player.name == "Host"
    assert host.cash == STARTING_CASH + 30


def test_monopoly_bankruptcy_transfers_assets_to_creditor(monkeypatch):
    game = _start_two_player_game()
    host = game.players[0]
    guest = game.players[1]

    host.owned_space_ids.append("boardwalk")
    game.property_owners["boardwalk"] = host.id
    guest.owned_space_ids.append("mediterranean_avenue")
    game.property_owners["mediterranean_avenue"] = guest.id
    guest.cash = 10
    guest.get_out_of_jail_cards = 1
    guest.position = 36
    game.current_player = guest
    game.turn_has_rolled = False
    game.turn_pending_purchase_space_id = ""

    rolls = iter([1, 2])  # total = 3 -> Boardwalk (rent 50)
    monkeypatch.setattr("server.games.monopoly.game.random.randint", lambda a, b: next(rolls))

    game.execute_action(guest, "roll_dice")

    assert guest.bankrupt is True
    assert game.property_owners["mediterranean_avenue"] == host.id
    assert "mediterranean_avenue" in host.owned_space_ids
    assert guest.get_out_of_jail_cards == 0
    assert host.get_out_of_jail_cards == 1
    assert "mediterranean_avenue" in game.mortgaged_space_ids
    assert host.cash == STARTING_CASH + 40


def test_monopoly_doubles_grant_extra_roll(monkeypatch):
    game = _start_two_player_game()
    host = game.current_player
    assert host is not None

    rolls = iter([2, 2])  # total = 4 (income tax), doubles
    monkeypatch.setattr("server.games.monopoly.game.random.randint", lambda a, b: next(rolls))
    game.execute_action(host, "roll_dice")

    assert game.current_player is host
    assert game.turn_has_rolled is False
    assert game.turn_doubles_count == 1
    assert host.position == 4


def test_monopoly_speed_doubles_do_not_grant_extra_roll(monkeypatch):
    game = _start_two_player_game(MonopolyOptions(preset_id="speed"))
    host = game.current_player
    assert host is not None

    rolls = iter([2, 2])  # total = 4 (income tax), doubles
    monkeypatch.setattr("server.games.monopoly.game.random.randint", lambda a, b: next(rolls))
    game.execute_action(host, "roll_dice")

    assert game.current_player is host
    assert game.turn_has_rolled is True
    assert game.turn_can_roll_again is False
    assert game.turn_doubles_count == 0
    assert host.position == 4


def test_monopoly_three_doubles_send_player_to_jail(monkeypatch):
    game = _start_two_player_game()
    host = game.current_player
    assert host is not None
    game.chance_deck_order = ["bank_dividend_50"]
    game.community_chest_deck_order = ["income_tax_refund_20"]
    game.chance_deck_index = 0
    game.community_chest_deck_index = 0

    rolls = iter([2, 2, 3, 3, 4, 4])
    monkeypatch.setattr("server.games.monopoly.game.random.randint", lambda a, b: next(rolls))
    game.execute_action(host, "roll_dice")
    game.execute_action(host, "roll_dice")
    game.execute_action(host, "roll_dice")

    assert host.in_jail is True
    assert host.position == 10
    assert game.turn_has_rolled is True


def test_monopoly_pay_bail_allows_normal_roll_after(monkeypatch):
    game = _start_two_player_game()
    host = game.current_player
    assert host is not None
    host.in_jail = True
    host.position = 10

    game.execute_action(host, "pay_bail")
    assert host.in_jail is False
    assert host.cash == STARTING_CASH - BAIL_AMOUNT
    assert game.turn_has_rolled is False

    rolls = iter([1, 2])
    monkeypatch.setattr("server.games.monopoly.game.random.randint", lambda a, b: next(rolls))
    game.execute_action(host, "roll_dice")

    assert host.position == 13


def test_monopoly_sore_losers_rebate_applies_to_bail_payment():
    game = _start_two_player_game(MonopolyOptions(preset_id="sore_losers"))
    host = game.current_player
    assert host is not None
    host.in_jail = True
    host.position = 10

    game.execute_action(host, "pay_bail")

    assert host.in_jail is False
    assert host.cash == STARTING_CASH - BAIL_AMOUNT + 10


def test_monopoly_failed_jail_roll_increments_attempts(monkeypatch):
    game = _start_two_player_game()
    host = game.current_player
    assert host is not None
    host.in_jail = True
    host.position = 10

    rolls = iter([1, 2])
    monkeypatch.setattr("server.games.monopoly.game.random.randint", lambda a, b: next(rolls))
    game.execute_action(host, "roll_dice")

    assert host.in_jail is True
    assert host.jail_turns == 1
    assert host.position == 10
    assert game.turn_has_rolled is True


def test_monopoly_community_chest_can_grant_jail_card(monkeypatch):
    game = _start_two_player_game()
    host = game.current_player
    assert host is not None
    game.community_chest_deck_order = ["get_out_of_jail_free"]
    game.community_chest_deck_index = 0

    rolls = iter([1, 1])  # total = 2 -> community chest
    monkeypatch.setattr("server.games.monopoly.game.random.randint", lambda a, b: next(rolls))
    game.execute_action(host, "roll_dice")

    assert host.get_out_of_jail_cards == 1


def test_monopoly_chance_go_back_three_resolves_destination(monkeypatch):
    game = _start_two_player_game()
    host = game.current_player
    assert host is not None
    host.position = 4
    game.chance_deck_order = ["go_back_three"]
    game.chance_deck_index = 0

    rolls = iter([1, 2])  # total = 3 -> chance at 7, then back to 4 income tax
    monkeypatch.setattr("server.games.monopoly.game.random.randint", lambda a, b: next(rolls))
    game.execute_action(host, "roll_dice")

    assert host.position == 4
    assert host.cash == STARTING_CASH - 200


def test_monopoly_auction_sells_pending_property(monkeypatch):
    game = _start_two_player_game()
    host = game.current_player
    assert host is not None
    guest = game.players[1]

    rolls = iter([1, 2])  # total = 3 -> Baltic
    monkeypatch.setattr("server.games.monopoly.game.random.randint", lambda a, b: next(rolls))
    game.execute_action(host, "roll_dice")
    game.execute_action(host, "auction_property")
    game.execute_action(guest, "auction_bid", input_value="10")
    game.execute_action(host, "auction_pass")

    assert game.turn_pending_purchase_space_id == ""
    assert game.pending_auction_space_id == ""
    assert game.property_owners.get("baltic_avenue") is not None


def test_monopoly_speed_auto_auctions_and_disables_manual_buy(monkeypatch):
    game = _start_two_player_game(MonopolyOptions(preset_id="speed"))
    host = game.current_player
    assert host is not None
    assert game._is_buy_property_enabled(host) == "monopoly-buy-disabled"

    rolls = iter([1, 2])  # total = 3 -> Baltic
    monkeypatch.setattr("server.games.monopoly.game.random.randint", lambda a, b: next(rolls))
    game.execute_action(host, "roll_dice")

    assert game.turn_pending_purchase_space_id == ""
    assert game.property_owners.get("baltic_avenue") is not None
    assert sum(player.cash for player in game.players) == 1940


def test_monopoly_auction_respects_doubles_roll_chain(monkeypatch):
    game = _start_two_player_game()
    host = game.current_player
    assert host is not None
    guest = game.players[1]

    rolls = iter([3, 3])  # total = 6 -> Oriental (property), doubles
    monkeypatch.setattr("server.games.monopoly.game.random.randint", lambda a, b: next(rolls))
    game.execute_action(host, "roll_dice")
    assert game.turn_can_roll_again is True
    game.execute_action(host, "auction_property")
    game.execute_action(guest, "auction_bid", input_value="10")
    game.execute_action(host, "auction_pass")

    assert game.turn_has_rolled is False
    assert game.turn_can_roll_again is False


def test_monopoly_builder_buy_awards_blocks_and_allows_build_without_full_set(monkeypatch):
    game = _start_two_player_game(MonopolyOptions(preset_id="builder"))
    host = game.current_player
    assert host is not None

    rolls = iter([1, 2])  # total = 3 -> Baltic
    monkeypatch.setattr("server.games.monopoly.game.random.randint", lambda a, b: next(rolls))
    game.execute_action(host, "roll_dice")
    game.execute_action(host, "buy_property")

    assert host.builder_blocks == 1
    assert game.property_owners["baltic_avenue"] == host.id

    house_cost = SPACE_BY_ID["baltic_avenue"].house_cost
    cash_after_buy = host.cash
    game.execute_action(host, "build_house", input_value="baltic_avenue")

    assert game._building_level("baltic_avenue") == 1
    assert host.builder_blocks == 0
    assert host.cash == cash_after_buy - house_cost

    game.execute_action(host, "build_house", input_value="baltic_avenue")
    assert game._building_level("baltic_avenue") == 1


def test_monopoly_builder_auction_awards_builder_blocks(monkeypatch):
    game = _start_two_player_game(MonopolyOptions(preset_id="builder"))
    host = game.current_player
    assert host is not None
    guest = game.players[1]

    rolls = iter([1, 2])  # total = 3 -> Baltic
    monkeypatch.setattr("server.games.monopoly.game.random.randint", lambda a, b: next(rolls))
    game.execute_action(host, "roll_dice")
    game.execute_action(host, "auction_property")
    game.execute_action(guest, "auction_bid", input_value="10")
    game.execute_action(host, "auction_pass")

    owner_id = game.property_owners.get("baltic_avenue")
    assert owner_id is not None
    owner = game.get_player_by_id(owner_id)
    assert owner is not None
    assert owner.builder_blocks == 1


def test_monopoly_mortgage_and_unmortgage_cycle():
    game = _start_two_player_game()
    host = game.current_player
    assert host is not None
    host.owned_space_ids.append("boardwalk")
    game.property_owners["boardwalk"] = host.id

    game.execute_action(host, "mortgage_property", input_value="boardwalk")
    assert "boardwalk" in game.mortgaged_space_ids
    assert host.cash == STARTING_CASH + 200

    game.execute_action(host, "unmortgage_property", input_value="boardwalk")
    assert "boardwalk" not in game.mortgaged_space_ids
    assert host.cash == STARTING_CASH - 20


def test_monopoly_trade_offer_accept_transfers_property_for_cash():
    game = _start_two_player_game()
    host = game.current_player
    assert host is not None
    guest = game.players[1]

    host.owned_space_ids.append("baltic_avenue")
    game.property_owners["baltic_avenue"] = host.id

    offer = _find_trade_option(game, host, "Sell Baltic Avenue to Guest for 60")
    assert offer is not None

    game.execute_action(host, "offer_trade", input_value=offer)
    assert game.pending_trade_offer is not None
    assert game.pending_trade_offer.target_id == guest.id

    game.execute_action(guest, "accept_trade")

    assert game.pending_trade_offer is None
    assert game.property_owners["baltic_avenue"] == guest.id
    assert "baltic_avenue" not in host.owned_space_ids
    assert "baltic_avenue" in guest.owned_space_ids
    assert host.cash == STARTING_CASH + 60
    assert guest.cash == STARTING_CASH - 60


def test_monopoly_trade_offer_decline_keeps_state_unchanged():
    game = _start_two_player_game()
    host = game.current_player
    assert host is not None
    guest = game.players[1]

    host.owned_space_ids.append("baltic_avenue")
    game.property_owners["baltic_avenue"] = host.id

    offer = _find_trade_option(game, host, "Sell Baltic Avenue to Guest for 60")
    assert offer is not None

    game.execute_action(host, "offer_trade", input_value=offer)
    assert game.pending_trade_offer is not None

    game.execute_action(guest, "decline_trade")

    assert game.pending_trade_offer is None
    assert game.property_owners["baltic_avenue"] == host.id
    assert host.cash == STARTING_CASH
    assert guest.cash == STARTING_CASH


def test_monopoly_trade_options_block_properties_when_group_has_buildings():
    game = _start_two_player_game()
    host = game.current_player
    assert host is not None

    for space_id in ("mediterranean_avenue", "baltic_avenue"):
        host.owned_space_ids.append(space_id)
        game.property_owners[space_id] = host.id
    game._set_building_level("mediterranean_avenue", 1)

    assert game._options_for_offer_trade(host) == []


def test_monopoly_trade_options_include_swap_and_cash_balancing():
    game = _start_two_player_game()
    host = game.current_player
    assert host is not None
    guest = game.players[1]

    host.owned_space_ids.append("baltic_avenue")
    game.property_owners["baltic_avenue"] = host.id
    guest.owned_space_ids.append("oriental_avenue")
    game.property_owners["oriental_avenue"] = guest.id

    options = game._options_for_offer_trade(host)
    assert any("Swap Baltic Avenue with Guest for Oriental Avenue" in option for option in options)
    assert any(
        "Swap Baltic Avenue + 40 with Guest for Oriental Avenue" in option
        for option in options
    )


def test_monopoly_trade_accept_invalid_offer_cancels_pending():
    game = _start_two_player_game()
    host = game.current_player
    assert host is not None
    guest = game.players[1]

    host.owned_space_ids.append("baltic_avenue")
    game.property_owners["baltic_avenue"] = host.id

    offer = _find_trade_option(game, host, "Sell Baltic Avenue to Guest for 60")
    assert offer is not None

    game.execute_action(host, "offer_trade", input_value=offer)
    assert game.pending_trade_offer is not None

    guest.cash = 0
    game.execute_action(guest, "accept_trade")

    assert game.pending_trade_offer is None
    assert game.property_owners["baltic_avenue"] == host.id
    assert host.cash == STARTING_CASH


def test_monopoly_bot_accepts_favorable_pending_trade_offer():
    game = _start_two_player_game()
    host = game.players[0]
    guest = game.players[1]

    guest.owned_space_ids.append("mediterranean_avenue")
    game.property_owners["mediterranean_avenue"] = guest.id
    game.pending_trade_offer = MonopolyTradeOffer(
        proposer_id=host.id,
        target_id=guest.id,
        give_cash=200,
        receive_property_id="mediterranean_avenue",
        summary="Buy Mediterranean Avenue from Guest for 200",
    )

    assert game.bot_think(guest) == "accept_trade"


def test_monopoly_bot_declines_unfavorable_pending_trade_offer():
    game = _start_two_player_game()
    host = game.players[0]
    guest = game.players[1]

    guest.owned_space_ids.append("boardwalk")
    game.property_owners["boardwalk"] = guest.id
    game.pending_trade_offer = MonopolyTradeOffer(
        proposer_id=host.id,
        target_id=guest.id,
        give_cash=50,
        receive_property_id="boardwalk",
        summary="Buy Boardwalk from Guest for 50",
    )

    assert game.bot_think(guest) == "decline_trade"


def test_monopoly_bot_builds_when_cash_rich_and_build_options_exist():
    game = _start_two_player_game()
    host = game.current_player
    assert host is not None

    for space_id in ("mediterranean_avenue", "baltic_avenue"):
        host.owned_space_ids.append(space_id)
        game.property_owners[space_id] = host.id
    host.cash = 1000
    game.turn_has_rolled = False
    game.turn_pending_purchase_space_id = ""

    assert game.bot_think(host) == "build_house"


def test_monopoly_build_house_obeys_even_building_rules():
    game = _start_two_player_game()
    host = game.current_player
    assert host is not None

    for space_id in ("mediterranean_avenue", "baltic_avenue"):
        host.owned_space_ids.append(space_id)
        game.property_owners[space_id] = host.id

    house_cost = SPACE_BY_ID["mediterranean_avenue"].house_cost
    starting_cash = host.cash

    game.execute_action(host, "build_house", input_value="mediterranean_avenue")
    assert game._building_level("mediterranean_avenue") == 1
    assert game._building_level("baltic_avenue") == 0
    assert host.cash == starting_cash - house_cost

    # Cannot build a second level on the same property before the group is even.
    game.execute_action(host, "build_house", input_value="mediterranean_avenue")
    assert game._building_level("mediterranean_avenue") == 1
    assert host.cash == starting_cash - house_cost

    game.execute_action(host, "build_house", input_value="baltic_avenue")
    assert game._building_level("baltic_avenue") == 1
    assert host.cash == starting_cash - (house_cost * 2)


def test_monopoly_sell_house_obeys_even_selling_rules():
    game = _start_two_player_game()
    host = game.current_player
    assert host is not None

    for space_id in ("mediterranean_avenue", "baltic_avenue"):
        host.owned_space_ids.append(space_id)
        game.property_owners[space_id] = host.id

    game._set_building_level("mediterranean_avenue", 2)
    game._set_building_level("baltic_avenue", 1)
    sell_value = SPACE_BY_ID["mediterranean_avenue"].house_cost // 2
    starting_cash = host.cash

    # Cannot sell from the lower property while another in the group is higher.
    game.execute_action(host, "sell_house", input_value="baltic_avenue")
    assert game._building_level("mediterranean_avenue") == 2
    assert game._building_level("baltic_avenue") == 1
    assert host.cash == starting_cash

    game.execute_action(host, "sell_house", input_value="mediterranean_avenue")
    assert game._building_level("mediterranean_avenue") == 1
    assert game._building_level("baltic_avenue") == 1
    assert host.cash == starting_cash + sell_value


def test_monopoly_house_supply_limit_blocks_new_house_builds():
    game = _start_two_player_game()
    host = game.current_player
    assert host is not None

    for space_id in ("mediterranean_avenue", "baltic_avenue"):
        host.owned_space_ids.append(space_id)
        game.property_owners[space_id] = host.id

    crowded_ids = [
        space_id
        for space_id in sorted(game.building_levels)
        if space_id not in {"mediterranean_avenue", "baltic_avenue"}
    ][:16]
    for space_id in crowded_ids:
        game._set_building_level(space_id, 2)

    assert game._available_houses() == 0
    assert game._options_for_build_house(host) == []

    game.execute_action(host, "build_house", input_value="mediterranean_avenue")
    assert game._building_level("mediterranean_avenue") == 0
    assert host.cash == STARTING_CASH


def test_monopoly_hotel_supply_limit_blocks_hotel_upgrade():
    game = _start_two_player_game()
    host = game.current_player
    assert host is not None

    for space_id in ("mediterranean_avenue", "baltic_avenue"):
        host.owned_space_ids.append(space_id)
        game.property_owners[space_id] = host.id
        game._set_building_level(space_id, 4)

    hotel_locked_ids = [
        space_id
        for space_id in sorted(game.building_levels)
        if space_id not in {"mediterranean_avenue", "baltic_avenue"}
    ][:12]
    for space_id in hotel_locked_ids:
        game._set_building_level(space_id, 5)

    assert game._available_hotels() == 0
    assert game._options_for_build_house(host) == []

    game.execute_action(host, "build_house", input_value="mediterranean_avenue")
    assert game._building_level("mediterranean_avenue") == 4
    assert host.cash == STARTING_CASH


def test_monopoly_liquidation_sells_buildings_before_mortgage_for_bank_debt(monkeypatch):
    game = _start_two_player_game()
    guest = game.players[1]

    for space_id in ("mediterranean_avenue", "baltic_avenue"):
        guest.owned_space_ids.append(space_id)
        game.property_owners[space_id] = guest.id
    game._set_building_level("mediterranean_avenue", 1)

    guest.cash = 30
    guest.position = 35
    game.current_player = guest
    game.turn_has_rolled = False
    game.turn_pending_purchase_space_id = ""

    rolls = iter([1, 2])  # total = 3 -> Luxury Tax (100)
    monkeypatch.setattr("server.games.monopoly.game.random.randint", lambda a, b: next(rolls))
    game.execute_action(guest, "roll_dice")

    assert guest.bankrupt is False
    assert game._building_level("mediterranean_avenue") == 0
    assert set(game.mortgaged_space_ids) == {"mediterranean_avenue", "baltic_avenue"}
    assert guest.cash == 15


def test_monopoly_cannot_mortgage_color_group_with_buildings():
    game = _start_two_player_game()
    host = game.current_player
    assert host is not None

    for space_id in ("mediterranean_avenue", "baltic_avenue"):
        host.owned_space_ids.append(space_id)
        game.property_owners[space_id] = host.id
    game._set_building_level("mediterranean_avenue", 1)

    assert game._options_for_mortgage_property(host) == []
    game.execute_action(host, "mortgage_property", input_value="mediterranean_avenue")
    assert game.mortgaged_space_ids == []
    assert host.cash == STARTING_CASH


def test_monopoly_mortgaged_property_charges_no_rent(monkeypatch):
    game = _start_two_player_game()
    host = game.current_player
    assert host is not None
    guest = game.players[1]

    host.owned_space_ids.append("baltic_avenue")
    game.property_owners["baltic_avenue"] = host.id
    game.mortgaged_space_ids.append("baltic_avenue")
    game.execute_action(host, "end_turn")

    rolls = iter([1, 2])  # guest to Baltic
    monkeypatch.setattr("server.games.monopoly.game.random.randint", lambda a, b: next(rolls))
    game.execute_action(guest, "roll_dice")

    assert host.cash == STARTING_CASH
    assert guest.cash == STARTING_CASH


def test_monopoly_color_set_doubles_base_rent(monkeypatch):
    game = _start_two_player_game()
    host = game.current_player
    assert host is not None
    guest = game.players[1]

    for space_id in ("mediterranean_avenue", "baltic_avenue"):
        host.owned_space_ids.append(space_id)
        game.property_owners[space_id] = host.id

    game.current_player = guest
    game.turn_has_rolled = False
    game.turn_pending_purchase_space_id = ""

    rolls = iter([1, 2])  # guest to Baltic
    monkeypatch.setattr("server.games.monopoly.game.random.randint", lambda a, b: next(rolls))
    game.execute_action(guest, "roll_dice")

    assert host.cash == STARTING_CASH + 8
    assert guest.cash == STARTING_CASH - 8


def test_monopoly_house_rent_table_applies(monkeypatch):
    game = _start_two_player_game()
    host = game.current_player
    assert host is not None
    guest = game.players[1]

    for space_id in ("mediterranean_avenue", "baltic_avenue"):
        host.owned_space_ids.append(space_id)
        game.property_owners[space_id] = host.id
    game._set_building_level("baltic_avenue", 3)

    game.current_player = guest
    game.turn_has_rolled = False
    game.turn_pending_purchase_space_id = ""

    rolls = iter([1, 2])  # guest to Baltic, 3 houses => 180
    monkeypatch.setattr("server.games.monopoly.game.random.randint", lambda a, b: next(rolls))
    game.execute_action(guest, "roll_dice")

    assert host.cash == STARTING_CASH + 180
    assert guest.cash == STARTING_CASH - 180


def test_monopoly_railroad_rent_scales_with_owned_count(monkeypatch):
    game = _start_two_player_game()
    host = game.current_player
    assert host is not None
    guest = game.players[1]

    for space_id in ("reading_railroad", "bo_railroad"):
        host.owned_space_ids.append(space_id)
        game.property_owners[space_id] = host.id

    game.current_player = guest
    game.turn_has_rolled = False
    game.turn_pending_purchase_space_id = ""

    rolls = iter([2, 3])  # guest to Reading Railroad
    monkeypatch.setattr("server.games.monopoly.game.random.randint", lambda a, b: next(rolls))
    game.execute_action(guest, "roll_dice")

    assert host.cash == STARTING_CASH + 50
    assert guest.cash == STARTING_CASH - 50


def test_monopoly_utility_rent_uses_roll_total(monkeypatch):
    game = _start_two_player_game()
    host = game.current_player
    assert host is not None
    guest = game.players[1]

    host.owned_space_ids.append("electric_company")
    game.property_owners["electric_company"] = host.id

    game.current_player = guest
    game.turn_has_rolled = False
    game.turn_pending_purchase_space_id = ""
    guest.position = 10

    rolls = iter([1, 1])  # total 2 -> Electric Company
    monkeypatch.setattr("server.games.monopoly.game.random.randint", lambda a, b: next(rolls))
    game.execute_action(guest, "roll_dice")

    assert host.cash == STARTING_CASH + 8
    assert guest.cash == STARTING_CASH - 8


def test_monopoly_two_utilities_charge_higher_multiplier(monkeypatch):
    game = _start_two_player_game()
    host = game.current_player
    assert host is not None
    guest = game.players[1]

    for space_id in ("electric_company", "water_works"):
        host.owned_space_ids.append(space_id)
        game.property_owners[space_id] = host.id

    game.current_player = guest
    game.turn_has_rolled = False
    game.turn_pending_purchase_space_id = ""
    guest.position = 10

    rolls = iter([1, 1])  # total 2 -> Electric Company
    monkeypatch.setattr("server.games.monopoly.game.random.randint", lambda a, b: next(rolls))
    game.execute_action(guest, "roll_dice")

    assert host.cash == STARTING_CASH + 20
    assert guest.cash == STARTING_CASH - 20
