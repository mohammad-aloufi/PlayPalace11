# Monopoly Electronic Banking Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a maximum-fidelity `electronic_banking` preset powered by a deterministic in-game banking simulator, while keeping all non-electronic presets unchanged.

**Architecture:** Add a dedicated simulator module for accounts and transactions, then bridge Monopoly economy events through this simulator only when `electronic_banking` is active. Keep board/turn flow in `MonopolyGame` and isolate preset-gated behavior to avoid regressions.

**Tech Stack:** Python 3.13, dataclasses, pytest, existing Monopoly game engine (`server/games/monopoly/game.py`), Fluent localization files (`server/locales/*/monopoly.ftl`).

---

### Task 1: Add Failing Contract Tests For Electronic Banking Simulator

**Files:**
- Create: `server/tests/test_monopoly_banking_sim.py`

**Step 1: Write the failing test**

```python
from server.games.monopoly.banking_sim import (
    BankingState,
    ElectronicBankingProfile,
    init_accounts,
    transfer,
    get_balance,
)

def test_init_accounts_creates_balances_for_players():
    profile = ElectronicBankingProfile(
        preset_id="electronic_banking",
        anchor_edition_id="monopoly-00114",
        starting_balance=1500,
    )
    state = init_accounts(["p1", "p2"], profile)
    assert get_balance(state, "p1") == 1500
    assert get_balance(state, "p2") == 1500

def test_transfer_moves_balance_and_records_transaction():
    profile = ElectronicBankingProfile(
        preset_id="electronic_banking",
        anchor_edition_id="monopoly-00114",
        starting_balance=1500,
    )
    state = init_accounts(["p1", "p2"], profile)
    tx = transfer(state, "p1", "p2", 200, "rent")
    assert tx.status == "success"
    assert get_balance(state, "p1") == 1300
    assert get_balance(state, "p2") == 1700
```

**Step 2: Run test to verify it fails**

Run: `cd server && ../.venv/bin/pytest tests/test_monopoly_banking_sim.py -v`
Expected: FAIL because `banking_sim.py` does not exist.

**Step 3: Write minimal implementation**

```python
# create skeleton symbols in banking_sim.py
```

**Step 4: Run test to verify it passes**

Run: same command as Step 2
Expected: PASS for these tests.

**Step 5: Commit**

```bash
git add server/tests/test_monopoly_banking_sim.py server/games/monopoly/banking_sim.py
git commit -m "Add banking simulator test contract"
```

### Task 2: Implement Core Banking Simulator State And Operations

**Files:**
- Modify: `server/games/monopoly/banking_sim.py`
- Modify: `server/tests/test_monopoly_banking_sim.py`

**Step 1: Write the failing test**

```python
def test_transfer_fails_without_mutation_on_insufficient_funds():
    profile = ElectronicBankingProfile(
        preset_id="electronic_banking",
        anchor_edition_id="monopoly-00114",
        starting_balance=100,
    )
    state = init_accounts(["p1", "p2"], profile)
    tx = transfer(state, "p1", "p2", 300, "rent")
    assert tx.status == "failed"
    assert tx.failure_reason == "insufficient_funds"
    assert get_balance(state, "p1") == 100
    assert get_balance(state, "p2") == 100
```

**Step 2: Run test to verify it fails**

Run: `cd server && ../.venv/bin/pytest tests/test_monopoly_banking_sim.py::test_transfer_fails_without_mutation_on_insufficient_funds -v`
Expected: FAIL.

**Step 3: Write minimal implementation**

```python
@dataclass
class BankAccount: ...

@dataclass
class BankTransaction: ...

@dataclass
class BankingState: ...

def transfer(...):
    # validate -> append tx -> mutate only on success
```

**Step 4: Run test to verify it passes**

Run: same as Step 2
Expected: PASS.

**Step 5: Commit**

