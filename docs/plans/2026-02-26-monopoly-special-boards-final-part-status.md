# Monopoly Special Boards Final-Part Completion Status and Follow-Up

Date: 2026-02-27  
Branch: `monopoly`  
Head: tracked via git history on `monopoly`

## Current Snapshot

- Special boards tracked: `55`
- Manual rule data files: `55` (`server/games/monopoly/manual_rules/data/*.json`)
- Fidelity statuses:
  - `manual_core`: `55`
  - `near_full`: `0`
- Boards with hardware capability flags: `junior_super_mario`, `mario_celebration`, `star_wars_mandalorian`, `jurassic_park`
- Pac-Man game-unit behavior remains intentionally out of scope.

## Verification Evidence (2026-02-27)

- `cd server && ../.venv/bin/pytest tests/test_monopoly_manual_rule_payload_completeness.py -v`
  - Result: `55 passed`
- `cd server && ../.venv/bin/pytest tests/test_monopoly_star_wars_manual_rule_payload.py tests/test_monopoly_disney_marvel_manual_rule_payload.py tests/test_monopoly_manual_card_draw_text.py tests/test_monopoly_manual_rule_payload_completeness.py -v`
  - Result: `222 passed`
- `cd server && ../.venv/bin/pytest tests/test_monopoly_special_board_manual_core_conformance.py tests/test_monopoly_special_board_anchor_index.py tests/test_monopoly_manual_core_fidelity_alignment.py tests/test_monopoly_hybrid_lane_exception_contract.py -q`
  - Result: `62 passed`
- `cd server && ../.venv/bin/pytest -k monopoly -q`
  - Result: `1286 passed, 598 deselected`

## Verification Evidence (2026-02-28)

- `cd server && nix shell nixpkgs#uv -c uv run --extra dev pytest tests/test_monopoly_hardware_emulation.py tests/test_monopoly_wave_special_audio_star_wars.py tests/test_monopoly_wave_special_audio_junior.py tests/test_monopoly_wave_special_audio_mario_celebration.py -q`
  - Result: `16 passed`
- `cd server && nix shell nixpkgs#uv -c uv run --extra dev pytest -k monopoly -q`
  - Result: `1295 passed, 598 deselected`

## New Progress: Hardware/Audio Mapping Expansion

- Added deterministic Junior Super Mario coin-sound hardware event wiring for manual-core power-up flow:
  - Runtime emits `junior_coin_sound_powerup` from `_apply_junior_super_mario_powerup(...)` when `junior_powerup_sound_ready` capability is active.
  - Event payload records `power_up_die` and resolved no-sound `outcome` for future emulated-sound parity work.
- Expanded hardware resolver support:
  - `server/games/monopoly/hardware_emulation.py` now recognizes `junior_coin_sound_powerup` and `mario_question_block_sound`.
  - Emulated events now include placeholder client sound asset paths:
    - `play_theme` -> `game_monopoly_hardware/play_theme_placeholder.ogg`
    - `star_wars_theme` -> `game_monopoly_hardware/star_wars_theme_placeholder.ogg`
    - `junior_coin_sound_powerup` -> `game_monopoly_hardware/junior_coin_sound_placeholder.ogg`
    - `mario_question_block_sound` -> `game_monopoly_hardware/mario_question_block_sound_placeholder.ogg`
  - Added Mario Celebration hardware event wiring:
    - Runtime emits `mario_question_block_sound` on Question Block (`chance`) draws when `question_block_sound_unit` capability is active.
    - Manual evidence source: `server/games/monopoly/manual_rules/extracted/mario_celebration.txt` (`Question Block Sound Unit` and explicit "What sound did you hear?" rules).
  - Placeholder provenance is tracked in `client/sounds/game_monopoly_hardware/README.md` and all entries are flagged for replacement with original captures later.
- Added verification coverage:
  - `server/tests/test_monopoly_wave_special_audio_junior.py`
  - Expanded `server/tests/test_monopoly_hardware_emulation.py` with Junior event emulation assertions.

## Verification Evidence (2026-02-28, Jurassic Park gate)

