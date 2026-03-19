# Card Game Helper Modernization Plan

Date: 2026-03-19
Branch: `main`
Status: proposed

## Goal
Modernize shared helper infrastructure for deck-based card games where it improves maintainability and consistency without flattening game-specific rules or changing gameplay behavior.

## Scope
### In scope
- Shared helper improvements for deck handling, dealing, turn timer/status helpers, and poker hand flow.
- Reuse opportunities across deck-based games, including:
  - `blackjack`
  - `holdem`
  - `fivecarddraw`
  - `crazyeights`
  - `scopa`
  - `ninetynine`
  - other future deck-based games using `server/game_utils/cards.py`
- Low-risk cleanup of duplicated helper logic inside games when it can move into focused mixins or utility modules.
- Documentation of boundaries between reusable infrastructure and game-specific rule engines.

### Out of scope
- Rule changes for any game.
- Save/load payload changes unless a later implementation phase proves they are necessary and separately approved.
- Rewriting all card games onto a single inheritance tree.
- Merging distinct game semantics into one generic card-game base class.
- Bot strategy changes except where helper signatures force a small adaptation.

## Constraints
- Gameplay behavior must remain unchanged.
- Existing action ids, keybind mappings, and localization keys should remain stable unless a change is explicitly justified.
- Shared helpers should stay narrow and explicit. Avoid adding a large abstract framework that obscures game flow.
- Implementation should proceed incrementally, with each phase independently testable and reversible.

## Current State Summary
- `server/game_utils/cards.py` provides core card and deck primitives plus basic formatting helpers.
- Poker already has a useful shared layer:
  - `poker_betting.py`
  - `poker_table.py`
  - `poker_actions.py`
  - `poker_showdown.py`
  - `poker_payout.py`
  - `poker_evaluator.py`
- The biggest duplication is between `holdem` and `fivecarddraw` in:
  - betting actions
  - turn/timer handling
  - pot resolution and showdown narration
  - chip/team score synchronization
  - common status actions
- Additional duplication exists across non-poker deck games in:
  - deck exhaustion and reshuffle patterns
  - round-robin dealing
  - card reading helpers
  - timer/status actions

## Design Principles
1. Extract infrastructure, not rules.
2. Prefer small mixins or helper modules over a monolithic card-game superclass.
3. Keep game state owned by each game dataclass.
4. Require explicit per-game hooks where logic diverges.
5. Treat `holdem` and `fivecarddraw` as the primary proving ground for poker helper expansion.

## Recommended Architecture
### 1. Expand `cards.py` into a slightly richer deck-operations layer
Add low-level, broadly reusable deck operations while keeping rule policy in games.

Candidate additions:
- `deal_round_robin(deck, players, cards_each, start_index=0)`
- `draw_with_refill(...)` or similarly explicit helpers for “draw, reshuffle/rebuild if empty”
- `reshuffle_discard_into_deck(deck, discard_pile, keep_top_discard=False)`
- utility helpers for common draw sound scheduling if they can be kept UI-agnostic or moved to a separate card UX mixin

Intended consumers:
- `holdem` hole-card and board dealing
- `fivecarddraw` opening and replacement dealing
- `crazyeights` empty-draw-pile recycle
- `ninetynine` discard-pile recycle
- `scopa` player deal loops
- `blackjack` shoe refill logic where appropriate

Non-goal:
- Do not hide game-specific shuffle/rebuild rules behind implicit behavior.

### 2. Add a focused `PokerStatusActionsMixin`
Extract duplicated status and validation helpers shared by poker games.

Candidate responsibilities:
- `_active_betting_ids()`
- `_all_in_ids()`
- `_require_active_player()`
- `_action_check_pot()`
- `_action_check_bet()`
- `_action_check_min_raise()`
- `_action_check_hand_players()`
- `_action_read_hand()`
- `_action_read_hand_value()`
- `_action_read_card()`
- `_action_check_turn_timer()`
- `_action_check_dealer()`
- `_action_check_position()`
- `_sync_team_scores()`

