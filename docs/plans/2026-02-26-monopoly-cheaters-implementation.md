# Monopoly Cheaters Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Implement full-fidelity deterministic `cheaters` preset mechanics from anchor rules (`monopoly-e4888`) using an event-driven cheat detection engine.

**Architecture:** Add an anchor-driven cheaters profile resolver and a deterministic cheaters engine module with event hooks. Wire `MonopolyGame` action boundaries to emit events and apply engine outcomes (allow/block/penalty/reward) through existing economy and bankruptcy helpers, while keeping non-cheaters presets unchanged.

**Tech Stack:** Python 3.13, dataclasses, pytest, existing Monopoly engine (`server/games/monopoly/game.py`), Fluent localization files.

---

### Task 1: Add Cheaters Profile Resolver

**Files:**
- Create: `server/games/monopoly/cheaters_profile.py`
- Create: `server/tests/test_monopoly_cheaters_profile.py`

**Step 1: Write the failing test**

```python
from server.games.monopoly.cheaters_profile import (
    DEFAULT_CHEATERS_PROFILE,
    resolve_cheaters_profile,
)


def test_resolve_cheaters_profile_uses_anchor_defaults():
    profile = resolve_cheaters_profile("cheaters")
    assert profile.preset_id == "cheaters"
    assert profile.anchor_edition_id == "monopoly-e4888"
    assert profile.source_policy == "anchor-first"
    assert "early_end_turn" in profile.enabled_rules


def test_resolve_cheaters_profile_falls_back_to_default():
    profile = resolve_cheaters_profile("unknown")
    assert profile == DEFAULT_CHEATERS_PROFILE
```

**Step 2: Run test to verify it fails**

Run: `cd server && ../.venv/bin/pytest tests/test_monopoly_cheaters_profile.py -v`
Expected: FAIL because profile module does not exist.

**Step 3: Write minimal implementation**

Create dataclass:

```python
@dataclass(frozen=True)
class CheatersProfile:
    preset_id: str
    anchor_edition_id: str
    source_policy: str = "anchor-first"
    enabled_rules: tuple[str, ...] = ()
    penalty_amounts: dict[str, int] = field(default_factory=dict)
    reward_amounts: dict[str, int] = field(default_factory=dict)
    escalation_threshold: int = 2
    provenance_notes: tuple[str, ...] = ()
```

Define `DEFAULT_CHEATERS_PROFILE` anchored to `monopoly-e4888` and `resolve_cheaters_profile(...)`.

**Step 4: Run test to verify it passes**

Run: same as Step 2
Expected: PASS.

**Step 5: Commit**

```bash
git add server/games/monopoly/cheaters_profile.py server/tests/test_monopoly_cheaters_profile.py
git commit -m "Add cheaters profile resolver"
```

### Task 2: Add Deterministic Cheaters Engine Core

**Files:**
- Create: `server/games/monopoly/cheaters_engine.py`
- Create: `server/tests/test_monopoly_cheaters_engine.py`

**Step 1: Write the failing test**

```python
from server.games.monopoly.cheaters_engine import CheatersEngine
from server.games.monopoly.cheaters_profile import DEFAULT_CHEATERS_PROFILE


def test_engine_blocks_early_end_turn_with_penalty():
    engine = CheatersEngine(DEFAULT_CHEATERS_PROFILE)
    engine.on_turn_start("p1", turn_index=0)
    outcome = engine.on_turn_end_attempt("p1", context={"turn_has_rolled": False})
    assert outcome.status == "penalty"
    assert outcome.cash_delta < 0
    assert outcome.message_key == "monopoly-cheaters-early-end-turn-blocked"


def test_engine_allows_end_turn_after_roll():
    engine = CheatersEngine(DEFAULT_CHEATERS_PROFILE)
    engine.on_turn_start("p1", turn_index=0)
    outcome = engine.on_turn_end_attempt("p1", context={"turn_has_rolled": True})
    assert outcome.status == "allow"
```

**Step 2: Run test to verify it fails**

Run: `cd server && ../.venv/bin/pytest tests/test_monopoly_cheaters_engine.py -v`
Expected: FAIL.

**Step 3: Write minimal implementation**

Add:

- `CheaterOutcome` dataclass
- `CheatersEngine` with per-player turn state
- `on_turn_start(...)`
- `on_turn_end_attempt(...)` for early-end-turn detector

**Step 4: Run test to verify it passes**

