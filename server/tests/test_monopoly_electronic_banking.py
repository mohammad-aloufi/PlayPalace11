"""Integration tests for Monopoly electronic banking preset behavior."""

from server.game_utils.actions import Visibility
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


def test_electronic_banking_on_start_initializes_bank_accounts():
    game = _start_two_player_game(MonopolyOptions(preset_id="electronic_banking"))
    assert game.banking_profile is not None
    assert game.banking_state is not None
    for player in game.players:
        assert game._bank_balance(player) == 1500


def test_electronic_banking_rent_uses_simulator_transfer(monkeypatch):
    game = _start_two_player_game(MonopolyOptions(preset_id="electronic_banking"))
    host = game.current_player
    assert host is not None

    rolls = iter([1, 2, 1, 2])  # Host buys Baltic, guest lands and pays rent.
    monkeypatch.setattr("server.games.monopoly.game.random.randint", lambda a, b: next(rolls))

    game.execute_action(host, "roll_dice")
    game.execute_action(host, "buy_property")
    game.execute_action(host, "end_turn")

    guest = game.current_player
    assert guest is not None
    game.execute_action(guest, "roll_dice")

    assert game._bank_balance(host) == 1444
    assert game._bank_balance(guest) == 1496
    assert game.banking_state is not None
    assert any(
        tx.reason == "rent:baltic_avenue" and tx.status == "success"
        for tx in game.banking_state.ledger
    )


def test_electronic_banking_tax_uses_simulator_debit(monkeypatch):
    game = _start_two_player_game(MonopolyOptions(preset_id="electronic_banking"))
    host = game.current_player
    assert host is not None

    rolls = iter([2, 2])  # Income Tax.
    monkeypatch.setattr("server.games.monopoly.game.random.randint", lambda a, b: next(rolls))

    game.execute_action(host, "roll_dice")

    assert game._bank_balance(host) == 1300
    assert game.banking_state is not None
    assert any(
        tx.reason == "tax:Income Tax" and tx.status == "success"
        for tx in game.banking_state.ledger
    )


def test_electronic_banking_pass_go_uses_simulator_credit(monkeypatch):
    game = _start_two_player_game(MonopolyOptions(preset_id="electronic_banking"))
    host = game.current_player
    assert host is not None
    host.position = 39

    rolls = iter([1, 1])
    monkeypatch.setattr("server.games.monopoly.game.random.randint", lambda a, b: next(rolls))
    game.execute_action(host, "roll_dice")

    assert game._bank_balance(host) == 1700
    assert game.banking_state is not None
    assert any(tx.reason == "pass_go" and tx.status == "success" for tx in game.banking_state.ledger)


def test_electronic_banking_actions_visible_only_in_preset():
    eb = _start_two_player_game(MonopolyOptions(preset_id="electronic_banking"))
    cl = _start_two_player_game(MonopolyOptions(preset_id="classic_standard"))
    host_eb = eb.current_player
    host_cl = cl.current_player
    assert host_eb is not None
    assert host_cl is not None

    assert eb._is_banking_balance_hidden(host_eb) != Visibility.HIDDEN
    assert eb._is_banking_ledger_hidden(host_eb) != Visibility.HIDDEN
    assert cl._is_banking_balance_hidden(host_cl) == Visibility.HIDDEN
    assert cl._is_banking_ledger_hidden(host_cl) == Visibility.HIDDEN


def test_electronic_banking_manual_transfer_updates_balances():
    game = _start_two_player_game(MonopolyOptions(preset_id="electronic_banking"))
    host = game.current_player
    assert host is not None
    guest = game.players[1]

    option = next(
        opt
        for opt in game._options_for_banking_transfer(host)
        if "target=" + guest.id in opt and "amount=10" in opt
    )
    game.execute_action(host, "banking_transfer", input_value=option)

    assert game._bank_balance(host) == 1490
    assert game._bank_balance(guest) == 1510
    assert game.banking_state is not None
    assert game.banking_state.ledger[-1].reason == "manual_transfer"


def test_electronic_banking_bot_uses_bank_balance_for_buy_decision():
    game = _start_two_player_game(MonopolyOptions(preset_id="electronic_banking"))
    host = game.current_player
    assert host is not None
    host.is_bot = True
    host.cash = 1500  # Intentionally stale mirror value.
    game.turn_has_rolled = True
    game.turn_pending_purchase_space_id = "baltic_avenue"
    assert game.banking_state is not None
    game.banking_state.accounts[host.id].balance = 100

    assert game.bot_think(host) == "auction_property"