Initial consumers:
- `holdem`
- `fivecarddraw`

Rationale:
- These methods are already very close structurally.
- This reduces drift and avoids duplicate fixes.
- There is already evidence of duplication-related cleanliness issues in `fivecarddraw`.

### 3. Add a `PokerBettingFlowMixin`
Extract the repeated betting action implementations from `holdem` and `fivecarddraw`.

Candidate responsibilities:
- `_action_fold()`
- `_action_call()`
- `_action_raise()`
- `_action_all_in()`
- `_after_action()`
- `_advance_turn()`
- `_set_turn_by_index()`
- `_start_turn_timer()`
- `_handle_turn_timeout()` with per-game override hooks
- common pot-limit/no-limit raise handling

Required per-game hooks:
- `on_betting_round_complete()`
- `on_uncontested_win(active_ids)`
- `on_all_players_all_in()`
- `get_turn_skippable_state(player)`
- game-specific bot raise suggestion if needed

Rationale:
- This is the highest-value shared surface in current card code.
- `holdem` and `fivecarddraw` are close enough for a shared flow layer.
- The hook boundary is still narrow and understandable.

### 4. Add a `PokerHandLifecycleMixin`
Extract repeated new-hand and showdown infrastructure used by `holdem` and `fivecarddraw`.

Candidate responsibilities:
- queueing next hand
- resetting shared per-hand state
- base ante posting helper
- common showdown announcement entry point
- shared pot-resolution loop with injected hand scorer and hand-description formatter
- showdown line generation wrappers around `poker_showdown.py`

Required per-game hooks:
- `deal_opening_cards(active_players)`
- `start_first_betting_round()`
- `score_player_showdown_hand(player)`
- `describe_player_showdown_hand(player, locale)`
- any game-specific phase advancement

Rationale:
- The payout and showdown code is nearly duplicated.
- It belongs with the existing poker helper cluster rather than inside each game file.

### 5. Add a small card-presentation helper layer
Create a thin helper or mixin above `cards.py` for repetitive hand/card narration.

Candidate responsibilities:
- parse card slot/action suffixes
- speak card at slot
- speak full hand
- label card slot with localized card name
- optional sorted-hand helpers

Possible consumers:
- `holdem`
- `fivecarddraw`
- `blackjack`
- `ninetynine`
- `scopa`

Non-goal:
- Do not centralize all action-label logic. Only move repeated, clearly generic card-slot handling.

## What Should Stay Local To Games
These areas should remain game-specific and not be generalized beyond small utility support:
- Blackjack:
  - split-hand state
  - insurance/even-money/surrender logic
  - dealer play rules
  - payout rule profiles
- Crazy Eights:
  - wild-suit selection flow
  - special-card effects
  - hand/round sequencing
- Scopa:
  - capture search and ranking
  - scoring rules
  - initial-table constraints
- Ninety-Nine:
  - card value semantics by variant
  - token penalties
  - milestone logic

## Proposed Module Layout
Potential additions under `server/game_utils/`:
- `card_flow.py`
  - generic deck/deal/refill operations
- `card_presentation.py`
  - generic hand/card narration and slot helpers
- `poker_status_mixin.py`
  - shared poker status/UI helpers
- `poker_betting_flow_mixin.py`
  - shared poker betting action flow
- `poker_hand_lifecycle_mixin.py`
  - shared poker hand startup/showdown infrastructure

Potential updates:
- `cards.py`
- `__init__.py`
- targeted poker game imports/inheritance

## Phased Execution Plan
### Phase 1: Baseline cleanup and helper inventory
Goals:
- Document all duplicated helper clusters.
- Fix obvious local cleanliness issues with no behavior change.
- Establish naming conventions for new card helpers.

Tasks:
- Catalog duplicated poker helper methods between `holdem` and `fivecarddraw`.
- Catalog duplicated deck refill/deal logic across all deck-based games.
- Remove accidental duplicate local helpers where safe.
- Decide whether card UX helpers belong in `cards.py` or a sibling module.

Exit criteria:
- Clear inventory of candidate extractions.
- No behavior changes.