- `cd server && nix shell nixpkgs#uv -c uv run --extra dev pytest tests/test_monopoly_hardware_emulation.py tests/test_monopoly_wave_special_audio_star_wars.py tests/test_monopoly_wave_special_audio_junior.py tests/test_monopoly_wave_special_audio_mario_celebration.py tests/test_monopoly_wave_special_audio_jurassic_park.py -q`
  - Result: `24 passed`
- `cd server && nix shell nixpkgs#uv -c uv run --extra dev pytest -k monopoly -q`
  - Result: `1303 passed, 598 deselected`

## Verification Evidence (2026-02-28, Mario Celebration Question Block deeper mechanic)

- `cd server && nix shell nixpkgs#uv -c uv run --extra dev pytest tests/test_monopoly_hardware_emulation.py tests/test_monopoly_wave_special_audio_star_wars.py tests/test_monopoly_wave_special_audio_junior.py tests/test_monopoly_wave_special_audio_mario_celebration.py tests/test_monopoly_wave_special_audio_jurassic_park.py -q`
  - Result: `32 passed`
- `cd server && nix shell nixpkgs#uv -c uv run --extra dev pytest -k monopoly -q`
  - Result: `1311 passed, 598 deselected`

## New Progress: Mario Celebration Question Block Deeper Mechanic Modeling

- Replaced decorative `mario_question_block_sound` event with gameplay-affecting Question Block mechanic:
  - When a player lands on a Chance (Question Block) space on mario_celebration, the Chance card draw is entirely bypassed.
  - Instead, the Question Block Sound Unit resolves one of 4 outcomes using `random.randint(1, 6)`:
    - Roll 1-2 (33%): Coin Ping — collect 1-4 coins ($100-$400), event `mario_question_block_coin_ping`
    - Roll 3-4 (33%): Bowser's Laugh — pay Bank $500, event `mario_question_block_bowser`
    - Roll 5 (17%): Power-Up Ring — roll die and move again, resolve landed space, event `mario_question_block_power_up`
    - Roll 6 (17%): Game Over — pay Bank $1000, event `mario_question_block_game_over`
  - Outcome distribution matches the no-sound fallback die table from the manual (lines 86-93).
  - Mechanic is gated on `active_board_effective_mode == "board_rules"` and `question_block_sound_unit` capability.
  - Sound mode only controls audio playback; gameplay effects apply regardless.
- Manual evidence source: `server/games/monopoly/manual_rules/extracted/mario_celebration.txt` (lines 86-93, 342-356).
- New methods in `game.py`:
  - `_resolve_question_block_outcome()` — returns `(event_id, outcome_type, amount)` or `None`.
  - `_apply_question_block_outcome()` — emits hardware event and applies gameplay effect.
- Integration point: `_resolve_space()` chance handler — Question Block check before `_draw_card()`.
- Cleaned up `_resolve_card_hardware_event_id()` — removed mario_celebration branch (no longer needed).
- Old `mario_question_block_sound` event retained in sound profile registry for backward compatibility but no longer emitted at runtime.
- Added 4 new hardware events with sourced stand-in assets:
  - `mario_question_block_coin_ping.ogg` (8-Bit Sound Library, `Collect_Point_01.mp3`, CC-BY 3.0)
  - `mario_question_block_power_up.ogg` (8-Bit Sound Library, `Pickup_00.mp3`, CC-BY 3.0)
  - `mario_question_block_bowser.ogg` (8-Bit Sound Library, `Hit_00.mp3`, CC-BY 3.0)
  - `mario_question_block_game_over.ogg` (8-Bit Sound Library, `Hero_Death_00.mp3`, CC-BY 3.0)
- Added verification coverage:
  - `server/tests/test_monopoly_wave_special_audio_mario_celebration.py` rewritten with 7 tests (coin_ping credit, bowser debit, game_over debit, power_up movement, none-mode gameplay, non-QB board draws normally, deck index unchanged).
  - Expanded `server/tests/test_monopoly_hardware_emulation.py` with 4 new framework-level tests for Question Block event IDs.

## New Progress: Jurassic Park Electronic Gate Hardware Mapping

