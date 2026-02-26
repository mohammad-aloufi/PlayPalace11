# Monopoly Special Boards Final-Part Status and Remaining Work

Date: 2026-02-26  
Branch: `monopoly`  
Head: `35be7d3`

## Current Snapshot

- Special boards tracked: `55`
- Manual rule data files: `55` (`server/games/monopoly/manual_rules/data/*.json`)
- Fidelity statuses:
  - `manual_core`: `5`
  - `near_full`: `50`
- Boards with hardware capability flags: `junior_super_mario`, `star_wars_mandalorian`
- Pac-Man game-unit behavior remains intentionally out of scope.

## Verification Evidence (2026-02-26)

- `cd server && ../.venv/bin/pytest tests/test_monopoly_manual_rule_payload_completeness.py -v`
  - Result: `55 passed`
- `cd server && ../.venv/bin/pytest -k monopoly -q`
  - Result: `1111 passed, 598 deselected`

## New Progress: Manual Source Extraction (All Special Boards)

- Added extractor: `server/scripts/monopoly/extract_manual_text.py`
- Added extracted artifacts:
  - `server/games/monopoly/manual_rules/extracted/manifest.json`
  - `server/games/monopoly/manual_rules/extracted/*.txt`
  - `server/games/monopoly/manual_rules/extracted/*.json`
- Added coverage test:
  - `server/tests/test_monopoly_manual_source_extraction_artifacts.py`
- Extraction run status:
  - selected boards: `55`
  - extracted successfully: `55`
  - `marvel_flip` uses `strings_fallback` mode after bounded `pypdf` retry.
- Rerun command:
  - `./.venv/bin/python server/scripts/monopoly/extract_manual_text.py --family ...` (all families from anchor index)

## New Progress: Payload Seeding from Extracted Manuals

- Added seed applier: `server/scripts/monopoly/apply_manual_extraction_seed.py`
- Applied extraction-backed metadata into all `55` special-board payloads:
  - `mechanics.manual_extraction` now records extraction mode, checksums, page count, and text artifact path.
  - `citations` now include `mechanics.manual_extraction`.
- Applied manual-derived Star Wars action labels:
  - `star_wars_classic_edition`, `star_wars_legacy`: `Use the Force`, `Hyperspace`, `Galactic Empire Tax`
  - `star_wars_mandalorian`, `star_wars_mandalorian_s2`: `Signet`, `Hyperspace Jump`, `Imperial Credits`, `Imperial Advance`
- Applied manual-derived Mario action/deck labels:
  - `mario_celebration`: `Question Block`, `Community Chest`; tax labels `Chain Chomp`, `Piranha Plant`
  - `mario_collectors`: `? Block`, `Warp Pipe`
  - `mario_kart`: `Power-Up`, `Grand Prix`
  - `mario_movie`: `Question Block`, `Bowser's Fury`
- Added seed verification tests:
  - `server/tests/test_monopoly_manual_extraction_seed.py`
  - Includes extraction metadata coverage for all 55 boards plus Star/Marvel/Disney/Mario label assertions.

## New Progress: Marvel Set Coverage

- Manual-extraction seed now covers the full Marvel board set with explicit action/deck labels where extract confidence is high:
  - `marvel_80_years`: `Catalog` + tax labels `Infinity Gauntlet`, `Cable & Deadpool`
  - `marvel_avengers`: `Stark Industries`, `Infinity Gauntlet`, tax labels `Ultron`, `Hela`
  - `marvel_black_panther_wf`: `Wakandan`, `Talokanil`
  - `marvel_deadpool`: `Dumb Luck`, `Pouches`
  - `marvel_eternals`: `Uni-Mind`, `Arishem's Judgement`
  - `marvel_falcon_winter_soldier`: `The Shield`, `The Flag Smashers`
  - `marvel_spider_man`: `Daily Bugle`, `Spider-Sense`
  - `marvel_super_villains`: `Chance`, `Reshape the Universe`
- Known extraction-limited exceptions that remain on baseline labels pending stronger source parsing:
  - `marvel_avengers_legacy`
  - `marvel_flip` (currently `strings_fallback` extraction mode)

## New Progress: Disney Set Coverage

