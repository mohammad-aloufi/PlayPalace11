# Monopoly Junior Variants Design (2026-02-26)

## Goal

Add two selectable Junior presets with near-complete fidelity and anchor-first manual policy:

- `junior_modern` (canonical anchor: newest verified Junior manual, `monopoly-f8562`)
- `junior_legacy` (canonical anchor: oldest Junior manual, `monopoly-00441`)

This phase is board-first and targets playable + near-complete rules fidelity for both Junior baselines.

## Confirmed Decisions

1. Work track: board-first variant expansion.
2. Fidelity phase now: playable core fidelity, expanded to near-complete scope for Junior.
3. Future phase: maximum fidelity after this phase lands.
4. Junior must support both modern and legacy baselines.
5. Delivery model: separate preset IDs, not a nested lobby toggle.
6. Conflict policy: anchor-first.
7. Anchor mapping:
   - `junior_modern` -> `monopoly-f8562`
   - `junior_legacy` -> `monopoly-00441`

## Approach

Recommended and approved approach: shared Junior engine with profile-driven behavior.

Why:

- avoids duplicate implementations,
- keeps divergence explicit and testable,
- scales to additional Junior family quirks without polluting classic flow.

## Architecture

### Preset Layer

- Extend selectable preset catalog/aliases to include:
  - `junior_modern`
  - `junior_legacy`
- Preserve existing `junior` compatibility behavior (if needed) via explicit mapping to one of the new IDs.

### Runtime Dispatch

- Keep current Monopoly flow for non-Junior presets.
- Add Junior runtime branch selected by preset profile.
- Junior branch owns:
  - movement semantics,
  - purchase/rent/payment handling,
  - jail/card/special-space behavior,
  - game-end trigger and winner computation.

### Ruleset Profiles

Introduce structured Junior ruleset profiles keyed by preset ID:

- `JuniorRulesetProfile("junior_modern")`
- `JuniorRulesetProfile("junior_legacy")`

Each profile provides:

- dice model,
- economy model (cash/start/payments),
- ownership model,
- cards and special spaces behavior,
- jail model,
- endgame policy,
- anchor provenance metadata.

## Data Model

### Rule Data

Store normalized Junior rule groups for each ruleset:

- `movement_rules`
- `money_supply_rules`
- `purchase_and_rent_rules`
- `card_and_special_space_rules`
- `jail_rules`
- `game_end_rules`

For each group record:

- `source_anchor_edition_id`
- optional source references/notes used for implementation traceability.

### Conflict and Fallback Records

For near-complete fidelity with anchor-first policy:

- keep explicit conflict resolution notes where non-anchor manuals differ,
- keep explicit fallback notes when anchor text is missing/ambiguous.

Fallback priority:

1. anchor-adjacent rule evidence in same edition family,
2. Junior family consensus,
3. deterministic safe default.

No silent merges.

### State and Serialization

Add only minimal Junior-specific state needed for gameplay.

- All new fields must have safe defaults for old saves.
- Classic and existing variant saves remain compatible.

## Runtime Flow

1. Start game:
   - resolve preset,
   - resolve Junior ruleset (if Junior preset),
   - initialize Junior-specific economy/state.
2. Turn:
   - if Junior preset: execute Junior turn pipeline,
   - else: current Monopoly pipeline unchanged.
3. Menus/actions:
   - reuse stable action IDs where possible,
   - show/hide/enable by ruleset constraints,
   - suppress incompatible classic-only actions under Junior.
4. Bot behavior:
   - Junior-specific decision path,
   - ruleset-aware economy/endgame heuristics.
5. Endgame:
   - evaluate exactly by selected Junior ruleset policy.

## Error Handling and Guardrails

- Unknown/invalid Junior preset resolves to deterministic safe fallback with explicit note.
- Impossible action states return localized errors, not silent no-op behavior.
- Junior branch isolation prevents behavior regression in classic/speed/builder/etc.

## Testing Strategy

### Unit Tests

- preset resolution and anchor mapping,
- ruleset profile loading and provenance fields,
- per-ruleset movement/economy/rent/cards/jail/endgame behavior.

### Scenario/Play Tests

- deterministic full-turn sequences for `junior_modern` and `junior_legacy`,
- divergent-rule edge cases proving modern vs legacy behavior differences.

### Bot Tests

- baseline turn decisions in Junior context,
- no deadlocks/stalls in Junior loops.

### Regression Tests

- existing Monopoly suites remain green,
- serialization compatibility for added state fields.

## Acceptance Criteria

1. Both presets are selectable and playable end-to-end.
2. Implemented rules match anchor-manual behavior for covered mechanics.
3. Conflict/fallback decisions are explicitly documented and test-backed.
4. Monopoly test subset passes without regressions.

## Out of Scope for This Design

- Non-Junior remaining variants (`cheaters`, `electronic_banking`, `voice_banking`, `city`) implementation details.
- Spin-off families (`bid_card_game`, `deal_card_game`, `knockout`).
- Maximum-fidelity extras beyond this near-complete Junior phase.

## Next Step

Create a detailed implementation plan (task breakdown, sequencing, validation gates) using the writing-plans workflow before coding.