- Added Jurassic Park Electronic Gate mechanic — the gate outcome directly determines GO payout:
  - Every time a player passes or lands on GO, the gate randomly selects theme song ($200) or dinosaur roar ($100) with 50/50 odds.
  - New capability: `electronic_gate_sound_unit` added to jurassic_park board rules.
  - New hardware events: `jurassic_park_gate_theme`, `jurassic_park_gate_roar`.
  - Gate resolver: `_resolve_jurassic_park_gate_outcome()` in `game.py` returns `None` when not active, or `(event_id, cash)` tuple.
  - Integration point: `_move_player()` pass-GO block — after `_resolve_board_pass_go_credit`, gate overrides `pass_go_cash` and emits hardware event.
  - Key design: credit randomization happens regardless of sound mode; sound mode only controls audio playback.
- Manual evidence source: `server/games/monopoly/manual_rules/extracted/jurassic_park.txt` (lines 307-314, 346-352).
- Added sourced stand-in assets:
  - `jurassic_park_gate_theme.ogg` (OpenGameArt `sci-fi-sound-effects-library`, `Jingle_Achievement_00.mp3` transcoded to OGG, author Little Robot Sound Factory, CC-BY 3.0)
  - `jurassic_park_gate_roar.ogg` (OpenGameArt `sci-fi-sound-effects-library`, `Alarm_Loop_01.mp3` transcoded to OGG, author Little Robot Sound Factory, CC-BY 3.0)
- Added verification coverage:
  - `server/tests/test_monopoly_wave_special_audio_jurassic_park.py` (gate emits theme/roar, credit matches outcome, ignored in none mode, non-gate boards unaffected)
  - Expanded `server/tests/test_monopoly_hardware_emulation.py` with both gate event emulation assertions.

## New Progress: Sourced Stand-In Hardware Audio Assets

- Added runtime-preferred stand-in assets under `client/sounds/game_monopoly_hardware/original/`:
  - `play_theme.ogg` (OpenGameArt `electric-sound-effects-library`, `SpaceEngine_Start_01.mp3` transcoded to OGG, author Little Robot Sound Factory)
  - `star_wars_theme.ogg` (OpenGameArt `sci-fi-sound-effects-library`, `Jingle_Win_01.mp3` transcoded to OGG, author Little Robot Sound Factory)
  - `junior_coin_sound_powerup.ogg` (OpenGameArt `8-bit-sound-effects-library`, `Collect_Point_00.mp3` transcoded to OGG, author Little Robot Sound Factory)
  - `mario_question_block_sound.ogg` (OpenGameArt `8-bit-sound-effects-library`, `Collect_Point_00.mp3` transcoded to OGG, author Little Robot Sound Factory)
- Resolver behavior now actively uses `original/` assets when present and falls back to placeholders when absent.
- Provenance, source URLs, licenses, and SHA256 hashes are recorded in:
  - `client/sounds/game_monopoly_hardware/README.md`

## New Progress: Manual Source Extraction (All Special Boards)

- Added extractor: `server/scripts/monopoly/extract_manual_text.py`
- Added card-candidate miner: `server/scripts/monopoly/extract_manual_card_candidates.py`
- Added extracted artifacts:
  - `server/games/monopoly/manual_rules/extracted/manifest.json`
  - `server/games/monopoly/manual_rules/extracted/*.txt`
  - `server/games/monopoly/manual_rules/extracted/*.ocr.txt` (image-heavy manual sidecars)
  - `server/games/monopoly/manual_rules/extracted/*.json`
- Added coverage test:
  - `server/tests/test_monopoly_manual_source_extraction_artifacts.py`
- Extraction run status:
  - selected boards: `55`
  - extracted successfully: `55`
  - `marvel_flip` uses `strings_fallback` mode after bounded `pypdf` retry.
  - Preferred extraction metadata now records:
    - `preferred_text_path` / `preferred_text_sha256` / `preferred_text_source`
    - `ocr_text_path` / `ocr_text_sha256` when OCR sidecars are present.
- Rerun command:
  - `./.venv/bin/python server/scripts/monopoly/extract_manual_text.py --family ...` (all families from anchor index)
  - OCR-assisted rerun (optional): add `--ocr-when-text-below <chars>` and/or `--ocr-board-id <id>`.
  - Candidate-line extraction: `./.venv/bin/python server/scripts/monopoly/extract_manual_card_candidates.py --board-id <id>`
