"""Handler helpers for Monopoly turn actions."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ....game_utils.bot_helper import BotHelper
from ...base import Player
from ..voice_commands import parse_voice_command

if TYPE_CHECKING:
    from ..game import MonopolyGame


def _game_randint(low: int, high: int) -> int:
    """Use Monopoly game-module RNG so existing monkeypatches keep working."""
    from .. import game as monopoly_game_module

    return monopoly_game_module.random.randint(low, high)


def action_banking_balance(game: MonopolyGame, player: Player, action_id: str) -> None:
    """Announce current electronic bank balance to the requesting player."""
    _ = action_id
    if not game._is_electronic_banking_preset():
        return
    mono_player = player  # type: ignore[assignment]
    user = game.get_user(player)
    if user:
        user.speak_l(
            "monopoly-banking-balance-report",
            player=mono_player.name,
            cash=game._bank_balance(mono_player),
        )


def action_banking_transfer(game: MonopolyGame, player: Player, option: str, action_id: str) -> None:
    """Execute one manual bank transfer between players."""
    _ = action_id
    if not game._is_electronic_banking_preset() or game.banking_state is None:
        return
    mono_player = player  # type: ignore[assignment]
    if option not in game._options_for_banking_transfer(player):
        return
    parsed = game._parse_banking_transfer_option(option)
    if not parsed:
        return

    target_id, amount = parsed
    target = game.get_player_by_id(target_id)
    if not target or target.bankrupt:
        return

    transferred = game._transfer_between_players(
        mono_player,
        target,
        amount,
        "manual_transfer",
    )
    if transferred == amount:
        game.broadcast_l(
            "monopoly-banking-transfer-success",
            from_player=mono_player.name,
            to_player=target.name,
            amount=transferred,
        )
    else:
        game.broadcast_l(
            "monopoly-banking-transfer-failed",
            player=mono_player.name,
            reason="insufficient_funds",
        )

    game._sync_cash_scores()
    game.rebuild_all_menus()


def action_banking_ledger(game: MonopolyGame, player: Player, action_id: str) -> None:
    """Announce recent banking ledger events to the requesting player."""
    _ = action_id
    user = game.get_user(player)
    if not user:
        return
    if not game._is_electronic_banking_preset() or game.banking_state is None:
        return

    entries: list[str] = []
    for tx in game.banking_state.ledger[-5:]:
        if tx.status == "success":
            entries.append(
                f"{tx.tx_id} {tx.kind} {tx.from_id}->{tx.to_id} {tx.amount} ({tx.reason})"
            )
        else:
            entries.append(
                f"{tx.tx_id} {tx.kind} failed ({tx.failure_reason or 'unknown'})"
            )

    if not entries:
        user.speak_l("monopoly-banking-ledger-empty")
        return
    user.speak_l("monopoly-banking-ledger-report", entries=" | ".join(entries))


def action_voice_command(game: MonopolyGame, player: Player, text: str, action_id: str) -> None:
    """Parse and execute one voice-style command in voice banking preset."""
    if game.active_preset_id != "voice_banking":
        return
    mono_player = player  # type: ignore[assignment]
    parsed = parse_voice_command(text)

    user = game.get_user(player)
    if parsed.error:
        game.voice_last_response_by_player_id[mono_player.id] = parsed.error
        if user:
            user.speak_l("monopoly-voice-command-error", reason=parsed.error)
        return

    if parsed.intent == "check_balance":
        game.voice_last_response_by_player_id[mono_player.id] = parsed.intent
        if user:
            user.speak_l(
                "monopoly-banking-balance-report",
                player=mono_player.name,
                cash=game._bank_balance(mono_player),
            )
        return

    if parsed.intent == "show_recent_ledger":
        game.voice_last_response_by_player_id[mono_player.id] = parsed.intent
        action_banking_ledger(game, player, action_id)
        return

    if parsed.intent == "repeat_last_bank_result":
        previous = game.voice_last_response_by_player_id.get(mono_player.id, "none")
        game.voice_last_response_by_player_id[mono_player.id] = parsed.intent
        if user:
            user.speak_l("monopoly-voice-command-repeat", response=previous)
        return

    if parsed.intent == "transfer_amount_to_player":
        target = None
        wanted_name = parsed.target_name.strip().lower()
        for turn_player in game.turn_players:
            if turn_player.id == mono_player.id or turn_player.bankrupt:
                continue
            if turn_player.name.lower() == wanted_name:
                target = turn_player
                break

        if target is None:
            game.voice_last_response_by_player_id[mono_player.id] = "invalid_target"
            if user:
                user.speak_l("monopoly-voice-command-error", reason="invalid_target")
            return

        game.voice_pending_transfer_by_player_id[mono_player.id] = (target.id, parsed.amount)
        game.voice_last_response_by_player_id[mono_player.id] = "transfer_pending_confirm"
        if user:
            user.speak_l(
                "monopoly-voice-transfer-staged",
                amount=parsed.amount,
                target=target.name,
            )
        return

    if parsed.intent == "confirm_transfer":
        pending = game.voice_pending_transfer_by_player_id.get(mono_player.id)
        if not pending:
            game.voice_last_response_by_player_id[mono_player.id] = "no_pending_transfer"
            if user:
                user.speak_l("monopoly-voice-command-error", reason="no_pending_transfer")
            return

        target_id, amount = pending
        target = game.get_player_by_id(target_id)
        if not target or target.bankrupt:
            game.voice_pending_transfer_by_player_id.pop(mono_player.id, None)
            game.voice_last_response_by_player_id[mono_player.id] = "invalid_target"
            if user:
                user.speak_l("monopoly-voice-command-error", reason="invalid_target")
            return

        transferred = game._transfer_between_players(
            mono_player,
            target,
            amount,
            "voice_transfer",
        )
        game.voice_pending_transfer_by_player_id.pop(mono_player.id, None)
        if transferred == amount:
            game.voice_last_response_by_player_id[mono_player.id] = "transfer_confirmed"
            game.broadcast_l(
                "monopoly-banking-transfer-success",
                from_player=mono_player.name,
                to_player=target.name,
                amount=transferred,
            )
            game._sync_cash_scores()
            game.rebuild_all_menus()
        else:
            game.voice_last_response_by_player_id[mono_player.id] = "insufficient_funds"
            if user:
                user.speak_l("monopoly-voice-command-error", reason="insufficient_funds")
        return

    game.voice_last_response_by_player_id[mono_player.id] = parsed.intent
    if user:
        user.speak_l("monopoly-voice-command-accepted", intent=parsed.intent)


def action_auction_property(game: MonopolyGame, player: Player, action_id: str) -> None:
    """Start an interactive auction for the pending unpurchased property."""
    _ = action_id
    mono_player = player  # type: ignore[assignment]
    if game._is_auction_active():
        return
    space = game._pending_purchase_space()
    if not space:
        return

    game._start_property_auction(space, mono_player)


def action_auction_bid(game: MonopolyGame, player: Player, option: str, action_id: str) -> None:
    """Place a bid in the active interactive auction."""
    _ = action_id
    if not game._is_auction_active():
        return
    current_bidder = game._current_auction_bidder()
    if current_bidder is None or current_bidder.id != player.id:
        return
    if option not in game._options_for_auction_bid(player):
        return
    space = game._pending_auction_space()
    if not space:
        return

    try:
        bid = int(option)
    except ValueError:
        return

    min_bid = game._auction_min_bid()
    if bid < min_bid or bid > game._current_liquid_balance(current_bidder):
        return

    game.pending_auction_current_bid = bid
    game.pending_auction_high_bidder_id = current_bidder.id
    game.broadcast_l(
        "monopoly-auction-bid-placed",
        player=current_bidder.name,
        property=space.name,
        amount=bid,
    )

    current_index = game.pending_auction_turn_index % len(game.pending_auction_bidder_ids)
    game._advance_pending_auction_turn(current_index)
    if game._is_auction_active():
        game.rebuild_all_menus()


def action_auction_pass(game: MonopolyGame, player: Player, action_id: str) -> None:
    """Pass on bidding in the active interactive auction."""
    _ = action_id
    if not game._is_auction_active():
        return
    current_bidder = game._current_auction_bidder()
    if current_bidder is None or current_bidder.id != player.id:
        return
    if player.id not in game.pending_auction_bidder_ids:
        return

    space = game._pending_auction_space()
    if not space:
        game._finish_pending_auction()
        return

    current_index = game.pending_auction_bidder_ids.index(player.id)
    game.pending_auction_bidder_ids.remove(player.id)
    if game.pending_auction_high_bidder_id == player.id:
        game.pending_auction_high_bidder_id = ""
        game.pending_auction_current_bid = 0
    game.broadcast_l(
        "monopoly-auction-pass-event",
        player=current_bidder.name,
        property=space.name,
    )

    game._advance_pending_auction_turn(current_index - 1)
    if game._is_auction_active():
        game.rebuild_all_menus()


def action_mortgage_property(
    game: MonopolyGame, player: Player, space_id: str, action_id: str
) -> None:
    """Mortgage one owned property to raise cash."""
    _ = action_id
    if game._is_junior_preset():
        return
    mono_player = player  # type: ignore[assignment]
    if space_id not in game._options_for_mortgage_property(player):
        return
    space = game.active_space_by_id.get(space_id)
    if not space:
        return

    value = game._mortgage_value(space)
    credited = game._credit_player(mono_player, value, f"mortgage:{space.space_id}")
    if credited <= 0:
        return
    game.mortgaged_space_ids.append(space_id)
    game.broadcast_l(
        "monopoly-property-mortgaged",
        player=mono_player.name,
        property=space.name,
        amount=credited,
        cash=mono_player.cash,
    )

    game._sync_cash_scores()
    game.rebuild_all_menus()


def action_unmortgage_property(
    game: MonopolyGame, player: Player, space_id: str, action_id: str
) -> None:
    """Unmortgage one owned property."""
    _ = action_id
    if game._is_junior_preset():
        return
    mono_player = player  # type: ignore[assignment]
    if space_id not in game._options_for_unmortgage_property(player):
        return
    space = game.active_space_by_id.get(space_id)
    if not space:
        return

    cost = game._unmortgage_cost(space)
    if game._current_liquid_balance(mono_player) < cost:
        return
    paid = game._debit_player_to_bank(mono_player, cost, f"unmortgage:{space.space_id}")
    if paid < cost:
        return
    game.mortgaged_space_ids.remove(space_id)
    game.broadcast_l(
        "monopoly-property-unmortgaged",
        player=mono_player.name,
        property=space.name,
        amount=paid,
        cash=mono_player.cash,
    )

    game._sync_cash_scores()
    game.rebuild_all_menus()


def action_build_house(game: MonopolyGame, player: Player, space_id: str, action_id: str) -> None:
    """Build one house/hotel on an owned eligible street property."""
    _ = action_id
    if game._is_junior_preset():
        return
    mono_player = player  # type: ignore[assignment]
    if space_id not in game._options_for_build_house(player):
        return
    space = game.active_space_by_id.get(space_id)
    if not space or not game._is_street_property(space):
        return

    cost = max(0, space.house_cost)
    if game._current_liquid_balance(mono_player) < cost:
        return
    if game.rule_profile.builder_block_required_for_build and mono_player.builder_blocks <= 0:
        return

    if not game._can_raise_building_level(space_id):
        return
    paid = game._debit_player_to_bank(mono_player, cost, f"build:{space.space_id}")
    if paid < cost:
        return
    new_level = game._building_level(space_id) + 1
    game._set_building_level(space_id, new_level)
    if game.rule_profile.builder_block_required_for_build:
        mono_player.builder_blocks -= 1
        game.broadcast_l(
            "monopoly-builder-block-spent",
            player=mono_player.name,
            blocks=mono_player.builder_blocks,
        )
    game.broadcast_l(
        "monopoly-house-built",
        player=mono_player.name,
        property=space.name,
        amount=paid,
        level=new_level,
        cash=mono_player.cash,
    )

    game._sync_cash_scores()
    game.rebuild_all_menus()


def action_sell_house(game: MonopolyGame, player: Player, space_id: str, action_id: str) -> None:
    """Sell one house/hotel from an owned eligible street property."""
    _ = action_id
    if game._is_junior_preset():
        return
    mono_player = player  # type: ignore[assignment]
    if space_id not in game._options_for_sell_house(player):
        return
    space = game.active_space_by_id.get(space_id)
    if not space or not game._is_street_property(space):
        return

    current_level = game._building_level(space_id)
    if current_level <= 0:
        return
    if not game._can_lower_building_level(space_id):
        return

    value = max(0, space.house_cost // 2)
    game._set_building_level(space_id, current_level - 1)
    new_level = game._building_level(space_id)
    credited = game._credit_player(mono_player, value, f"sell_building:{space.space_id}")
    game.broadcast_l(
        "monopoly-house-sold",
        player=mono_player.name,
        property=space.name,
        amount=credited,
        level=new_level,
        cash=mono_player.cash,
    )

    game._sync_cash_scores()
    game.rebuild_all_menus()


def action_offer_trade(game: MonopolyGame, player: Player, option: str, action_id: str) -> None:
    """Create a pending trade offer for another player."""
    _ = action_id
    if game._is_junior_preset():
        return
    mono_player = player  # type: ignore[assignment]
    if game.pending_trade_offer is not None:
        return
    if option not in game._options_for_offer_trade(player):
        return
    parsed = game._parse_trade_option(option)
    if not parsed:
        return

    target = game.get_player_by_id(parsed.target_id)
    if not target or not isinstance(target, type(mono_player)):
        return
    parsed.proposer_id = mono_player.id
    if not game._is_trade_offer_valid(mono_player, target, parsed):
        return

    game.pending_trade_offer = parsed
    game.broadcast_l(
        "monopoly-trade-offered",
        proposer=mono_player.name,
        target=target.name,
        offer=parsed.summary,
    )

    if target.is_bot:
        if game._bot_accepts_trade_offer(mono_player, target, parsed) and game._apply_trade_offer(
            mono_player, target, parsed
        ):
            game.broadcast_l(
                "monopoly-trade-completed",
                proposer=mono_player.name,
                target=target.name,
                offer=parsed.summary,
            )
        else:
            game.broadcast_l(
                "monopoly-trade-declined",
                proposer=mono_player.name,
                target=target.name,
                offer=parsed.summary,
            )
        game.pending_trade_offer = None

    game._sync_cash_scores()
    game.rebuild_all_menus()


def action_accept_trade(game: MonopolyGame, player: Player, action_id: str) -> None:
    """Accept the currently pending trade for this player."""
    _ = action_id
    if game._is_junior_preset():
        return
    mono_player = player  # type: ignore[assignment]
    offer = game._pending_trade_for_target(mono_player)
    if offer is None:
        return
    proposer = game.get_player_by_id(offer.proposer_id)
    if not proposer or not isinstance(proposer, type(mono_player)):
        game.pending_trade_offer = None
        game.rebuild_all_menus()
        return

    if not game._apply_trade_offer(proposer, mono_player, offer):
        game.broadcast_l(
            "monopoly-trade-cancelled",
            offer=offer.summary,
        )
        game.pending_trade_offer = None
        game._sync_cash_scores()
        game.rebuild_all_menus()
        return

    game.broadcast_l(
        "monopoly-trade-completed",
        proposer=proposer.name,
        target=mono_player.name,
        offer=offer.summary,
    )
    game.pending_trade_offer = None
    game._sync_cash_scores()
    game.rebuild_all_menus()


def action_decline_trade(game: MonopolyGame, player: Player, action_id: str) -> None:
    """Decline the currently pending trade for this player."""
    _ = action_id
    if game._is_junior_preset():
        return
    mono_player = player  # type: ignore[assignment]
    offer = game._pending_trade_for_target(mono_player)
    if offer is None:
        return
    proposer = game.get_player_by_id(offer.proposer_id)
    proposer_name = proposer.name if proposer and isinstance(proposer, type(mono_player)) else "Unknown"
    game.broadcast_l(
        "monopoly-trade-declined",
        proposer=proposer_name,
        target=mono_player.name,
        offer=offer.summary,
    )
    game.pending_trade_offer = None
    game.rebuild_all_menus()


def action_pay_bail(game: MonopolyGame, player: Player, action_id: str) -> None:
    """Pay bail to leave jail before rolling."""
    _ = action_id
    mono_player = player  # type: ignore[assignment]
    bail_amount = game._bail_amount()
    if (
        not mono_player.in_jail
        or game.turn_has_rolled
        or game._current_liquid_balance(mono_player) < bail_amount
    ):
        return

    paid = game._debit_player_to_bank(mono_player, bail_amount, "pay_bail")
    if paid < bail_amount:
        return
    mono_player.in_jail = False
    mono_player.jail_turns = 0
    game.broadcast_l(
        "monopoly-bail-paid",
        player=mono_player.name,
        amount=paid,
        cash=mono_player.cash,
    )
    game._apply_sore_loser_rebate(mono_player, paid)

    game._sync_cash_scores()
    game.rebuild_all_menus()


def action_use_jail_card(game: MonopolyGame, player: Player, action_id: str) -> None:
    """Use a get-out-of-jail-free card."""
    _ = action_id
    mono_player = player  # type: ignore[assignment]
    if not mono_player.in_jail or game.turn_has_rolled or mono_player.get_out_of_jail_cards <= 0:
        return

    mono_player.get_out_of_jail_cards -= 1
    mono_player.in_jail = False
    mono_player.jail_turns = 0
    game.broadcast_l(
        "monopoly-jail-card-used",
        player=mono_player.name,
        cards=mono_player.get_out_of_jail_cards,
    )

    game._sync_cash_scores()
    game.rebuild_all_menus()


def action_claim_cheat_reward(game: MonopolyGame, player: Player, action_id: str) -> None:
    """Apply cheaters reward claim outcome for the active player."""
    _ = action_id
    mono_player = player  # type: ignore[assignment]
    if game.cheaters_engine is None or mono_player.bankrupt:
        return
    outcome = game.cheaters_engine.on_action_attempt(
        mono_player.id,
        "claim_cheat_reward",
        context={"turn_has_rolled": game.turn_has_rolled},
    )
    game._apply_cheaters_outcome(
        mono_player,
        outcome,
        reason="reward_claim",
    )
    game.rebuild_all_menus()


def action_end_turn(game: MonopolyGame, player: Player, action_id: str) -> None:
    """End current player's turn and advance."""
    _ = action_id
    mono_player = player  # type: ignore[assignment]
    game.voice_pending_transfer_by_player_id.pop(player.id, None)
    if game.cheaters_engine is not None and not mono_player.bankrupt:
        outcome = game.cheaters_engine.on_turn_end_attempt(
            mono_player.id,
            context={"turn_has_rolled": game.turn_has_rolled},
        )
        if not game._apply_cheaters_outcome(
            mono_player,
            outcome,
            reason="turn_end",
            block_action_on_penalty=True,
        ):
            game.rebuild_all_menus()
            return
    if game._is_city_preset() and game._check_city_endgame():
        game.rebuild_all_menus()
        return
    if game._is_junior_preset() and game._check_junior_endgame():
        game.rebuild_all_menus()
        return
    game._reset_turn_state()
    next_player = game.advance_turn(announce=True)
    game._start_cheaters_turn(next_player)
    game._start_city_turn(next_player)
    if game._is_city_preset() and game._check_city_endgame():
        game.rebuild_all_menus()
        return
    if game._is_junior_preset() and game._check_junior_endgame():
        game.rebuild_all_menus()
        return
    if next_player and next_player.is_bot:
        BotHelper.jolt_bot(next_player, ticks=_game_randint(8, 14))


