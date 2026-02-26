"""Unit tests for Monopoly electronic banking simulator."""

from server.games.monopoly.banking_sim import (
    BankingState,
    ElectronicBankingProfile,
    can_pay,
    credit,
    debit,
    get_balance,
    init_accounts,
    transfer,
)


def _profile(starting_balance: int = 1500) -> ElectronicBankingProfile:
    return ElectronicBankingProfile(
        preset_id="electronic_banking",
        anchor_edition_id="monopoly-00114",
        starting_balance=starting_balance,
    )


def test_init_accounts_creates_balances_for_players():
    state = init_accounts(["p1", "p2"], _profile())
    assert get_balance(state, "p1") == 1500
    assert get_balance(state, "p2") == 1500


def test_transfer_moves_balance_and_records_transaction():
    state = init_accounts(["p1", "p2"], _profile())
    tx = transfer(state, "p1", "p2", 200, "rent")
    assert tx.status == "success"
    assert get_balance(state, "p1") == 1300
    assert get_balance(state, "p2") == 1700
    assert state.ledger[-1].tx_id == tx.tx_id


def test_transfer_fails_without_mutation_on_insufficient_funds():
    state = init_accounts(["p1", "p2"], _profile(starting_balance=100))
    tx = transfer(state, "p1", "p2", 300, "rent")
    assert tx.status == "failed"
    assert tx.failure_reason == "insufficient_funds"
    assert get_balance(state, "p1") == 100
    assert get_balance(state, "p2") == 100


def test_credit_and_debit_update_balances():
    state = init_accounts(["p1"], _profile(starting_balance=100))
    assert can_pay(state, "p1", 100) is True
    assert can_pay(state, "p1", 101) is False

    debit_tx = debit(state, "p1", 25, "fee")
    assert debit_tx.status == "success"
    assert get_balance(state, "p1") == 75

    credit_tx = credit(state, "p1", 10, "bonus")
    assert credit_tx.status == "success"
    assert get_balance(state, "p1") == 85


def test_banking_snapshot_is_stable_for_same_sequence():
    state_a = init_accounts(["p1", "p2"], _profile())
    state_b = init_accounts(["p1", "p2"], _profile())
    transfer(state_a, "p1", "p2", 50, "rent")
    transfer(state_b, "p1", "p2", 50, "rent")
    assert isinstance(state_a, BankingState)
    assert state_a.snapshot() == state_b.snapshot()
