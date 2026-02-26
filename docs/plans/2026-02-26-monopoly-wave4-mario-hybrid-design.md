# Monopoly Wave 4 Mario Hybrid Design

Date: 2026-02-26
Branch: `monopoly`
Status: approved

## Goal
Expand strict Mario board support with meaningful gameplay differentiation while keeping runtime risk low. This wave keeps all current strict Mario boards available and upgrades two of them with concrete board-rule behavior beyond pass-GO override.

## Final Decisions
1. Strict Mario scope remains exactly five boards from the curated catalog.
2. This wave uses a hybrid strategy: broad coverage remains, with depth added to two high-impact boards.
3. New depth is implemented through deterministic card-behavior capabilities, not large engine rewrites.
4. `mario_kart` and `mario_movie` receive the first promoted behavior.
5. `mario_collectors`, `mario_celebration`, and `junior_super_mario` remain partial and safe-fallback in this wave.
6. Existing `auto` and `skin_only` board rules modes remain authoritative.

## Scope
### In scope
- Add two new board-rule capabilities:
  - `card_id_remap`
  - `card_cash_override`
- Wire capability lookup in registry and runtime.
- Implement both capabilities for:
  - `mario_kart`
  - `mario_movie`
- Add unit and integration tests for capability contracts and runtime behavior.
- Add/update Mario wave notes that record follow-on targets.

### Out of scope
- New non-Mario board onboarding in this wave.
- Full bespoke board engines for all Mario editions.
- UI option redesign.

## Strict Mario Board Set
- `mario_collectors` (`monopoly-c4382`)
- `mario_kart` (`monopoly-e1870`)
- `mario_celebration` (`monopoly-e9517`)
- `mario_movie` (`monopoly-f6818`)
- `junior_super_mario` (`monopoly-f4817`)

## Approaches Considered
1. Breadth-only (all strict Mario remain partial with no new mechanics).
2. Hybrid (selected): breadth plus targeted depth for two boards.
3. Full-depth now (all strict Mario mechanics implemented immediately).

### Selected Approach
Hybrid was chosen because it introduces visible gameplay difference now while preserving the existing low-risk, capability-gated architecture.

## Architecture
### Capability model extension
Keep rule packs data-driven and add two optional capability channels:

1. `card_id_remap`
- Input: `(rule_pack_id, deck_type, card_id)`
- Output: remapped `card_id` or original card when no mapping exists.

2. `card_cash_override`
- Input: `(rule_pack_id, card_id, default_amount)`
- Output: overridden amount when mapped; otherwise default.

### Rule-pack module contract
Mario packs can export deterministic dictionaries:
- `CARD_ID_REMAPS: dict[tuple[str, str], str]`
- `CARD_CASH_OVERRIDES: dict[str, int]`

Only `mario_kart` and `mario_movie` are populated this wave.

### Registry additions
Extend `board_rules_registry.py` with pure lookup helpers:
- `get_card_id_remap(rule_pack_id, deck_type, card_id) -> str`
- `get_card_cash_override(rule_pack_id, card_id) -> int | None`

Helpers must validate type and fall back safely.

### Runtime integration
In `MonopolyGame._resolve_card_effect`:
1. If board mode is not `board_rules`, skip all new behavior.
2. If board rule pack does not advertise the capability, skip.
3. Apply card remap before effect resolution.
4. Apply cash override where effect uses fixed cash amounts.

All other flow remains unchanged.

## Data Flow
1. Player lands on Chance or Community Chest.
2. Base card is drawn.
3. Runtime asks board rules for optional card remap.
4. Runtime resolves resulting card effect.
5. For money card effects, runtime asks board rules for optional cash override.
6. Broadcasts and state updates continue through existing paths.

## Error Handling and Fallbacks
- Missing rule pack or missing capability: use current default behavior.
- Invalid remap type or unknown target card: ignore and keep original card.
- Invalid cash override type or negative override: ignore and keep default amount.
- `skin_only` mode always bypasses new board-rule capabilities.

## Testing Strategy
### Unit tests
- Registry capability helpers:
  - known mapping returns expected remap/amount
  - missing mapping returns safe default
  - malformed module data is ignored safely

### Integration tests
- `board_rules` mode for `mario_kart` and `mario_movie` changes card outcome deterministically.
- Same scenario under `skin_only` remains unchanged.
- Existing pass-GO override behavior remains intact.

### Regression tests
- Run focused Mario + new capability tests.
- Run Monopoly regression (`-k monopoly`) to ensure no behavior regressions.

## Backlog Continuation
Record follow-on promotions after this wave:
1. Promote `mario_collectors` to use at least one new capability.
2. Promote `mario_celebration` similarly.
3. Define a Junior-safe Mario-specific mechanic track for `junior_super_mario`.

## Risks and Mitigations
1. Risk: Accidental cross-board side effects in card handling.
- Mitigation: capability gates and board-targeted tests.
2. Risk: Non-deterministic behavior from remap logic.
- Mitigation: static mapping tables and pure lookup helpers.
3. Risk: Localization drift for rule-pack status messaging.
- Mitigation: reuse existing board-rules simplified messaging in this wave.

## Success Criteria
1. `mario_kart` and `mario_movie` produce deterministic card behavior differences in `board_rules` mode.
2. `skin_only` mode behavior remains baseline.
3. All strict Mario boards remain selectable and start cleanly.
4. Monopoly regression suite remains green.