```bash
git add server/games/monopoly/banking_sim.py server/tests/test_monopoly_banking_sim.py
git commit -m "Implement deterministic banking simulator operations"
```

### Task 3: Add Profile Resolver For Electronic Banking Anchor Rules

**Files:**
- Create: `server/games/monopoly/electronic_banking_profile.py`
- Create: `server/tests/test_monopoly_electronic_banking_profile.py`

**Step 1: Write the failing test**

```python
from server.games.monopoly.electronic_banking_profile import resolve_electronic_banking_profile

def test_resolve_profile_uses_anchor_defaults():
    profile = resolve_electronic_banking_profile("electronic_banking")
    assert profile.anchor_edition_id == "monopoly-00114"
    assert profile.starting_balance > 0
```

**Step 2: Run test to verify it fails**

Run: `cd server && ../.venv/bin/pytest tests/test_monopoly_electronic_banking_profile.py -v`
Expected: FAIL.

**Step 3: Write minimal implementation**

```python
def resolve_electronic_banking_profile(preset_id: str) -> ElectronicBankingProfile:
    # return anchor-first preset profile
```

**Step 4: Run test to verify it passes**

Run: same as Step 2
Expected: PASS.

**Step 5: Commit**

```bash
git add server/games/monopoly/electronic_banking_profile.py server/tests/test_monopoly_electronic_banking_profile.py
git commit -m "Add electronic banking anchor profile resolver"
```

### Task 4: Wire Banking State Into MonopolyGame Start And Score Sync

**Files:**
- Modify: `server/games/monopoly/game.py`
- Modify: `server/tests/test_monopoly.py`

**Step 1: Write the failing test**

```python
def test_electronic_banking_on_start_initializes_bank_accounts():
    game = _start_two_player_game(MonopolyOptions(preset_id="electronic_banking"))
    assert game.banking_state is not None
    assert game._bank_balance(game.players[0]) > 0
```

**Step 2: Run test to verify it fails**

Run: `cd server && ../.venv/bin/pytest tests/test_monopoly.py::test_electronic_banking_on_start_initializes_bank_accounts -v`
Expected: FAIL.

**Step 3: Write minimal implementation**

```python
# add fields:
banking_profile: ElectronicBankingProfile | None = None
banking_state: BankingState | None = None

# on_start:
if electronic_banking:
    self.banking_profile = resolve_electronic_banking_profile(...)
    self.banking_state = init_accounts(...)
```

**Step 4: Run test to verify it passes**

Run: same command as Step 2
Expected: PASS.

**Step 5: Commit**

```bash
git add server/games/monopoly/game.py server/tests/test_monopoly.py
git commit -m "Initialize banking simulator state for electronic banking preset"
```

### Task 5: Route Rent, Tax, And Pass-Go Through Simulator

**Files:**
- Modify: `server/games/monopoly/game.py`
- Create: `server/tests/test_monopoly_electronic_banking.py`

**Step 1: Write the failing test**

```python
def test_electronic_banking_rent_uses_simulator_transfer(monkeypatch):
    game = _start_two_player_game(MonopolyOptions(preset_id="electronic_banking"))
    host = game.players[0]
    guest = game.players[1]
    # arrange host owns baltic, guest lands on it
    ...
    assert game._bank_balance(host) > game.banking_profile.starting_balance
    assert game._bank_balance(guest) < game.banking_profile.starting_balance
```

```python
def test_electronic_banking_tax_uses_simulator_debit(monkeypatch):
    ...
```

**Step 2: Run test to verify it fails**

Run: `cd server && ../.venv/bin/pytest tests/test_monopoly_electronic_banking.py -v`
Expected: FAIL.

**Step 3: Write minimal implementation**

```python
def _bank_transfer(...): ...
def _bank_debit(...): ...
def _bank_credit(...): ...

# route rent/tax/pass-go to these helpers when electronic banking active
```

**Step 4: Run test to verify it passes**

