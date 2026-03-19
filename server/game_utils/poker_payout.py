"""Shared pot resolution helpers for poker games."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable, TypeVar

from .poker_pot import PokerPot
from .poker_showdown import order_winners_by_button

TPlayer = TypeVar("TPlayer")


@dataclass
class PokerPotPayoutResult:
    """Resolved payout data for a single main or side pot."""

    pot_index: int
    pot_amount: int
    eligible_player_ids: set[str]
    winners: list[TPlayer]
    best_score: tuple[int, tuple[int, ...]]
    payouts: list[tuple[TPlayer, int]]


def compute_ordered_payouts(
    pot_amount: int,
    ordered_winners: list[TPlayer],
) -> list[tuple[TPlayer, int]]:
    """Split a pot across already ordered winners.

    Odd chips are awarded one at a time in the supplied order.

    Args:
        pot_amount: Total chips in the pot.
        ordered_winners: Winners in odd-chip priority order.

    Returns:
        List of ``(winner, payout)`` tuples in the same order.
    """
    if pot_amount <= 0 or not ordered_winners:
        return []
    share = pot_amount // len(ordered_winners)
    remainder = pot_amount % len(ordered_winners)
    payouts: list[tuple[TPlayer, int]] = []
    for index, winner in enumerate(ordered_winners):
        payout = share + (1 if index < remainder else 0)
        payouts.append((winner, payout))
    return payouts


def resolve_pots_with_payouts(
    pots: Iterable[PokerPot],
    get_player_by_id: Callable[[str], TPlayer | None],
    active_ids: list[str],
    button_id: str | None,
    get_id: Callable[[TPlayer], str],
    score_fn: Callable[[TPlayer], tuple[int, tuple[int, ...]]],
    award_fn: Callable[[TPlayer, int], None] | None = None,
) -> list[PokerPotPayoutResult]:
    """Resolve a sequence of pots and optionally apply payouts.

    Args:
        pots: Main/side pots to resolve.
        get_player_by_id: Lookup from player id to player object.
        active_ids: Active player ids in current hand order.
        button_id: Current dealer/button player id.
        get_id: Callable to extract player id from player object.
        score_fn: Callable returning a comparable hand score tuple.
        award_fn: Optional callback to apply an awarded amount to a winner.

    Returns:
        Resolved payout results for each pot that had at least one eligible winner.
    """
    results: list[PokerPotPayoutResult] = []
    for pot_index, pot in enumerate(pots):
        eligible_players = [get_player_by_id(pid) for pid in pot.eligible_player_ids]
        eligible_players = [player for player in eligible_players if player is not None]
        if not eligible_players:
            continue
        winners, best_score, _share, _remainder = resolve_pot(
            pot.amount,
            eligible_players,
            active_ids,
            button_id,
            get_id,
            score_fn,
        )
        if not winners or not best_score:
            continue
        payouts = compute_ordered_payouts(pot.amount, winners)
        if award_fn:
            for winner, payout in payouts:
                award_fn(winner, payout)
        results.append(
            PokerPotPayoutResult(
                pot_index=pot_index,
                pot_amount=pot.amount,
                eligible_player_ids=set(pot.eligible_player_ids),
                winners=winners,
                best_score=best_score,
                payouts=payouts,
            )
        )
    return results


def resolve_pot(
    pot_amount: int,
    eligible_players: Iterable[TPlayer],
    active_ids: list[str],
    button_id: str | None,
    get_id: Callable[[TPlayer], str],
    score_fn: Callable[[TPlayer], tuple[int, tuple[int, ...]]],
) -> tuple[list[TPlayer], tuple[int, tuple[int, ...]] | None, int, int]:
    """Resolve a single pot and compute payouts.

    Args:
        pot_amount: Total chips in this pot.
        eligible_players: Players eligible to win this pot.
        active_ids: Active player ids in current hand order.
        button_id: Current dealer/button player id.
        get_id: Callable to extract player id from player object.
        score_fn: Callable returning a comparable hand score tuple.

    Returns:
        Tuple of (ordered_winners, best_score, share, remainder).
    """
    best_score = None
    winners: list[TPlayer] = []
    for p in eligible_players:
        score = score_fn(p)
        if best_score is None or score > best_score:
            best_score = score
            winners = [p]
        elif score == best_score:
            winners.append(p)
    if not best_score or not winners:
        return ([], None, 0, 0)
    ordered_winners = order_winners_by_button(winners, active_ids, button_id, get_id)
    share = pot_amount // len(winners)
    remainder = pot_amount % len(winners)
    return (ordered_winners, best_score, share, remainder)