Run: same as Step 2
Expected: PASS.

**Step 5: Commit**

```bash
git add server/games/monopoly/cheaters_engine.py server/tests/test_monopoly_cheaters_engine.py
git commit -m "Add deterministic cheaters engine core"
```

### Task 3: Add Escalation Behavior in Engine

**Files:**
- Modify: `server/games/monopoly/cheaters_engine.py`
- Modify: `server/tests/test_monopoly_cheaters_engine.py`

**Step 1: Write the failing test**

```python
def test_engine_escalates_penalty_after_threshold():
    engine = CheatersEngine(DEFAULT_CHEATERS_PROFILE)
    engine.on_turn_start("p1", turn_index=0)
    first = engine.on_turn_end_attempt("p1", context={"turn_has_rolled": False})
    second = engine.on_turn_end_attempt("p1", context={"turn_has_rolled": False})
    assert second.cash_delta <= first.cash_delta
    assert second.reason_code == "escalated_repeat_violation"
```

**Step 2: Run test to verify it fails**

Run: `cd server && ../.venv/bin/pytest tests/test_monopoly_cheaters_engine.py::test_engine_escalates_penalty_after_threshold -v`
Expected: FAIL.

**Step 3: Write minimal implementation**

Track strike counts and apply stronger penalty once `escalation_threshold` is reached.

**Step 4: Run test to verify it passes**

Run: same as Step 2
Expected: PASS.

**Step 5: Commit**

```bash
git add server/games/monopoly/cheaters_engine.py server/tests/test_monopoly_cheaters_engine.py
git commit -m "Add cheaters penalty escalation behavior"
```

### Task 4: Initialize Cheaters Profile and Engine in MonopolyGame

**Files:**
- Modify: `server/games/monopoly/game.py`
- Modify: `server/tests/test_monopoly.py`
- Create: `server/tests/test_monopoly_cheaters.py`

**Step 1: Write the failing test**

```python
def test_cheaters_on_start_initializes_profile_and_engine():
    game = _start_two_player_game(MonopolyOptions(preset_id="cheaters"))
    assert game.cheaters_profile is not None
    assert game.cheaters_engine is not None
    assert game.cheaters_profile.anchor_edition_id == "monopoly-e4888"
```

**Step 2: Run test to verify it fails**

Run: `cd server && ../.venv/bin/pytest tests/test_monopoly_cheaters.py::test_cheaters_on_start_initializes_profile_and_engine -v`
Expected: FAIL.

**Step 3: Write minimal implementation**

Add fields:

- `cheaters_profile: CheatersProfile | None = None`
- `cheaters_engine: CheatersEngine | None = None`

On `on_start`, initialize when `active_preset_id == "cheaters"` and reset otherwise.

**Step 4: Run test to verify it passes**

Run: same as Step 2
Expected: PASS.

**Step 5: Commit**

```bash
git add server/games/monopoly/game.py server/tests/test_monopoly.py server/tests/test_monopoly_cheaters.py
git commit -m "Initialize cheaters preset engine in Monopoly game"
```

### Task 5: Wire End-Turn Detector and Penalty Application

**Files:**
- Modify: `server/games/monopoly/game.py`
- Modify: `server/locales/en/monopoly.ftl`
- Modify: `server/locales/pl/monopoly.ftl`
- Modify: `server/locales/pt/monopoly.ftl`
- Modify: `server/locales/ru/monopoly.ftl`
- Modify: `server/locales/vi/monopoly.ftl`
- Modify: `server/locales/zh/monopoly.ftl`
- Modify: `server/tests/test_monopoly_cheaters.py`

**Step 1: Write the failing test**

```python
def test_cheaters_blocks_end_turn_before_roll_and_applies_penalty():
    game = _start_two_player_game(MonopolyOptions(preset_id="cheaters"))
    host = game.current_player
    assert host is not None
    starting = host.cash

    game.execute_action(host, "end_turn")

    assert game.current_player is host
    assert host.cash < starting
```

**Step 2: Run test to verify it fails**

Run: `cd server && ../.venv/bin/pytest tests/test_monopoly_cheaters.py::test_cheaters_blocks_end_turn_before_roll_and_applies_penalty -v`
Expected: FAIL.

**Step 3: Write minimal implementation**

In `_action_end_turn`, before advancing turn:

- call engine `on_turn_end_attempt(...)`
- if `block/penalty`, apply penalty through `_debit_player_to_bank(..., allow_partial=True)` or bankruptcy path
- broadcast localized message
- return without turn advance

Add localization keys in all locales.

**Step 4: Run test to verify it passes**

Run: same as Step 2
Expected: PASS.

**Step 5: Commit**

```bash
git add server/games/monopoly/game.py server/locales/en/monopoly.ftl server/locales/pl/monopoly.ftl server/locales/pt/monopoly.ftl server/locales/ru/monopoly.ftl server/locales/vi/monopoly.ftl server/locales/zh/monopoly.ftl server/tests/test_monopoly_cheaters.py
git commit -m "Wire cheaters end-turn detector and penalties"
```

### Task 6: Wire Payment-Avoidance Detection Hook

**Files:**
- Modify: `server/games/monopoly/game.py`
- Modify: `server/tests/test_monopoly_cheaters.py`

**Step 1: Write the failing test**

```python
def test_cheaters_payment_violation_triggers_penalty():
    game = _start_two_player_game(MonopolyOptions(preset_id="cheaters"))
    host = game.current_player
    guest = game.players[1]
    # Arrange host owns Baltic, guest lands there.
    ...
    # Guest attempts sequence that would evade required payment.
    ...
    assert guest.cash < expected_without_penalty
```

**Step 2: Run test to verify it fails**

Run: `cd server && ../.venv/bin/pytest tests/test_monopoly_cheaters.py::test_cheaters_payment_violation_triggers_penalty -v`
Expected: FAIL.

**Step 3: Write minimal implementation**

Add hook calls around payment-required/payment-result paths and penalize flagged evasions.

**Step 4: Run test to verify it passes**

Run: same as Step 2
Expected: PASS.

**Step 5: Commit**

```bash
git add server/games/monopoly/game.py server/tests/test_monopoly_cheaters.py
git commit -m "Add cheaters payment-avoidance detection hook"
```

### Task 7: Add Reward Path (Anchor-Backed) if Configured

**Files:**
- Modify: `server/games/monopoly/cheaters_engine.py`
- Modify: `server/games/monopoly/game.py`
- Modify: `server/tests/test_monopoly_cheaters_engine.py`
- Modify: `server/tests/test_monopoly_cheaters.py`

**Step 1: Write the failing test**

```python
def test_cheaters_engine_can_emit_reward_outcome():
    engine = CheatersEngine(DEFAULT_CHEATERS_PROFILE)
    engine.on_turn_start("p1", 0)
    outcome = engine.on_action_attempt("p1", "claim_cheat_reward", context={})
    assert outcome.status in {"allow", "reward"}
    if outcome.status == "reward":
        assert outcome.cash_delta > 0
```

**Step 2: Run test to verify it fails**

Run: `cd server && ../.venv/bin/pytest tests/test_monopoly_cheaters_engine.py::test_cheaters_engine_can_emit_reward_outcome -v`
Expected: FAIL.

**Step 3: Write minimal implementation**

Implement deterministic optional reward event path guarded by profile `enabled_rules`.

**Step 4: Run test to verify it passes**

Run: same as Step 2
Expected: PASS.

**Step 5: Commit**

```bash
git add server/games/monopoly/cheaters_engine.py server/games/monopoly/game.py server/tests/test_monopoly_cheaters_engine.py server/tests/test_monopoly_cheaters.py
git commit -m "Add cheaters reward outcome path"
```

### Task 8: Final Verification

**Files:**
- Modify: tests only if regressions are found

**Step 1: Run focused cheaters tests**

Run:

```bash
cd server && ../.venv/bin/pytest tests/test_monopoly_cheaters_profile.py tests/test_monopoly_cheaters_engine.py tests/test_monopoly_cheaters.py -v
```

Expected: PASS.

**Step 2: Run Monopoly regression suite**

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

**Step 4: Fix regressions minimally if needed**

Use targeted patches only.

**Step 5: Commit**

```bash
git add server/games/monopoly/*.py server/tests/test_monopoly*.py server/locales/*/monopoly.ftl
git commit -m "Finalize cheaters preset engine integration"
```

## Done Definition

1. `cheaters` preset initializes anchor-driven profile and engine.
2. Early end-turn cheat detection blocks and penalizes deterministically.
3. Payment-avoidance hook path applies anchor-backed penalties safely.
4. Optional reward outcomes are deterministic and profile-gated.
5. Monopoly regression suite remains green.
