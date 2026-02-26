# Monopoly Wave 3 Classic Breadth Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add 25 additional high-signal classic special-edition Monopoly boards as selectable `partial_rules` board profiles with regression-safe runtime behavior.

**Architecture:** Reuse the existing data-driven board profile resolver, rule-pack registry, and board-rule module mapping established in Wave 1 and Wave 2. Implement Wave 3 as metadata and test expansion only, keeping game mechanics unchanged beyond existing capability hooks. Preserve deterministic behavior with `partial` fallback semantics and current announcements.

**Tech Stack:** Python 3.13, dataclasses, existing Monopoly runtime (`server/games/monopoly/game.py`), pytest, Fluent locale files, curated Monopoly catalog artifacts.

---

## Wave 3 Canonical IDs

Use this exact list in all Wave 3 tests and data tables:

```python
WAVE3_BOARD_IDS = [
    "disney_star_wars_dark_side",
    "disney_legacy",
    "disney_the_edition",
    "lord_of_the_rings_trilogy",
    "star_wars_saga",
    "marvel_avengers_legacy",
    "star_wars_legacy",
    "star_wars_classic_edition",
    "star_wars_solo",
    "game_of_thrones",
    "deadpool_collectors",
    "toy_story",
    "black_panther",
    "stranger_things_collectors",
    "ghostbusters",
    "marvel_eternals",
    "transformers",
    "stranger_things_netflix",
    "fortnite_collectors",
    "star_wars_mandalorian_s2",
    "transformers_beast_wars",
    "marvel_falcon_winter_soldier",
    "fortnite_flip",
    "marvel_flip",
    "pokemon",
]
```

Use this exact edition mapping:

```python
WAVE3_PACKS = [
    ("disney_star_wars_dark_side", "monopoly-f6167"),
    ("disney_legacy", "monopoly-19643"),
    ("disney_the_edition", "monopoly-40224"),
    ("lord_of_the_rings_trilogy", "monopoly-41603"),
    ("star_wars_saga", "monopoly-42452"),
    ("marvel_avengers_legacy", "monopoly-b0323"),
    ("star_wars_legacy", "monopoly-b0324"),
    ("star_wars_classic_edition", "monopoly-b8613"),
    ("star_wars_solo", "monopoly-e1702"),
    ("game_of_thrones", "monopoly-e3278"),
    ("deadpool_collectors", "monopoly-e4833"),
    ("toy_story", "monopoly-e5065"),
    ("black_panther", "monopoly-e5797"),
    ("stranger_things_collectors", "monopoly-e8194"),
    ("ghostbusters", "monopoly-e9479"),
    ("marvel_eternals", "monopoly-f1659"),
    ("transformers", "monopoly-f1660"),
    ("stranger_things_netflix", "monopoly-f2544"),
    ("fortnite_collectors", "monopoly-f2546"),
    ("star_wars_mandalorian_s2", "monopoly-f4257"),
    ("transformers_beast_wars", "monopoly-f5269"),
    ("marvel_falcon_winter_soldier", "monopoly-f5851"),
    ("fortnite_flip", "monopoly-f7774"),
    ("marvel_flip", "monopoly-f9931"),
    ("pokemon", "monopoly-g0716"),
]
```

### Task 1: Create Wave 3 Source Artifact

**Files:**
- Create: `docs/plans/2026-02-26-monopoly-wave3-top25-classic.md`
- Read: `docs/plans/2026-02-26-monopoly-wave3-classic-breadth-design.md`
- Read: `docs/plans/2026-02-26-monopoly-themed-board-backlog.md`

**Step 1: Write failing existence check**

Run:

```bash
rg -n "Wave 3 Top 25 Classic" docs/plans/2026-02-26-monopoly-wave3-top25-classic.md
```

Expected: FAIL with missing file.

**Step 2: Create curated Top-25 source file**

Create markdown table with exactly these 25 rows and columns:

