# Monopoly Manual-Core All Special Boards Implementation Plan

> Status update (2026-02-26): Implementation through executable payload completion is done.  
> For full done-vs-remaining tracking and the final manual-auth roadmap, see `docs/plans/2026-02-26-monopoly-special-boards-final-part-status.md`.

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Deliver strict manual-cited, full-mechanics Monopoly parity by implementing Mario boards first, then migrating all remaining special boards to manual-core/near-full fidelity.

**Architecture:** Introduce a canonical manual-rules data layer (board layout, economy, cards, mechanics, win conditions, citations), refactor runtime to resolve active board rules from this layer, and enforce citation validation gates before any manual-core promotion. Use Mario as the reference migration, then scale board-family waves with the same conformance suite.

**Tech Stack:** Python 3.11+, pytest/pytest-asyncio, existing Monopoly runtime (`server/games/monopoly`), JSON/dataclass rule artifacts, existing catalog/manual metadata.

---

### Task 1: Add Manual Rule Schema Models

**Files:**
- Create: `server/games/monopoly/manual_rules/models.py`
- Create: `server/tests/test_monopoly_manual_rule_models.py`

**Step 1: Write the failing test**

```python
from server.games.monopoly.manual_rules.models import ManualRuleSet


def test_manual_rule_set_requires_citations():
    payload = {
        "board_id": "mario_kart",
        "anchor_edition_id": "monopoly-e1870",
        "board": {"spaces": []},
        "economy": {"properties": {}},
        "cards": {"chance": [], "community_chest": []},
        "mechanics": {},
        "win_condition": {"type": "bankruptcy"},
        "citations": [],
    }
    ManualRuleSet.from_dict(payload)
```

**Step 2: Run test to verify it fails**

Run: `cd server && ../.venv/bin/pytest tests/test_monopoly_manual_rule_models.py::test_manual_rule_set_requires_citations -v`  
Expected: FAIL with import/model missing.

**Step 3: Write minimal implementation**

```python
@dataclass(frozen=True)
class Citation:
    rule_path: str
    edition_id: str
    page_ref: str
    confidence: str


@dataclass(frozen=True)
class ManualRuleSet:
    board_id: str
    anchor_edition_id: str
    board: dict[str, object]
    economy: dict[str, object]
    cards: dict[str, object]
    mechanics: dict[str, object]
    win_condition: dict[str, object]
    citations: tuple[Citation, ...]

    @classmethod
    def from_dict(cls, payload: dict[str, object]) -> "ManualRuleSet":
        citations = tuple(Citation(**row) for row in payload["citations"])
        if not citations:
            raise ValueError("citations must be non-empty")
        return cls(...)
```

**Step 4: Run test to verify it passes**

Run: `cd server && ../.venv/bin/pytest tests/test_monopoly_manual_rule_models.py -v`  
Expected: PASS.

**Step 5: Commit**

```bash
git add server/games/monopoly/manual_rules/models.py server/tests/test_monopoly_manual_rule_models.py
git commit -m "Add manual rule schema models for Monopoly boards"
```

### Task 2: Add Manual Rule Loader and Parsing

**Files:**
- Create: `server/games/monopoly/manual_rules/loader.py`
- Create: `server/games/monopoly/manual_rules/__init__.py`
- Create: `server/tests/test_monopoly_manual_rule_loader.py`
- Create: `server/games/monopoly/manual_rules/data/.gitkeep`

**Step 1: Write the failing test**

```python
from server.games.monopoly.manual_rules.loader import load_manual_rule_set


def test_loader_reads_board_rule_json(tmp_path):
    board_file = tmp_path / "mario_kart.json"
    board_file.write_text('{"board_id":"mario_kart","anchor_edition_id":"monopoly-e1870","board":{"spaces":[]},"economy":{"properties":{}},"cards":{"chance":[],"community_chest":[]},"mechanics":{},"win_condition":{"type":"bankruptcy"},"citations":[{"rule_path":"cards.chance[0]","edition_id":"monopoly-e1870","page_ref":"p.8","confidence":"high"}]}', encoding="utf-8")
    rules = load_manual_rule_set("mario_kart", data_dir=tmp_path)
    assert rules.board_id == "mario_kart"
```