- Candidate coverage snapshot (all 55 boards):
  - zero candidates: `disney_the_edition`, `fortnite`, `marvel_flip`
  - low candidates (<=10): `disney_princesses` (5)
  - strongest candidate density examples: `disney_star_wars_dark_side` (73), `lord_of_the_rings` (69), `transformers_beast_wars` (60)

## New Progress: Payload Seeding from Extracted Manuals

- Added seed applier: `server/scripts/monopoly/apply_manual_extraction_seed.py`
- Applied extraction-backed metadata into all `55` special-board payloads:
  - `mechanics.manual_extraction` now records extraction mode, checksums, page count, and preferred/manual text artifact path.
  - `mechanics.manual_extraction` keeps raw and OCR-aware traceability fields (`raw_text_*`, `ocr_text_*`, `preferred_text_source`).
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
  - Includes extraction metadata coverage for all 55 boards plus Star/Marvel/Disney/Mario/long-tail label assertions.

## New Progress: Marvel Set Coverage

- Manual-extraction seed now covers the full Marvel board set with explicit action/deck labels where extract confidence is high:
  - `marvel_80_years`: `Catalog` + tax labels `Infinity Gauntlet`, `Cable & Deadpool`
  - `marvel_avengers`: `Stark Industries`, `Infinity Gauntlet`, tax labels `Ultron`, `Hela`
  - `marvel_avengers_legacy`: `S.H.I.E.L.D.`, `Villains`
  - `marvel_black_panther_wf`: `Wakandan`, `Talokanil`
  - `marvel_deadpool`: `Dumb Luck`, `Pouches`
  - `marvel_eternals`: `Uni-Mind`, `Arishem's Judgement`
  - `marvel_falcon_winter_soldier`: `The Shield`, `The Flag Smashers`
  - `marvel_flip`: `Event`, `Team-Up`
  - `marvel_spider_man`: `Daily Bugle`, `Spider-Sense`
  - `marvel_super_villains`: `Chance`, `Reshape the Universe`

## New Progress: Disney Set Coverage

- Manual-extraction seed now covers Disney boards with explicit action/deck labels where extract confidence is high:
  - `disney_animation`: `Magic Mirror`, `Ariel's Treasure Chest`; tax labels `The Evil Queen's Spell`, `Maleficent's Curse`
  - `disney_legacy`: `Show Time`, `Magic Moments`
  - `disney_lightyear`: `Hyperspeed`, `Crystallic Fusion`; tax labels `Bugs`, `Zyclops`
  - `disney_lion_king`: `Destiny`; tax labels `Water Fowl`, `Wild Fire`
  - `disney_mickey_friends`: `Friendship`, `Magic Moments`; tax labels `Hot Dog Snack Break`, `Popcorn Snack Break`
  - `disney_princesses`: `Sorte`, `Magia`; tax labels `Imposto`
  - `disney_the_edition`: `Show Time`, `Magic Moments`; tax labels `Scrooge McDuck's Tax`, `Prince John's Tax`
  - `disney_star_wars_dark_side`: `The Empire`, `The Dark Side`; tax labels `Rebel Escape`, `Rebel Attack`
  - `disney_villains`: `Chance`, `Poison Apple`

## New Progress: Long-Tail Set Coverage

- Added manual-derived action/deck labels for:
  - `animal_crossing`: `Chance`, `Nook Miles`
  - `barbie`: `Dream Career`, `Dream Closet`
  - `black_panther`: `Kimoyo Beads`, `Heart-Shaped Herb`
  - `deadpool_collectors`: `Dumb Luck`, `Pouches`
  - `fortnite`: `Storm`, `Loot Chest`
  - `fortnite_collectors`: `Storm`, `Loot Chest`
  - `fortnite_flip`: `Game Mode`, `Loot Chest`
  - `game_of_thrones`: `Chance Cards`; tax labels `The Dothraki Tribute`, `Iron Bank Tax`
  - `ghostbusters`: `Roaming Vapor`
  - `harry_potter`: `Owl Post`; tax labels `Filch and Mrs. Norris`
  - `junior_super_mario`: `Chance`
  - `jurassic_park`: `Impact Tremor`, `Cold Storage`
  - `lord_of_the_rings`: `Quest`
  - `lord_of_the_rings_trilogy`: `People`, `Event`
  - `pokemon`: `Adventure`, `Challenge`
  - `stranger_things`: `Walkie-Talkie`, `Blinking Lights`
  - `stranger_things_collectors`: `Transmission`, `Upside Down`
  - `stranger_things_netflix`: `Cerebro`, `Hellfire Club`
  - `toy_story`: `Toy Chest`, `The Claw`
  - `transformers`: `Autobot`, `Decepticon`
  - `transformers_beast_wars`: `Maximal`, `Predacon`
