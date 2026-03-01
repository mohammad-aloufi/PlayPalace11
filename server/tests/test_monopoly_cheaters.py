"""Integration tests for Monopoly cheaters preset behavior."""

from server.games.monopoly.cheaters_engine import CheaterOutcome
from server.games.monopoly.game import MonopolyGame, MonopolyOptions
from server.core.users.test_user import MockUser


def _create_two_player_game(options: MonopolyOptions | None = None) -> MonopolyGame:
    game = MonopolyGame(options=options or MonopolyOptions())
    host_user = MockUser("Host")
    guest_user = MockUser("Guest")
    game.add_player("Host", host_user)
    game.add_player("Guest", guest_user)
    game.host = "Host"
    return game


def _start_two_player_game(options: MonopolyOptions | None = None) -> MonopolyGame:
    game = _create_two_player_game(options)
    game.on_start()
    return game


def test_cheaters_on_start_initializes_profile_and_engine():
    game = _start_two_player_game(MonopolyOptions(preset_id="cheaters"))
    assert game.cheaters_profile is not None
    assert game.cheaters_engine is not None
    assert game.cheaters_profile.anchor_edition_id == "monopoly-e4888"


def test_cheaters_blocks_end_turn_before_roll_and_applies_penalty():
    game = _start_two_player_game(MonopolyOptions(preset_id="cheaters"))
    host = game.current_player
    assert host is not None
    starting = host.cash

    game.execute_action(host, "end_turn")

    assert game.current_player is host
    assert host.cash < starting


def test_cheaters_payment_violation_triggers_penalty(monkeypatch):
    game = _start_two_player_game(MonopolyOptions(preset_id="cheaters"))
    host = game.current_player
    assert host is not None
    assert game.cheaters_engine is not None

    observed_required: list[tuple[str, int]] = []
    observed_result: list[tuple[int, int]] = []

    def fake_on_payment_required(
        player_id: str,
        reason: str,
        amount: int,
        context: dict | None = None,
    ) -> CheaterOutcome:
        _ = (player_id, context)
        observed_required.append((reason, amount))
        return CheaterOutcome(status="allow")

    def fake_on_payment_result(
        player_id: str,
        paid: int,
        required: int,
        context: dict | None = None,
    ) -> CheaterOutcome:
        _ = (player_id, context)
        observed_result.append((paid, required))
        return CheaterOutcome(
            status="penalty",
            cash_delta=-100,
            message_key="monopoly-cheaters-payment-avoidance-blocked",
            reason_code="payment_avoidance",
        )

    monkeypatch.setattr(game.cheaters_engine, "on_payment_required", fake_on_payment_required)
    monkeypatch.setattr(game.cheaters_engine, "on_payment_result", fake_on_payment_result)

    rolls = iter([1, 2, 1, 2])  # host buys Baltic, guest pays rent on Baltic
    monkeypatch.setattr("server.games.monopoly.game.random.randint", lambda a, b: next(rolls))

    game.execute_action(host, "roll_dice")
    game.execute_action(host, "buy_property")
    game.execute_action(host, "end_turn")

    guest = game.current_player
    assert guest is not None
    game.execute_action(guest, "roll_dice")

    assert observed_required
    assert observed_result
    assert guest.cash == 1396


def test_cheaters_claim_reward_action_credits_cash_once_per_turn():
    game = _start_two_player_game(MonopolyOptions(preset_id="cheaters"))
    host = game.current_player
    assert host is not None

    starting = host.cash
    game.execute_action(host, "claim_cheat_reward")
    after_first = host.cash
    game.execute_action(host, "claim_cheat_reward")

    assert game.current_player is host
    assert after_first == starting + 100
    assert host.cash == after_first