**Step 2: Run test to verify it fails**

Run: `cd server && ../.venv/bin/pytest tests/test_monopoly_manual_rule_loader.py::test_loader_reads_board_rule_json -v`  
Expected: FAIL with missing loader.

**Step 3: Write minimal implementation**

```python
def load_manual_rule_set(board_id: str, data_dir: Path | None = None) -> ManualRuleSet:
    base = data_dir or (Path(__file__).parent / "data")
    path = base / f"{board_id}.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    return ManualRuleSet.from_dict(payload)
```

**Step 4: Run test to verify it passes**

Run: `cd server && ../.venv/bin/pytest tests/test_monopoly_manual_rule_loader.py -v`  
Expected: PASS.

**Step 5: Commit**

```bash
git add server/games/monopoly/manual_rules/loader.py server/games/monopoly/manual_rules/__init__.py server/tests/test_monopoly_manual_rule_loader.py server/games/monopoly/manual_rules/data/.gitkeep
git commit -m "Add manual rule loader for board data artifacts"
```

### Task 3: Add Citation Validation Gate

**Files:**
- Create: `server/games/monopoly/manual_rules/validator.py`
- Create: `server/tests/test_monopoly_manual_rule_validator.py`

**Step 1: Write the failing test**

```python
from server.games.monopoly.manual_rules.validator import validate_manual_rule_set


def test_validator_rejects_missing_rule_path_citation(manual_rule_set_fixture):
    errors = validate_manual_rule_set(manual_rule_set_fixture)
    assert "economy.properties" in "\n".join(errors)
```

**Step 2: Run test to verify it fails**

Run: `cd server && ../.venv/bin/pytest tests/test_monopoly_manual_rule_validator.py::test_validator_rejects_missing_rule_path_citation -v`  
Expected: FAIL with missing validator.

**Step 3: Write minimal implementation**

```python
def validate_manual_rule_set(rule_set: ManualRuleSet) -> list[str]:
    errors: list[str] = []
    cited_paths = {c.rule_path for c in rule_set.citations}
    required = {"board.spaces", "economy.properties", "cards.chance", "cards.community_chest", "win_condition"}
    for path in required:
        if path not in cited_paths:
            errors.append(f"missing citation for {path}")
    return errors
```

**Step 4: Run test to verify it passes**

Run: `cd server && ../.venv/bin/pytest tests/test_monopoly_manual_rule_validator.py -v`  
Expected: PASS.

**Step 5: Commit**

```bash
git add server/games/monopoly/manual_rules/validator.py server/tests/test_monopoly_manual_rule_validator.py
git commit -m "Add citation validation gate for manual board rules"
```

### Task 4: Wire Runtime Board Rule Resolver

**Files:**
- Modify: `server/games/monopoly/game.py`
- Create: `server/tests/test_monopoly_manual_rule_runtime_resolution.py`

**Step 1: Write the failing test**

```python
def test_board_rules_mode_uses_loaded_manual_rule_set(monkeypatch):
    game = _start_game(board_id="mario_kart", board_rules_mode="auto")
    assert game.active_manual_rule_set is not None
    assert game.active_manual_rule_set.board_id == "mario_kart"
```

**Step 2: Run test to verify it fails**

Run: `cd server && ../.venv/bin/pytest tests/test_monopoly_manual_rule_runtime_resolution.py::test_board_rules_mode_uses_loaded_manual_rule_set -v`  
Expected: FAIL with missing field/path.

**Step 3: Write minimal implementation**

```python
self.active_manual_rule_set: ManualRuleSet | None = None
if self.active_board_effective_mode == "board_rules":
    self.active_manual_rule_set = load_manual_rule_set(self.active_board_id)
```

**Step 4: Run test to verify it passes**

Run: `cd server && ../.venv/bin/pytest tests/test_monopoly_manual_rule_runtime_resolution.py -v`  
Expected: PASS.