- Expanded Star Wars label/deck coverage beyond the original 4 boards:
  - `star_wars_40th`, `star_wars_boba_fett`, `star_wars_complete_saga`,
    `star_wars_light_side`, `star_wars_solo`, `star_wars_the_child`.
- Final Star Wars Saga labels are seeded from manual OCR:
  - `star_wars_saga`: `Sith`, `Jedi`; tax labels `Trade Blockade`, `Bounty`
- Literal manual card-text seeding coverage now includes canonical card text fields (`advance_to_go`, `go_to_jail`, `get_out_of_jail_free`) for:
  - Star Wars family (`12` boards): `disney_star_wars_dark_side`, `star_wars_40th`, `star_wars_boba_fett`, `star_wars_classic_edition`, `star_wars_complete_saga`, `star_wars_legacy`, `star_wars_light_side`, `star_wars_mandalorian`, `star_wars_mandalorian_s2`, `star_wars_saga`, `star_wars_solo`, `star_wars_the_child`
  - Disney/Marvel high-confidence subset (`15` boards): `disney_animation`, `disney_legacy`, `disney_lightyear`, `disney_lion_king`, `disney_mickey_friends`, `disney_princesses`, `disney_villains`, `marvel_80_years`, `marvel_avengers`, `marvel_black_panther_wf`, `marvel_deadpool`, `marvel_eternals`, `marvel_falcon_winter_soldier`, `marvel_spider_man`, `marvel_super_villains`
  - Disney mirror/manual fallback seeding: `disney_the_edition` (`advance_to_go`, `go_to_jail`, `get_out_of_jail_free`)
    - Source mirror used for literal text recovery: `https://www.manualsdir.com/manuals/613579/hasbro-monopoly-disney-edition-2010.html`
  - Additional partial seeding: `marvel_avengers_legacy`, `marvel_flip` (`go_to_jail` canonical card text in both decks)
  - The previously unresolved canonical slots on `marvel_avengers_legacy` and `marvel_flip` are now resolved in native deck rows via legacy-slot mapping with explicit text/evidence notes:
    - `shield_advance_to_go`
    - `villains_jail_release_options`
    - `event_advance_to_go`
    - `team_up_jail_release_options`
  - Native manual deck-id modeling is now active for the two remaining Marvel boards:
    - `marvel_avengers_legacy`: `shield_*` and `villains_*` card ids
    - `marvel_flip`: `event_*` and `team_up_*` card ids
  - Native manual deck-id modeling has now been expanded across the full Disney/Marvel family rollout boards via deck-name-prefixed ids plus `legacy_id` compatibility aliases.
  - Legacy canonical ids remain backward compatible via board rule remaps.
  - Runtime now resolves canonical compatibility ids to native deck ids by canonical card-slot index when board-specific manual decks are active.
  - Card-draw announcements now use `mechanics.decks` labels (for example `S.H.I.E.L.D.`, `Villains`, `Event`, `Team-Up`) instead of hardcoded `Chance`/`Community Chest` labels.
  - Option-2 kick-off: started replacing synthesized effects with manual-evidenced native effects by promoting `marvel_avengers_legacy` Villains slot-2 (`legacy_id=doctor_fee_pay_50`) to the board's verified `+215` credit outcome directly in native payload data.
  - Option-2 targeted OCR sweep (2026-02-27) re-ran high-DPI card/manual extraction for `marvel_avengers_legacy` and `marvel_flip`; those four native slots are now promoted from unresolved placeholders to explicit native text/effect rows using canonical-slot compatibility mapping plus OCR-backed evidence notes.