Run: same as Step 2
Expected: PASS.

**Step 5: Commit**

```bash
git add server/games/monopoly/game.py server/tests/test_monopoly_electronic_banking.py
git commit -m "Route electronic banking economy events through simulator"
```

### Task 6: Add Banking Actions (Balance, Transfer, Ledger)

**Files:**
- Modify: `server/games/monopoly/game.py`
- Modify: `server/locales/en/monopoly.ftl`
- Modify: `server/locales/pl/monopoly.ftl`
- Modify: `server/locales/pt/monopoly.ftl`
- Modify: `server/locales/ru/monopoly.ftl`
- Modify: `server/locales/vi/monopoly.ftl`
- Modify: `server/locales/zh/monopoly.ftl`
- Modify: `server/tests/test_monopoly_electronic_banking.py`

**Step 1: Write the failing test**

```python
def test_electronic_banking_actions_visible_only_in_preset():
    eb = _start_two_player_game(MonopolyOptions(preset_id="electronic_banking"))
    cl = _start_two_player_game(MonopolyOptions(preset_id="classic_standard"))
    host_eb = eb.current_player
    host_cl = cl.current_player
    assert eb._is_banking_balance_hidden(host_eb) != Visibility.HIDDEN
    assert cl._is_banking_balance_hidden(host_cl) == Visibility.HIDDEN
```

**Step 2: Run test to verify it fails**

Run: `cd server && ../.venv/bin/pytest tests/test_monopoly_electronic_banking.py::test_electronic_banking_actions_visible_only_in_preset -v`
Expected: FAIL.

**Step 3: Write minimal implementation**

```python
# add actions:
banking_balance
banking_transfer
banking_ledger
# with preset-gated is_enabled/is_hidden and localized labels
```

**Step 4: Run test to verify it passes**

Run: same command as Step 2
Expected: PASS.

**Step 5: Commit**

```bash
git add server/games/monopoly/game.py server/locales/en/monopoly.ftl server/locales/pl/monopoly.ftl server/locales/pt/monopoly.ftl server/locales/ru/monopoly.ftl server/locales/vi/monopoly.ftl server/locales/zh/monopoly.ftl server/tests/test_monopoly_electronic_banking.py
git commit -m "Add electronic banking account and ledger actions"
```

### Task 7: Add Deterministic Ledger Snapshot And Serialization Coverage

**Files:**
- Modify: `server/games/monopoly/banking_sim.py`
- Modify: `server/tests/test_monopoly_banking_sim.py`
- Modify: `server/tests/test_monopoly_electronic_banking.py`

**Step 1: Write the failing test**

```python
def test_banking_snapshot_is_stable_for_same_sequence():
    profile = ElectronicBankingProfile(...)
    state_a = init_accounts(["p1", "p2"], profile)
    state_b = init_accounts(["p1", "p2"], profile)
    transfer(state_a, "p1", "p2", 50, "rent")
    transfer(state_b, "p1", "p2", 50, "rent")
    assert state_a.snapshot() == state_b.snapshot()
```

**Step 2: Run test to verify it fails**

Run: `cd server && ../.venv/bin/pytest tests/test_monopoly_banking_sim.py::test_banking_snapshot_is_stable_for_same_sequence -v`
Expected: FAIL.

**Step 3: Write minimal implementation**

```python
def snapshot(state: BankingState) -> dict:
    # stable order and deterministic fields only
```

**Step 4: Run test to verify it passes**

Run: same command as Step 2
Expected: PASS.

**Step 5: Commit**

```bash
git add server/games/monopoly/banking_sim.py server/tests/test_monopoly_banking_sim.py server/tests/test_monopoly_electronic_banking.py
git commit -m "Add deterministic banking snapshot coverage"
```

### Task 8: Update Bot Economy Decisions For Electronic Banking

**Files:**
- Modify: `server/games/monopoly/game.py`
- Modify: `server/tests/test_monopoly_electronic_banking.py`