**Step 5: Commit**

```bash
git add server/games/monopoly/game.py server/tests/test_monopoly_manual_rule_runtime_resolution.py
git commit -m "Wire Monopoly runtime to load manual board rule sets"
```

### Task 5: Replace Static Board Space Resolution with Rule-Driven Board Layout

**Files:**
- Modify: `server/games/monopoly/game.py`
- Create: `server/tests/test_monopoly_manual_rule_board_layout.py`

**Step 1: Write the failing test**

```python
def test_manual_rule_space_lookup_uses_board_specific_space_ids(monkeypatch):
    game = _start_game(board_id="mario_kart", board_rules_mode="auto")
    assert game._space_at(1).space_id == "mario_kart_space_1"
```

**Step 2: Run test to verify it fails**

Run: `cd server && ../.venv/bin/pytest tests/test_monopoly_manual_rule_board_layout.py::test_manual_rule_space_lookup_uses_board_specific_space_ids -v`  
Expected: FAIL (still classic board).

**Step 3: Write minimal implementation**

```python
self._active_board_spaces = build_spaces_from_manual_rules(self.active_manual_rule_set)
self._active_space_by_id = {space.space_id: space for space in self._active_board_spaces}

# update _space_at and all SPACE_BY_ID call-sites to use active maps
```

**Step 4: Run test to verify it passes**

Run: `cd server && ../.venv/bin/pytest tests/test_monopoly_manual_rule_board_layout.py -v`  
Expected: PASS.

**Step 5: Commit**

```bash
git add server/games/monopoly/game.py server/tests/test_monopoly_manual_rule_board_layout.py
git commit -m "Drive Monopoly board spaces from manual board data"
```

### Task 6: Replace Static Deck Lists with Rule-Driven Deck Definitions

**Files:**
- Modify: `server/games/monopoly/game.py`
- Create: `server/tests/test_monopoly_manual_rule_decks.py`

**Step 1: Write the failing test**

```python
def test_manual_rule_decks_replace_classic_deck_ids(monkeypatch):
    game = _start_game(board_id="mario_kart", board_rules_mode="auto")
    assert game.chance_deck_order == ["mk_card_1", "mk_card_2"]
```

**Step 2: Run test to verify it fails**

Run: `cd server && ../.venv/bin/pytest tests/test_monopoly_manual_rule_decks.py::test_manual_rule_decks_replace_classic_deck_ids -v`  
Expected: FAIL (still classic deck IDs).

**Step 3: Write minimal implementation**

```python
if self.active_manual_rule_set is not None:
    self.chance_deck_order = [card["id"] for card in self.active_manual_rule_set.cards["chance"]]
    self.community_chest_deck_order = [card["id"] for card in self.active_manual_rule_set.cards["community_chest"]]
```

**Step 4: Run test to verify it passes**

Run: `cd server && ../.venv/bin/pytest tests/test_monopoly_manual_rule_decks.py -v`  
Expected: PASS.

**Step 5: Commit**

```bash
git add server/games/monopoly/game.py server/tests/test_monopoly_manual_rule_decks.py
git commit -m "Use manual board deck definitions for Chance and Community Chest"
```

### Task 7: Add Effect-Spec Execution for Board-Defined Cards

**Files:**
- Modify: `server/games/monopoly/game.py`
- Create: `server/tests/test_monopoly_manual_rule_card_effects.py`

**Step 1: Write the failing test**

```python
def test_manual_rule_card_effect_spec_applies_credit(monkeypatch):
    game = _start_game(board_id="mario_kart", board_rules_mode="auto")
    _force_draw(game, "mk_collect_100")
    _roll_to_card_space(game)
    assert game.current_player.cash == 1600
```

**Step 2: Run test to verify it fails**

Run: `cd server && ../.venv/bin/pytest tests/test_monopoly_manual_rule_card_effects.py::test_manual_rule_card_effect_spec_applies_credit -v`  
Expected: FAIL (legacy hardcoded card switch only).

