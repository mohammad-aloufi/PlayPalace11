# Monopoly Manual-Core All Boards Design

Date: 2026-02-26

## Objective
Implement strict manual-cited parity for Monopoly special boards with a Mario-first execution strategy, then migrate all remaining special boards. Target full rules fidelity, including board layout/economy, card content/effects, board-specific mechanics, and win conditions.

## Scope Decisions
- Evidence policy: strict manual-cited only.
- Fidelity target: full mechanics parity (not card-only).
- Delivery strategy: Mario-first pilot on final framework, then family waves.
- Explicit exclusion: Pac-Man game-unit emulation remains out of scope.

## Delivery Shape
1. Track A: Build final framework for manual-cited rules data and runtime resolution.
2. Track B: Migrate boards in waves using that framework.
3. Board done criteria:
- Runtime behavior is board-data driven (no classic-rule fallback for covered behavior).
- Conformance tests pass for startup, movement, economy, cards, special mechanics, and endgame.
- Citation bundle is present and validates.
- Parity status promoted only when complete.

## Architecture
### 1) Rule Artifact Layer
Add per-board canonical rule artifacts containing:
- `board`: ordered spaces, space types, references.
- `economy`: price/rent/build/mortgage/bank rules.
- `cards`: board-specific decks, card text keys, effect specs.
- `mechanics`: board-specific toggles/handlers.
- `win_condition`: board-specific completion logic.
- `citations`: source metadata per rule (`edition_id`, page/anchor, note, confidence).

### 2) Runtime Resolver
Refactor board resolution to a single path:
- `resolve_active_board_rules(board_id, mode)` -> ruleset object.
- `skin_only` remains strict visual-only fallback.
- `board_rules` mode consumes resolved board rules for core gameplay.

### 3) Card Engine
- Replace fixed global Chance/Community lists with board-defined deck definitions.
- Keep a generic card effect executor driven by board-defined effect specs.
- Unsupported effect specs fail manual-core tests (no silent downgrade).

### 4) Evidence Gate
- Add validator(s) that block `manual_core` promotion if citations are incomplete/invalid.
- Require machine-checkable mapping from rule path to citation metadata.

### 5) Parity State Discipline
- `partial_plus`: partial manual-backed behavior.
- `manual_core`: complete core parity + validated citations.
- `near_full`: all known board-specific extras covered (excluding explicitly out-of-scope items).

## Migration Sequencing
### Phase 1: Framework
- Implement rule artifact format, resolver, card engine dispatch, citation validation gates.

### Phase 2: Mario Pilot (full parity)
- `mario_collectors`
- `mario_kart`
- `mario_celebration`
- `mario_movie`
- `junior_super_mario`

### Phase 3: Remaining board families
- Star Wars
- Disney/Marvel
- Fortnite/Stranger Things
- LOTR/Transformers/Toy Story and remaining long-tail boards

After each wave:
- Run board conformance tests + Monopoly full regression.
- Update parity artifacts and matrix.
- Promote statuses only after evidence and tests pass.

## Testing Strategy
Per-board conformance suite template:
- startup + mode resolution
- movement and space effects
- economy correctness (buy/rent/build/mortgage)
- card deck content and effect execution
- board-specific mechanics
- win-condition/endgame

Additional controls:
- deterministic golden snapshots for board economy/decks.
- citation-validation tests in CI.
- full `-k monopoly` regression after each wave.

## Error Handling Rules
- Incomplete board data or missing citations: board cannot be `manual_core`.
- Missing/invalid citation metadata: validator/test failure.
- Unsupported effect spec in manual-core path: explicit test failure.

## Non-Goals
- Pac-Man game-unit emulation.
- Best-guess promotion without manual evidence.

## Success Criteria
- Mario family reaches strict manual-core parity first.
- Remaining special boards follow same gate until all are promoted to manual-core/near-full with validated citations.
- Runtime no longer depends on classic-only board/card assumptions for covered special-board behavior.