```markdown
# Monopoly Wave 3 Top 25 Classic

| board_id | edition_id | bucket | manual_en_us | status_target |
|---|---|---|---|---|
| disney_star_wars_dark_side | monopoly-f6167 | disney | yes | partial_rules |
| ... 24 more rows from WAVE3_PACKS ... |
```

**Step 3: Validate row count**

Run:

```bash
python - <<'PY'
from pathlib import Path
p=Path('docs/plans/2026-02-26-monopoly-wave3-top25-classic.md')
rows=[line for line in p.read_text().splitlines() if line.startswith('| ') and '---' not in line]
print('rows',len(rows)-1)
PY
```

Expected: `rows 25`.

**Step 4: Commit**

```bash
git add docs/plans/2026-02-26-monopoly-wave3-top25-classic.md
git commit -m "Add Wave 3 Top 25 classic board source"
```

### Task 2: Add Wave 3 Board Profiles

**Files:**
- Modify: `server/games/monopoly/board_profile.py`
- Create: `server/tests/test_monopoly_wave3_board_profile.py`
- Read: `docs/plans/2026-02-26-monopoly-wave3-top25-classic.md`

**Step 1: Write failing profile resolution tests**

Create:

```python
import pytest
from server.games.monopoly.board_profile import resolve_board_plan

WAVE3_BOARD_IDS = [ ... exact 25 ids ... ]

@pytest.mark.parametrize("board_id", WAVE3_BOARD_IDS)
def test_wave3_boards_resolve_to_classic_board_rules(board_id: str):
    plan = resolve_board_plan("classic_standard", board_id, "auto")
    assert plan.effective_preset_id == "classic_standard"
    assert plan.effective_mode == "board_rules"
    assert plan.rule_pack_status == "partial"
```

**Step 2: Run failing test**

Run: `cd server && ../.venv/bin/pytest tests/test_monopoly_wave3_board_profile.py -v`

Expected: FAIL (`effective_mode` mismatch or unknown board fallback).

**Step 3: Add 25 `BoardProfile` entries**

For each `board_id, edition_id` row add:

```python
"disney_star_wars_dark_side": BoardProfile(
    board_id="disney_star_wars_dark_side",
    label_key="monopoly-board-disney-star-wars-dark-side",
    anchor_edition_id="monopoly-f6167",
    compatible_preset_ids=("classic_standard",),
    fallback_preset_id="classic_standard",
    rule_pack_id="disney_star_wars_dark_side",
    rule_pack_status="partial",
),
```

Repeat for all 25 rows.

**Step 4: Run passing test**

Run: `cd server && ../.venv/bin/pytest tests/test_monopoly_wave3_board_profile.py -v`

Expected: PASS.

**Step 5: Commit**

```bash
git add server/games/monopoly/board_profile.py server/tests/test_monopoly_wave3_board_profile.py
git commit -m "Add Wave 3 classic board profiles"
```

### Task 3: Register Wave 3 Rule Packs

**Files:**
- Modify: `server/games/monopoly/board_rules_registry.py`
- Create: `server/tests/test_monopoly_wave3_board_rules_registry.py`

**Step 1: Write failing registry test**

```python
import pytest
from server.games.monopoly.board_rules_registry import get_rule_pack, supports_capability

WAVE3_RULE_PACK_IDS = [ ... exact 25 ids ... ]

@pytest.mark.parametrize("rule_pack_id", WAVE3_RULE_PACK_IDS)
def test_wave3_rule_pack_registered(rule_pack_id: str):
    pack = get_rule_pack(rule_pack_id)
    assert pack is not None
    assert pack.status == "partial"
    assert supports_capability(rule_pack_id, "pass_go_credit_override") is True
```

**Step 2: Run failing test**

Run: `cd server && ../.venv/bin/pytest tests/test_monopoly_wave3_board_rules_registry.py -v`

Expected: FAIL.

**Step 3: Add 25 `BoardRulePack` entries**