**Step 3: Write minimal implementation**

```python
def _apply_manual_card_effect(self, player, effect_spec):
    kind = effect_spec["type"]
    if kind == "credit":
        self._credit_player(player, int(effect_spec["amount"]), "manual_card_credit")
        return "resolved"
    if kind == "debit":
        ...
```

**Step 4: Run test to verify it passes**

Run: `cd server && ../.venv/bin/pytest tests/test_monopoly_manual_rule_card_effects.py -v`  
Expected: PASS.

**Step 5: Commit**

```bash
git add server/games/monopoly/game.py server/tests/test_monopoly_manual_rule_card_effects.py
git commit -m "Add effect-spec executor for manual board card behavior"
```

### Task 8: Add Manual-Core Promotion Gate Tests

**Files:**
- Create: `server/tests/test_monopoly_manual_core_promotion_gate.py`
- Modify: `server/games/monopoly/board_parity.py`

**Step 1: Write the failing test**

```python
def test_manual_core_requires_validated_rule_set_and_citations(monkeypatch):
    profile = get_board_parity_profile("mario_kart")
    assert profile.fidelity_status != "manual_core"
```

**Step 2: Run test to verify it fails**

Run: `cd server && ../.venv/bin/pytest tests/test_monopoly_manual_core_promotion_gate.py -v`  
Expected: FAIL before gate exists.

**Step 3: Write minimal implementation**

```python
def can_promote_manual_core(board_id: str) -> bool:
    rule_set = load_manual_rule_set(board_id)
    return len(validate_manual_rule_set(rule_set)) == 0
```

**Step 4: Run test to verify it passes**

Run: `cd server && ../.venv/bin/pytest tests/test_monopoly_manual_core_promotion_gate.py -v`  
Expected: PASS.

**Step 5: Commit**

```bash
git add server/tests/test_monopoly_manual_core_promotion_gate.py server/games/monopoly/board_parity.py
git commit -m "Add manual-core promotion gate backed by citation validation"
```

### Task 9: Mario Manual Rule Data Artifacts

**Files:**
- Create: `server/games/monopoly/manual_rules/data/mario_collectors.json`
- Create: `server/games/monopoly/manual_rules/data/mario_kart.json`
- Create: `server/games/monopoly/manual_rules/data/mario_celebration.json`
- Create: `server/games/monopoly/manual_rules/data/mario_movie.json`
- Create: `server/games/monopoly/manual_rules/data/junior_super_mario.json`
- Create: `server/tests/test_monopoly_mario_manual_rule_data.py`

**Step 1: Write the failing test**

```python
@pytest.mark.parametrize("board_id", ["mario_collectors", "mario_kart", "mario_celebration", "mario_movie", "junior_super_mario"])
def test_mario_manual_rule_data_exists_and_validates(board_id):
    rule_set = load_manual_rule_set(board_id)
    assert validate_manual_rule_set(rule_set) == []
```

**Step 2: Run test to verify it fails**

Run: `cd server && ../.venv/bin/pytest tests/test_monopoly_mario_manual_rule_data.py -v`  
Expected: FAIL until data files exist.

**Step 3: Write minimal implementation**

```json
{
  "board_id": "mario_kart",
  "anchor_edition_id": "monopoly-e1870",
  "board": {"spaces": [{"position": 0, "space_id": "go", "kind": "start"}]},
  "economy": {"properties": {}},
  "cards": {"chance": [], "community_chest": []},
  "mechanics": {"type": "mario_gamer"},
  "win_condition": {"type": "score_target", "target": 0},
  "citations": [{"rule_path": "board.spaces", "edition_id": "monopoly-e1870", "page_ref": "p.2", "confidence": "high"}]
}
```

**Step 4: Run test to verify it passes**

Run: `cd server && ../.venv/bin/pytest tests/test_monopoly_mario_manual_rule_data.py -v`  
Expected: PASS.

**Step 5: Commit**