**Step 1: Write the failing test**

```python
def test_electronic_banking_bot_uses_bank_balance_for_buy_decision():
    game = _start_two_player_game(MonopolyOptions(preset_id="electronic_banking"))
    host = game.current_player
    host.is_bot = True
    # set a pending buy and constrained bank balance
    ...
    assert game.bot_think(host) in {"buy_property", "auction_property"}
```

**Step 2: Run test to verify it fails**

Run: `cd server && ../.venv/bin/pytest tests/test_monopoly_electronic_banking.py::test_electronic_banking_bot_uses_bank_balance_for_buy_decision -v`
Expected: FAIL.

**Step 3: Write minimal implementation**

```python
def _current_liquid_balance(self, player: MonopolyPlayer) -> int:
    if self._is_electronic_banking_preset():
        return self._bank_balance(player)
    return player.cash
```

Update bot thresholds to use `_current_liquid_balance`.

**Step 4: Run test to verify it passes**

Run: same command as Step 2
Expected: PASS.

**Step 5: Commit**

```bash
git add server/games/monopoly/game.py server/tests/test_monopoly_electronic_banking.py
git commit -m "Use bank balances in electronic banking bot logic"
```

### Task 9: Final Verification Suite

**Files:**
- Modify: tests only if regressions discovered

**Step 1: Run focused electronic banking tests**

Run:

```bash
cd server && ../.venv/bin/pytest tests/test_monopoly_banking_sim.py tests/test_monopoly_electronic_banking.py tests/test_monopoly_electronic_banking_profile.py -v
```

Expected: PASS.

**Step 2: Run Monopoly regression set**

Run:

```bash
cd server && ../.venv/bin/pytest -k monopoly -v
```

Expected: PASS.

**Step 3: Run integration smoke checks**

Run:

```bash
cd server && ../.venv/bin/pytest tests/test_integration.py::TestGameRegistryIntegration::test_pig_game_registered tests/test_integration.py::TestGameRegistryIntegration::test_get_by_category -v
```

Expected: PASS.

**Step 4: Fix regressions minimally if any fail**

Apply targeted patches only; do not refactor broadly in this task.

**Step 5: Commit**

```bash
git add server/games/monopoly/*.py server/tests/test_monopoly*.py server/locales/*/monopoly.ftl
git commit -m "Finalize electronic banking simulator integration"
```

### Task 10: Documentation and Anchor Notes Update

**Files:**
- Modify: `docs/plans/2026-02-26-monopoly-junior-anchor-notes.md` (only if shared policy note needed)
- Create: `docs/plans/2026-02-26-monopoly-electronic-banking-anchor-notes.md`

**Step 1: Write failing doc check**

Expected document must include:
- preset id
- anchor id
- conflict policy
- fallback policy

**Step 2: Run doc check**

Run:

```bash
rg -n "electronic_banking|monopoly-00114|anchor-first|fallback" docs/plans/2026-02-26-monopoly-electronic-banking-anchor-notes.md
```

Expected: initially no matches (before file exists).

**Step 3: Add minimal anchor notes document**

```markdown
# Monopoly Electronic Banking Anchor Notes
- Anchor: monopoly-00114
- Policy: anchor-first
- Fallback: anchor-family -> consensus -> deterministic safe default
```

**Step 4: Re-run doc check**

Run: same as Step 2
Expected: all expected markers present.

**Step 5: Commit**

```bash
git add docs/plans/2026-02-26-monopoly-electronic-banking-anchor-notes.md
git commit -m "Add electronic banking anchor notes"
```

## Done Definition

1. `electronic_banking` economy is fully simulator-backed.
2. Money movement is deterministic and logged.
3. Banking-specific actions are localized and preset-gated.
4. Bot and winner logic use simulator balances where appropriate.
5. Full Monopoly regression suite remains green.