For each Wave 3 pack id:

```python
"disney_star_wars_dark_side": BoardRulePack(
    rule_pack_id="disney_star_wars_dark_side",
    status="partial",
    capability_ids=("pass_go_credit_override", "startup_board_announcement"),
),
```

**Step 4: Run passing test**

Run: `cd server && ../.venv/bin/pytest tests/test_monopoly_wave3_board_rules_registry.py -v`

Expected: PASS.

**Step 5: Commit**

```bash
git add server/games/monopoly/board_rules_registry.py server/tests/test_monopoly_wave3_board_rules_registry.py
git commit -m "Add Wave 3 board rules registry entries"
```

### Task 4: Add Wave 3 Rule-Pack Stub Modules

**Files:**
- Create: `server/games/monopoly/board_rules/<25_wave3_modules>.py`
- Modify: `server/games/monopoly/board_rules/__init__.py`
- Create: `server/tests/test_monopoly_wave3_rule_pack_modules.py`

**Step 1: Write failing module test**

```python
import pytest
from server.games.monopoly.board_rules import disney_star_wars_dark_side, marvel_flip

def test_wave3_stub_constants_contract():
    assert disney_star_wars_dark_side.ANCHOR_EDITION_ID == "monopoly-f6167"
    assert marvel_flip.RULE_PACK_STATUS == "partial"
    assert isinstance(marvel_flip.PASS_GO_CREDIT_OVERRIDE, int)
```

**Step 2: Run failing test**

Run: `cd server && ../.venv/bin/pytest tests/test_monopoly_wave3_rule_pack_modules.py -v`

Expected: FAIL due to missing modules/imports.

**Step 3: Create 25 stub constant modules**

Each module must define:

```python
RULE_PACK_ID = "disney_star_wars_dark_side"
ANCHOR_EDITION_ID = "monopoly-f6167"
RULE_PACK_STATUS = "partial"
PASS_GO_CREDIT_OVERRIDE = 200
CAPABILITY_IDS = ("pass_go_credit_override", "startup_board_announcement")
SIMPLIFICATION_NOTE_KEY = "monopoly-board-rules-simplified"
```

Update `__init__.py` imports and `__all__`.

**Step 4: Run passing test**

Run: `cd server && ../.venv/bin/pytest tests/test_monopoly_wave3_rule_pack_modules.py -v`

Expected: PASS.

**Step 5: Commit**

```bash
git add server/games/monopoly/board_rules/__init__.py server/games/monopoly/board_rules/*.py server/tests/test_monopoly_wave3_rule_pack_modules.py
git commit -m "Add Wave 3 board rule-pack stubs"
```

### Task 5: Wire Wave 3 Runtime Module Mapping

**Files:**
- Modify: `server/games/monopoly/board_rules_registry.py`
- Create: `server/tests/test_monopoly_wave3_pass_go_override.py`

**Step 1: Write failing integration test**

```python
from server.games.monopoly.game import MonopolyGame, MonopolyOptions
from server.users.test_user import MockUser

def test_wave3_board_pass_go_override_path(monkeypatch):
    game = MonopolyGame(options=MonopolyOptions(
        preset_id="classic_standard",
        board_id="disney_star_wars_dark_side",
        board_rules_mode="auto",
    ))
    game.add_player("Host", MockUser("Host"))
    game.add_player("Guest", MockUser("Guest"))
    game.host = "Host"
    game.on_start()

    host = game.current_player
    host.position = 39
    monkeypatch.setattr(
        "server.games.monopoly.board_rules.disney_star_wars_dark_side.PASS_GO_CREDIT_OVERRIDE",
        275,
    )
    rolls = iter([1, 1])
    monkeypatch.setattr("server.games.monopoly.game.random.randint", lambda a, b: next(rolls))
    game.execute_action(host, "roll_dice")
    assert host.cash == 1775
```

**Step 2: Run failing test**