```bash
git add server/games/monopoly/manual_rules/data/mario_collectors.json server/games/monopoly/manual_rules/data/mario_kart.json server/games/monopoly/manual_rules/data/mario_celebration.json server/games/monopoly/manual_rules/data/mario_movie.json server/games/monopoly/manual_rules/data/junior_super_mario.json server/tests/test_monopoly_mario_manual_rule_data.py
git commit -m "Add manual-cited Mario board rule data artifacts"
```

### Task 10: Mario End-to-End Manual-Core Conformance

**Files:**
- Create: `server/tests/test_monopoly_mario_manual_core_conformance.py`
- Modify: `server/games/monopoly/board_parity.py`
- Modify: `docs/plans/2026-02-26-monopoly-special-boards-parity-matrix.md`

**Step 1: Write the failing test**

```python
@pytest.mark.parametrize("board_id", ["mario_collectors", "mario_kart", "mario_celebration", "mario_movie", "junior_super_mario"])
def test_mario_board_reaches_manual_core(board_id):
    profile = get_board_parity_profile(board_id)
    assert profile.fidelity_status == "manual_core"
```

**Step 2: Run test to verify it fails**

Run: `cd server && ../.venv/bin/pytest tests/test_monopoly_mario_manual_core_conformance.py -v`  
Expected: FAIL until promotion is complete.

**Step 3: Write minimal implementation**

```python
_FIDELITY_OVERRIDES.update({
    "mario_collectors": "manual_core",
    "mario_kart": "manual_core",
    "mario_celebration": "manual_core",
    "mario_movie": "manual_core",
})
```

**Step 4: Run test to verify it passes**

Run: `cd server && ../.venv/bin/pytest tests/test_monopoly_mario_manual_core_conformance.py -v`  
Expected: PASS.

**Step 5: Commit**

```bash
git add server/tests/test_monopoly_mario_manual_core_conformance.py server/games/monopoly/board_parity.py docs/plans/2026-02-26-monopoly-special-boards-parity-matrix.md
git commit -m "Promote Mario family boards to manual-core parity"
```

### Task 11: Create Family-Wave Rule Data for Remaining Boards

**Files:**
- Create: `server/games/monopoly/manual_rules/data/<board_id>.json` for each remaining special board
- Create: `server/tests/test_monopoly_special_board_manual_rule_data.py`

**Step 1: Write the failing test**

```python
@pytest.mark.parametrize("board_id", ALL_SPECIAL_NON_MARIO_BOARD_IDS)
def test_special_board_manual_rule_data_validates(board_id):
    rule_set = load_manual_rule_set(board_id)
    assert validate_manual_rule_set(rule_set) == []
```

**Step 2: Run test to verify it fails**

Run: `cd server && ../.venv/bin/pytest tests/test_monopoly_special_board_manual_rule_data.py -v`  
Expected: FAIL until all board artifacts are added.

**Step 3: Write minimal implementation**

```json
{
  "board_id": "star_wars_40th",
  "anchor_edition_id": "monopoly-c1990",
  "board": {"spaces": [...]},
  "economy": {"properties": {...}},
  "cards": {"chance": [...], "community_chest": [...]},
  "mechanics": {...},
  "win_condition": {...},
  "citations": [...]
}
```

**Step 4: Run test to verify it passes**

Run: `cd server && ../.venv/bin/pytest tests/test_monopoly_special_board_manual_rule_data.py -v`  
Expected: PASS.

**Step 5: Commit**

```bash
git add server/games/monopoly/manual_rules/data server/tests/test_monopoly_special_board_manual_rule_data.py
git commit -m "Add manual-cited rule data for remaining special Monopoly boards"
```

### Task 12: End-to-End Conformance for All Special Boards

**Files:**
- Create: `server/tests/test_monopoly_special_board_manual_core_conformance.py`
- Modify: `server/games/monopoly/board_parity.py`
- Modify: `server/games/monopoly/catalog/special_board_anchor_index.json`
- Modify: `docs/plans/2026-02-26-monopoly-special-boards-parity-matrix.md`

**Step 1: Write the failing test**