- Manual-extraction seed now covers Disney boards with explicit action/deck labels where extract confidence is high:
  - `disney_animation`: `Magic Mirror`, `Ariel's Treasure Chest`; tax labels `The Evil Queen's Spell`, `Maleficent's Curse`
  - `disney_legacy`: `Show Time`, `Magic Moments`
  - `disney_lightyear`: `Hyperspeed`, `Crystallic Fusion`; tax labels `Bugs`, `Zyclops`
  - `disney_lion_king`: `Destiny`; tax labels `Water Fowl`, `Wild Fire`
  - `disney_mickey_friends`: `Friendship`, `Magic Moments`; tax labels `Hot Dog Snack Break`, `Popcorn Snack Break`
  - `disney_princesses`: `Sorte`, `Magia`; tax labels `Imposto`
  - `disney_star_wars_dark_side`: `The Empire`, `The Dark Side`; tax labels `Rebel Escape`, `Rebel Attack`
  - `disney_villains`: `Chance`, `Poison Apple`
- Known extraction-limited Disney exception:
  - `disney_the_edition`

## What Has Been Done (Whole Rollout to Date)

1. Core Monopoly runtime and preset foundations were implemented (classic, junior, electronic banking, voice banking, cheaters, city).
2. Board selection/rules-mode, board profiles, and wave-based board rollouts were added.
3. Special-board parity framework was built:
   - anchor index/catalog artifacts,
   - deck provider framework,
   - hardware/sound-emulation scaffolding,
   - board-specific card behavior coverage across special families.
4. Manual-rule architecture was implemented:
   - rule schema models, loader, validator,
   - runtime board-rule resolution,
   - board-space/deck/effect execution from manual JSON payloads,
   - citation-backed promotion gate.
5. Special-board data payload completion was finished:
   - all `55` boards now have executable board/economy/card payloads with citations,
   - Mario family is promoted to `manual_core`,
   - Star Wars/Disney/Marvel payload expansions were merged,
   - initial manual-authentic metadata seeding was added for `marvel_avengers`.

## What the Final Part Is

Move the remaining `50` `near_full` boards to true `manual_core` by replacing synthesized placeholders with manual-authentic values per board edition:

- board-space labels and action behavior,
- Chance/Community-style card text and exact effects,
- economy and special-rule values,
- citation records tied to exact manual pages.

## Remaining Work

1. Manual source acquisition and indexing
   - Improve source quality for low-text extractions (`disney_the_edition`, `lord_of_the_rings_trilogy`, `marvel_avengers_legacy`, `star_wars_saga`) where current extracts are too sparse for reliable card-by-card promotion.
   - Continue tracking source path/checksum/edition mapping for reproducibility.
2. PDF extraction pipeline
   - Add a reproducible parser/OCR flow for image-heavy manuals and board-art-heavy PDFs.
   - Normalize extracted rules into `manual_rules/data/*.json`.
   - Preserve `manual excerpt -> rule_path` traceability.
3. Family-by-family manual-auth pass
   - Priority:
     1. Long-tail families with newly seeded extraction metadata (animal, barbie, black, deadpool, fortnite, game, ghostbusters, harry, jurassic, lord, pokemon, stranger, toy, transformers)
     2. Remaining extraction-limited exceptions in Marvel/Star/Disney
   - For each board: replace placeholders, update citations, then promote to `manual_core`.
4. Hardware and sound readiness continuity
   - Keep `hardware_capability_ids` aligned with manual evidence.
   - Continue audio-event mappings and stubs for later sound-pack integration.
   - Continue excluding Pac-Man game-unit emulation from this scope.
5. Conformance and docs synchronization
   - Add/extend tests that reject placeholder text for `manual_core` boards.
   - Keep parity matrix, anchor index, and backlog docs synchronized.

## Current Blockers

- `strings_fallback` extraction quality for `marvel_flip` is lower fidelity than structured PDF extraction.
- Several extracted manuals are image-heavy or layout-noisy, so card-by-card deterministic parsing still needs OCR/normalization work.

## Definition of Done for the Final Part

- `fidelity_status == manual_core` for all `55` special boards.
- Board/economy/card/mechanics payloads are manual-authentic per board.
- Citation coverage is complete and page-precise.
- Monopoly regression remains green.