Run: `cd server && ../.venv/bin/pytest tests/test_monopoly_wave3_pass_go_override.py -v`

Expected: FAIL (`1700` cash) before module mapping.

**Step 3: Extend `RULE_PACK_MODULES`**

Map all 25 Wave 3 pack ids to their corresponding modules and ensure imports exist.

**Step 4: Run passing test**

Run: `cd server && ../.venv/bin/pytest tests/test_monopoly_wave3_pass_go_override.py -v`

Expected: PASS.

**Step 5: Commit**

```bash
git add server/games/monopoly/board_rules_registry.py server/tests/test_monopoly_wave3_pass_go_override.py
git commit -m "Wire Wave 3 board modules into capability runtime"
```

### Task 6: Add Wave 3 Locale Labels

**Files:**
- Modify: `server/locales/en/monopoly.ftl`
- Modify: `server/locales/pl/monopoly.ftl`
- Modify: `server/locales/pt/monopoly.ftl`
- Modify: `server/locales/ru/monopoly.ftl`
- Modify: `server/locales/vi/monopoly.ftl`
- Modify: `server/locales/zh/monopoly.ftl`
- Create: `server/tests/test_monopoly_wave3_board_labels.py`

**Step 1: Write failing label tests**

```python
import pytest
from server.messages.localization import Localization

WAVE3_LABEL_KEYS = [
    "monopoly-board-disney-star-wars-dark-side",
    # ... all 25 keys ...
]
LOCALES = ("en", "pl", "pt", "ru", "vi", "zh")

@pytest.mark.parametrize("locale", LOCALES)
@pytest.mark.parametrize("label_key", WAVE3_LABEL_KEYS)
def test_wave3_board_label_keys_exist_per_locale(locale: str, label_key: str):
    assert Localization.get(locale, label_key) != label_key
```

**Step 2: Run failing test**

Run: `cd server && ../.venv/bin/pytest tests/test_monopoly_wave3_board_labels.py -v`

Expected: FAIL.

**Step 3: Add 25 label keys in all locales**

Example:

```ftl
monopoly-board-disney-star-wars-dark-side = Disney Star Wars Dark Side
```

Use consistent English fallback strings across locales for parity.

**Step 4: Run passing test**

Run: `cd server && ../.venv/bin/pytest tests/test_monopoly_wave3_board_labels.py -v`

Expected: PASS.

**Step 5: Commit**

```bash
git add server/locales/*/monopoly.ftl server/tests/test_monopoly_wave3_board_labels.py
git commit -m "Add Wave 3 board localization labels"
```

### Task 7: Add Wave 3 Startup Matrix Tests

**Files:**
- Create: `server/tests/test_monopoly_wave3_boards.py`
- Modify if needed: `server/games/monopoly/*.py`

**Step 1: Write failing startup matrix tests**

```python
import pytest
from server.games.monopoly.game import MonopolyGame, MonopolyOptions
from server.users.test_user import MockUser

WAVE3_BOARD_IDS = [ ... exact 25 ids ... ]

def _start_two_player_game(options: MonopolyOptions) -> MonopolyGame:
    game = MonopolyGame(options=options)
    game.add_player("Host", MockUser("Host"))
    game.add_player("Guest", MockUser("Guest"))
    game.host = "Host"
    game.on_start()
    return game

@pytest.mark.parametrize("board_id", WAVE3_BOARD_IDS)
def test_wave3_board_starts_in_auto_board_rules(board_id: str):
    game = _start_two_player_game(MonopolyOptions(
        preset_id="classic_standard",
        board_id=board_id,
        board_rules_mode="auto",
    ))
    assert game.active_board_id == board_id
    assert game.active_board_effective_mode == "board_rules"

def test_wave3_board_autofixes_incompatible_preset():
    game = _start_two_player_game(MonopolyOptions(
        preset_id="city",
        board_id="disney_star_wars_dark_side",
        board_rules_mode="auto",
    ))
    assert game.active_preset_id == "classic_standard"
```