- Remaining boards without deck-label seeding: `0` (all `55` covered)

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
   - manual card draw text now supports literal `cards.*[].text` (with safe fallback to localized classic keys),
   - citation-backed promotion gate.
5. Special-board data payload completion was finished:
   - all `55` boards now have executable board/economy/card payloads with citations,
   - Mario family is promoted to `manual_core`,
   - Star Wars/Disney/Marvel payload expansions were merged,
   - initial manual-authentic metadata seeding was added for `marvel_avengers`.

## Final-Part Completion

The final-part promotion target is complete:

- all `55` special boards are now marked `manual_core` in parity and anchor artifacts;
- conformance tests enforce `manual_core` status across all special boards;
- cross-artifact alignment tests ensure parity + anchor index remain synchronized.

## New Progress: Card Text Seeding (2026-03-01)

- Seeded universal card text for 25 boards that previously had zero `"text"` fields on canonical cards:
  - Standard-$ boards (19): `animal_crossing`, `barbie`, `black_panther`, `deadpool_collectors`, `fortnite`, `fortnite_collectors`, `fortnite_flip`, `game_of_thrones`, `ghostbusters`, `harry_potter`, `jurassic_park`, `lord_of_the_rings`, `lord_of_the_rings_trilogy`, `stranger_things`, `stranger_things_collectors`, `stranger_things_netflix`, `toy_story`, `transformers`, `mario_collectors`
  - Themed-currency boards (6): `mario_celebration` (2 Coins), `mario_kart` (2 Coins), `mario_movie` (2 Coins), `junior_super_mario` (2 Coins), `pokemon` (2 Poké Balls), `transformers_beast_wars` (4 Energon)
- Each board received 4 `"text"` fields: `advance_to_go` (chance), `go_to_jail` (chance), `go_to_jail` (community_chest), `get_out_of_jail_free` (community_chest).
- Total text fields added: 100 (25 boards × 4 cards).
- All 55 boards now have universal card text coverage.

## New Progress: Cash Override Evidence Metadata (2026-03-01)

- Added `"text_note"` evidence annotation to 29 boards with non-empty `CARD_CASH_OVERRIDES`:
  - Format: `"Cash override active: board_rules <card_id> → <amount>. Source: manual-evidenced board economy."`
  - Covers `bank_dividend_50`, `income_tax_refund_20`, and `bank_error_collect_200` overrides.
- Fixed `mario_collectors` evidence: actual override is `bank_error_collect_200 → 250` (not `bank_dividend_50 → 120` as initially planned).
- Total text_note fields added: 29.

## Verification Evidence (2026-03-01, Card Text & Evidence Metadata)

- `cd server && nix shell nixpkgs#uv -c uv run --extra dev pytest tests/test_monopoly_card_text_coverage.py -q`
  - Result: `84 passed, 26 skipped`
- New test file: `server/tests/test_monopoly_card_text_coverage.py`
  - `test_all_boards_have_universal_card_text` — verifies every board has `"text"` on advance_to_go, go_to_jail, get_out_of_jail_free.
  - `test_cash_override_boards_have_evidence_notes` — verifies every board with non-empty `CARD_CASH_OVERRIDES` has `text_note` on the overridden card.

## Follow-Up Work

1. Continue manual-source quality improvements for image-heavy manuals and OCR stability.
2. Keep explicit evidence notes on inferred/legacy-slot-promoted literals where direct per-card scans are still noisy.
3. Expand hardware/audio mappings when manuals provide deterministic trigger behavior.
4. Keep parity matrix and plan docs synchronized with any future board-rule revisions.

## Current Blockers

- No blockers for `manual_core` status rollout remain.
- Ongoing limitation: direct per-card scan quality is still noisy on some image-heavy manuals, so a subset of card literals continue to rely on legacy-slot compatibility inference with OCR evidence notes.
- Environment-specific network/OCR tooling reliability can still affect extraction refresh throughput, but no longer blocks conformance due cached extraction fallback.

## Definition of Done for the Final Part

- `fidelity_status == manual_core` for all `55` special boards.
- Board/economy/card/mechanics payloads are manual-authentic per board.
- Citation coverage is complete and page-precise.
- Monopoly regression remains green.