def action_roll_dice(game: MonopolyGame, player: Player, action_id: str) -> None:
    """Handle rolling and landing logic for classic scaffold."""
    _ = action_id
    mono_player = player  # type: ignore[assignment]
    bail_amount = game._bail_amount()

    if game.turn_has_rolled or mono_player.bankrupt or game.turn_pending_purchase_space_id:
        return

    if game._is_junior_super_mario_manual_core_active():
        numbered_die = _game_randint(1, 6)
        power_up_die = _game_randint(1, 6)
        die_1 = numbered_die
        die_2 = power_up_die
        total = numbered_die
        is_doubles = False
        game.turn_last_roll = [die_1, die_2]
    elif game._is_junior_preset() and game.junior_ruleset:
        rolls = [_game_randint(1, 6) for _ in range(game.junior_ruleset.dice_count)]
        die_1 = rolls[0]
        die_2 = rolls[1] if len(rolls) > 1 else 0
        total = sum(rolls)
        is_doubles = len(rolls) > 1 and all(value == rolls[0] for value in rolls)
        game.turn_last_roll = rolls
    else:
        die_1 = _game_randint(1, 6)
        die_2 = _game_randint(1, 6)
        total = die_1 + die_2
        is_doubles = die_1 == die_2
        game.turn_last_roll = [die_1, die_2]

    game.turn_has_rolled = True
    game.turn_pending_purchase_space_id = ""
    if mono_player.in_jail:
        if game._is_junior_super_mario_manual_core_active():
            if mono_player.get_out_of_jail_cards > 0:
                mono_player.get_out_of_jail_cards -= 1
                mono_player.in_jail = False
                mono_player.jail_turns = 0
                game.broadcast_l(
                    "monopoly-jail-card-used",
                    player=mono_player.name,
                    cards=mono_player.get_out_of_jail_cards,
                )
            elif game._current_liquid_balance(mono_player) >= 1:
                paid = game._debit_player_to_bank(mono_player, 1, "pay_bail")
                if paid < 1:
                    game.turn_doubles_count = 0
                    game._sync_cash_scores()
                    game.rebuild_all_menus()
                    return
                mono_player.in_jail = False
                mono_player.jail_turns = 0
                game.broadcast_l(
                    "monopoly-bail-paid",
                    player=mono_player.name,
                    amount=paid,
                    cash=mono_player.cash,
                )
            else:
                game.turn_doubles_count = 0
                game._sync_cash_scores()
                game.rebuild_all_menus()
                return

            landed_space = game._move_player(
                mono_player, total, collect_pass_go=False
            )
            game.broadcast_l(
                "monopoly-roll-result",
                player=mono_player.name,
                die1=die_1,
                die2=die_2,
                total=total,
                space=landed_space.name,
            )
            resolution = game._resolve_space(mono_player, landed_space, dice_total=total)
            if not mono_player.bankrupt and resolution == "resolved":
                game._apply_junior_super_mario_powerup(mono_player, die_2)
            game.turn_doubles_count = 0
            game._sync_cash_scores()
            game.rebuild_all_menus()
            return
        if is_doubles:
            mono_player.in_jail = False
            mono_player.jail_turns = 0
            game.broadcast_l(
                "monopoly-jail-roll-doubles",
                player=mono_player.name,
                die1=die_1,
                die2=die_2,
            )
            landed_space = game._move_player(
                mono_player, total, collect_pass_go=False
            )
            game.broadcast_l(
                "monopoly-roll-result",
                player=mono_player.name,
                die1=die_1,
                die2=die_2,
                total=total,
                space=landed_space.name,
            )
            game._resolve_space(mono_player, landed_space, dice_total=total)
        else:
            mono_player.jail_turns += 1
            game.broadcast_l(
                "monopoly-jail-roll-failed",
                player=mono_player.name,
                die1=die_1,
                die2=die_2,
                attempts=mono_player.jail_turns,
            )
            if mono_player.jail_turns >= 3:
                if game._current_liquid_balance(mono_player) < bail_amount:
                    game._liquidate_assets_for_debt(mono_player, bail_amount)
                if game._current_liquid_balance(mono_player) < bail_amount:
                    game._declare_bankrupt(mono_player)
                    game._sync_cash_scores()
                    game.rebuild_all_menus()
                    return
                paid = game._debit_player_to_bank(mono_player, bail_amount, "jail_bail")
                if paid < bail_amount:
                    game._declare_bankrupt(mono_player)
                    game._sync_cash_scores()
                    game.rebuild_all_menus()
                    return
                mono_player.in_jail = False
                mono_player.jail_turns = 0
                game.broadcast_l(
                    "monopoly-bail-paid",
                    player=mono_player.name,
                    amount=paid,
                    cash=mono_player.cash,
                )
                game._apply_sore_loser_rebate(mono_player, paid)
                landed_space = game._move_player(
                    mono_player, total, collect_pass_go=False
                )
                game.broadcast_l(
                    "monopoly-roll-result",
                    player=mono_player.name,
                    die1=die_1,
                    die2=die_2,
                    total=total,
                    space=landed_space.name,
                )
                game._resolve_space(mono_player, landed_space, dice_total=total)
        game.turn_doubles_count = 0
        game._sync_cash_scores()
        game.rebuild_all_menus()
        return

    if game.rule_profile.doubles_grant_extra_roll and is_doubles:
        game.turn_doubles_count += 1
    else:
        game.turn_doubles_count = 0

    if game.rule_profile.doubles_grant_extra_roll and game.turn_doubles_count >= 3:
        game._send_to_jail(mono_player, by_triple_doubles=True)
        game._sync_cash_scores()
        game.rebuild_all_menus()
        return

    landed_space = game._move_player(mono_player, total, collect_pass_go=True)
    game.broadcast_l(
        "monopoly-roll-result",
        player=mono_player.name,
        die1=die_1,
        die2=die_2,
        total=total,
        space=landed_space.name,
    )
    resolution = game._resolve_space(mono_player, landed_space, dice_total=total)
    if game._is_junior_super_mario_manual_core_active() and not mono_player.bankrupt:
        if resolution == "resolved":
            resolution = game._apply_junior_super_mario_powerup(mono_player, die_2)

    if game.rule_profile.doubles_grant_extra_roll and not mono_player.bankrupt and is_doubles:
        if resolution == "resolved":
            game._prepare_next_roll_after_doubles(mono_player)
        elif resolution == "pending_purchase":
            game.turn_can_roll_again = True

    game._sync_cash_scores()
    game.rebuild_all_menus()


def action_buy_property(game: MonopolyGame, player: Player, action_id: str) -> None:
    """Buy currently pending property."""
    _ = action_id
    if not game.rule_profile.allow_manual_property_buy:
        return
    mono_player = player  # type: ignore[assignment]
    space = game._pending_purchase_space()
    if not space:
        return
    if space.space_id in game.property_owners:
        game.turn_pending_purchase_space_id = ""
        return
    if not game._buy_property_for_player(mono_player, space):
        return
    game.turn_pending_purchase_space_id = ""

    if game.turn_can_roll_again:
        game._prepare_next_roll_after_doubles(mono_player)

    game._sync_cash_scores()
    game.rebuild_all_menus()