**Step 2: Run test**

Run: `cd server && ../.venv/bin/pytest tests/test_monopoly_wave3_boards.py -v`

Expected: PASS after previous tasks, otherwise apply minimal data fixes.

**Step 3: Commit**

```bash
git add server/tests/test_monopoly_wave3_boards.py server/games/monopoly/*.py
git commit -m "Add Wave 3 board startup integration matrix"
```

### Task 8: Update Backlog Status for Wave 3 Selection

**Files:**
- Modify: `docs/plans/2026-02-26-monopoly-themed-board-backlog.md`
- Read: `docs/plans/2026-02-26-monopoly-wave3-top25-classic.md`

**Step 1: Write failing status validation**

Run:

```bash
python - <<'PY'
from pathlib import Path
backlog = Path('docs/plans/2026-02-26-monopoly-themed-board-backlog.md').read_text()
for eid in [
    "monopoly-f6167","monopoly-19643","monopoly-40224","monopoly-41603","monopoly-42452",
    "monopoly-b0323","monopoly-b0324","monopoly-b8613","monopoly-e1702","monopoly-e3278",
    "monopoly-e4833","monopoly-e5065","monopoly-e5797","monopoly-e8194","monopoly-e9479",
    "monopoly-f1659","monopoly-f1660","monopoly-f2544","monopoly-f2546","monopoly-f4257",
    "monopoly-f5269","monopoly-f5851","monopoly-f7774","monopoly-f9931","monopoly-g0716",
]:
    needle = f"| `{eid}` |"
    if needle not in backlog:
        raise SystemExit(f"missing row: {eid}")
    line = next(l for l in backlog.splitlines() if needle in l)
    if '`partial_rules`' not in line:
        raise SystemExit(f"not partial_rules: {eid}")
print('ok')
PY
```

Expected: FAIL before updates.

**Step 2: Update statuses**

Set only the selected 25 edition rows from `not_started` to `partial_rules`.

**Step 3: Re-run validation**

Expected: `ok`.

**Step 4: Commit**

```bash
git add docs/plans/2026-02-26-monopoly-themed-board-backlog.md
git commit -m "Update backlog status for Wave 3 classic boards"
```

### Task 9: Final Verification and Stabilization (@verification-before-completion)

**Files:**
- Modify only if regression fixes are required.

**Step 1: Run focused Wave 3 tests**

Run:

```bash
cd server && ../.venv/bin/pytest \
  tests/test_monopoly_wave3_board_profile.py \
  tests/test_monopoly_wave3_board_rules_registry.py \
  tests/test_monopoly_wave3_rule_pack_modules.py \
  tests/test_monopoly_wave3_board_labels.py \
  tests/test_monopoly_wave3_pass_go_override.py \
  tests/test_monopoly_wave3_boards.py -v
```

Expected: PASS.

**Step 2: Run Monopoly regression**

Run:

```bash
cd server && ../.venv/bin/pytest -k monopoly -v
```

Expected: PASS.

**Step 3: Run integration smoke**

Run:

```bash
cd server && ../.venv/bin/pytest \
  tests/test_integration.py::TestGameRegistryIntegration::test_pig_game_registered \
  tests/test_integration.py::TestGameRegistryIntegration::test_get_by_category -v
```

Expected: PASS.

**Step 4: Fix regressions minimally (if any)**

Patch only failing scope first, rerun failed scope, then rerun full verification.

**Step 5: Commit stabilization**

```bash
git add server/games/monopoly/*.py server/games/monopoly/board_rules/*.py server/tests/test_monopoly_wave3*.py server/locales/*/monopoly.ftl docs/plans/2026-02-26-monopoly-themed-board-backlog.md docs/plans/2026-02-26-monopoly-wave3-top25-classic.md
git commit -m "Finalize Monopoly Wave 3 classic board breadth rollout"
```