```python
@pytest.mark.parametrize("board_id", ALL_SPECIAL_BOARD_IDS)
def test_special_board_manual_core_or_near_full(board_id):
    profile = get_board_parity_profile(board_id)
    assert profile.fidelity_status in {"manual_core", "near_full"}
```

**Step 2: Run test to verify it fails**

Run: `cd server && ../.venv/bin/pytest tests/test_monopoly_special_board_manual_core_conformance.py -v`  
Expected: FAIL before final promotions.

**Step 3: Write minimal implementation**

```python
# update fidelity overrides after validated migration
_FIDELITY_OVERRIDES["star_wars_40th"] = "manual_core"
# ...and so on for each board
```

**Step 4: Run test to verify it passes**

Run: `cd server && ../.venv/bin/pytest tests/test_monopoly_special_board_manual_core_conformance.py -v`  
Expected: PASS.

**Step 5: Commit**

```bash
git add server/tests/test_monopoly_special_board_manual_core_conformance.py server/games/monopoly/board_parity.py server/games/monopoly/catalog/special_board_anchor_index.json docs/plans/2026-02-26-monopoly-special-boards-parity-matrix.md
git commit -m "Promote all special boards to manual-core or near-full parity"
```

### Task 13: Full Regression and Documentation Finalization

**Files:**
- Modify: `docs/plans/2026-02-26-monopoly-special-boards-parity-matrix.md`
- Modify: `docs/plans/2026-02-26-monopoly-mario-board-anchor-notes.md`
- Modify: `docs/plans/2026-02-26-monopoly-manual-core-all-special-boards-design.md` (status note)

**Step 1: Write failing verification checklist test (optional gate)**

```python
def test_all_manual_core_boards_have_citation_complete_status():
    assert load_manual_core_qa_report()["citation_errors"] == 0
```

**Step 2: Run focused and full tests**

Run:

```bash
cd server && ../.venv/bin/pytest \
  tests/test_monopoly_manual_rule_models.py \
  tests/test_monopoly_manual_rule_loader.py \
  tests/test_monopoly_manual_rule_validator.py \
  tests/test_monopoly_mario_manual_core_conformance.py \
  tests/test_monopoly_special_board_manual_core_conformance.py -v
cd server && ../.venv/bin/pytest -k monopoly -v
```

Expected: PASS.

**Step 3: Write final documentation updates**

```markdown
## Final Status
- all special boards promoted under strict manual-cited policy
- citation gate enabled in CI
- Pac-Man game-unit remains excluded
```

**Step 4: Verify docs and artifact consistency**

Run: `git diff -- docs/plans/2026-02-26-monopoly-special-boards-parity-matrix.md server/games/monopoly/catalog/special_board_anchor_index.json`  
Expected: status and fidelity rows are synchronized.

**Step 5: Commit**

```bash
git add docs/plans/2026-02-26-monopoly-special-boards-parity-matrix.md docs/plans/2026-02-26-monopoly-mario-board-anchor-notes.md docs/plans/2026-02-26-monopoly-manual-core-all-special-boards-design.md
git commit -m "Finalize strict manual-core parity rollout for special Monopoly boards"
```

### Task 14: Push and PR Readiness

**Files:**
- No code files; release hygiene only

**Step 1: Generate summary of migration coverage**

Run: `git log --oneline --decorate -n 20`  
Expected: clear wave-by-wave commit history.

**Step 2: Validate clean working tree**

Run: `git status --short`  
Expected: no output.

**Step 3: Push branch**

Run: `git push origin monopoly`  
Expected: push succeeds.

**Step 4: Prepare PR notes**

```markdown
- strict manual-cited rule engine
- mario-first full parity
- all remaining boards promoted with citation gates
- full monopoly regression passing
```

**Step 5: Commit (if PR notes tracked in repo)**

```bash
git add docs/plans
git commit -m "Add final PR handoff notes for manual-core rollout"
```

## Verification-before-completion
Use `@verification-before-completion` before any completion claim:
- keep command output evidence in handoff
- cite exact test commands and results
- do not report done unless full Monopoly regression passes