### Phase 2: Deck/deal helper extraction
Goals:
- Improve shared deck operations without changing rule ownership.

Tasks:
- Add round-robin dealing helper(s).
- Add explicit discard-to-deck reshuffle helper(s).
- Add optional draw-with-refill helper where semantics are stable.
- Migrate one or two low-risk consumers first.

Suggested first adopters:
- `ninetynine`
- `crazyeights`

Exit criteria:
- Shared deck operation helpers exist and are used in at least two games.
- No regression in local game rules.

### Phase 3: Poker status helper extraction
Goals:
- Eliminate repeated poker status methods with minimal risk.

Tasks:
- Introduce `PokerStatusActionsMixin`.
- Migrate `holdem`.
- Migrate `fivecarddraw`.
- Keep action names and menu behavior stable.

Exit criteria:
- Shared poker status surface is in one place.
- `holdem` and `fivecarddraw` retain current user-facing behavior.

### Phase 4: Poker betting flow extraction
Goals:
- Consolidate fold/call/raise/all-in logic and round progression behavior.

Tasks:
- Introduce `PokerBettingFlowMixin`.
- Define explicit per-game hooks for phase advancement.
- Migrate `holdem`.
- Migrate `fivecarddraw`.
- Preserve `poker_log` calls, sound cues, and localization keys.

Exit criteria:
- Betting action duplication is materially reduced.
- Per-game phase logic remains easy to follow.

### Phase 5: Poker hand lifecycle extraction
Goals:
- Consolidate hand reset, payout, showdown, and next-hand scheduling.

Tasks:
- Introduce `PokerHandLifecycleMixin`.
- Move common showdown/pot-resolution code behind narrow hooks.
- Keep board/deal specifics local to each game.

Exit criteria:
- `holdem` and `fivecarddraw` own their rules and phase transitions, not duplicated payout plumbing.

### Phase 6: Optional card-presentation layer
Goals:
- Reduce repeated card-slot narration code where it is clearly generic.

Tasks:
- Add helper functions for reading a card at a slot and building per-slot labels.
- Migrate only repeated call sites.

Exit criteria:
- Shared card narration helpers are useful and small.
- No framework sprawl.

## Rollout Order Recommendation
1. Baseline cleanup and inventory.
2. Deck/deal helpers.
3. Poker status mixin.
4. Poker betting flow mixin.
5. Poker hand lifecycle mixin.
6. Optional card-presentation helper extraction.

This order front-loads the lowest-risk, highest-signal extractions and delays the more structural poker refactors until helper boundaries are proven.

## Verification Strategy
For each phase:
1. Run targeted tests for touched games.
2. Run serialization/save-load checks for touched game states if any shared state code changes.
3. Exercise representative menu/status actions manually or through tests:
   - read hand
   - read card
   - check timer
   - dealer/button/position reporting
4. Validate bot turns still complete under timer pressure.
5. Confirm sound scheduling and turn progression still fire in the same order.

Suggested test slices:
- `holdem`
- `fivecarddraw`
- `blackjack`
- `crazyeights`
- `scopa`
- `ninetynine`

## Risks
- Over-generalizing too early could make game flow harder to follow.
- Shared helper hooks can become implicit and fragile if too many are introduced at once.
- Deck refill semantics differ enough that a “universal draw helper” may become misleading.
- Poker extraction may accidentally couple game-specific phase progression unless hook boundaries stay strict.

## Risk Mitigations
- Keep helpers small and explicit.
- Migrate one game pair at a time.
- Prefer helper functions first, mixins second, large abstractions last.
- Preserve existing public methods on game classes as thin wrappers during migration.
- Stop extraction if a helper needs too many conditionals for different games.

## Success Criteria
1. Deck-based card games share more low-level helper code where semantics truly match.
2. `holdem` and `fivecarddraw` lose a substantial amount of duplicated infrastructure code.
3. No game loses existing functionality or behavior.
4. Game files remain readable because rule logic stays local.
5. Shared modules describe stable infrastructure boundaries rather than becoming a second hidden rules engine.
