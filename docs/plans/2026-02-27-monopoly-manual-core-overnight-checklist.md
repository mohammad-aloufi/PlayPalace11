# Monopoly Manual-Core Overnight Checklist

Generated: 2026-02-27 04:32:26Z
Branch: `monopoly`

## Snapshot

- Total special boards: `55`
- `manual_core`: `55`
- `near_full`: `0`
- Pac-Man game-unit emulation remains out of scope.

## Completion Status

1. All tracked special boards are now promoted to `manual_core`.
2. Legacy-slot promotion policy remains explicit for image-heavy literal card text on `marvel_avengers_legacy` and `marvel_flip` (with OCR-backed evidence notes).
3. Junior Super Mario now emits deterministic coin-sound hardware events in `sound_mode=emulated`; Monopoly hardware runtime now prefers sourced `original/` stand-ins with placeholder fallback (`play_theme`, `star_wars_theme`, `junior_coin_sound_powerup`).
4. Stand-ins were refreshed toward board-style cues (short fanfare pair + 8-bit collect coin) using OpenGameArt licensed sources.
5. Source provenance, license notes, and checksums for stand-in originals are documented in `client/sounds/game_monopoly_hardware/README.md`.

## Board Checklist

| Priority | Family | Board | Anchor | Status | Track |
|---|---|---|---|---|---|
| P1 | `animal` | `animal_crossing` | `monopoly-f1661` | `manual_core` | `[x]` |
| P1 | `barbie` | `barbie` | `monopoly-g0038` | `manual_core` | `[x]` |
| P1 | `black` | `black_panther` | `monopoly-e5797` | `manual_core` | `[x]` |
| P1 | `deadpool` | `deadpool_collectors` | `monopoly-e4833` | `manual_core` | `[x]` |
| P2 | `disney` | `disney_animation` | `monopoly-c2116` | `manual_core` | `[x]` |
| P2 | `disney` | `disney_legacy` | `monopoly-19643` | `manual_core` | `[x]` |
| P2 | `disney` | `disney_lightyear` | `monopoly-f8046` | `manual_core` | `[x]` |
| P2 | `disney` | `disney_lion_king` | `monopoly-e6707` | `manual_core` | `[x]` |
| P2 | `disney` | `disney_mickey_friends` | `monopoly-f5267` | `manual_core` | `[x]` |
| P2 | `disney` | `disney_princesses` | `monopoly-b4644` | `manual_core` | `[x]` |
| P2 | `disney` | `disney_star_wars_dark_side` | `monopoly-f6167` | `manual_core` | `[x]` |
| P2 | `disney` | `disney_the_edition` | `monopoly-40224` | `manual_core` | `[x]` |
| P2 | `disney` | `disney_villains` | `monopoly-f0091` | `manual_core` | `[x]` |
| P1 | `fortnite` | `fortnite` | `monopoly-e6603` | `manual_core` | `[x]` |
| P1 | `fortnite` | `fortnite_collectors` | `monopoly-f2546` | `manual_core` | `[x]` |
| P1 | `fortnite` | `fortnite_flip` | `monopoly-f7774` | `manual_core` | `[x]` |
| P1 | `game` | `game_of_thrones` | `monopoly-e3278` | `manual_core` | `[x]` |
| P1 | `ghostbusters` | `ghostbusters` | `monopoly-e9479` | `manual_core` | `[x]` |
| P1 | `harry` | `harry_potter` | `monopoly-f9422` | `manual_core` | `[x]` |
| P3 | `junior` | `junior_super_mario` | `monopoly-f4817` | `manual_core` | `[x]` |
| P1 | `jurassic` | `jurassic_park` | `monopoly-f1662` | `manual_core` | `[x]` |
| P1 | `lord` | `lord_of_the_rings` | `monopoly-f1663` | `manual_core` | `[x]` |
| P1 | `lord` | `lord_of_the_rings_trilogy` | `monopoly-41603` | `manual_core` | `[x]` |
| P3 | `mario` | `mario_celebration` | `monopoly-e9517` | `manual_core` | `[x]` |
| P3 | `mario` | `mario_collectors` | `monopoly-c4382` | `manual_core` | `[x]` |
| P3 | `mario` | `mario_kart` | `monopoly-e1870` | `manual_core` | `[x]` |
| P3 | `mario` | `mario_movie` | `monopoly-f6818` | `manual_core` | `[x]` |
| P2 | `marvel` | `marvel_80_years` | `monopoly-e7866` | `manual_core` | `[x]` |
| P2 | `marvel` | `marvel_avengers` | `monopoly-e6504` | `manual_core` | `[x]` |
| P2 | `marvel` | `marvel_avengers_legacy` | `monopoly-b0323` | `manual_core` | `[x]` |
| P2 | `marvel` | `marvel_black_panther_wf` | `monopoly-f5405` | `manual_core` | `[x]` |
| P2 | `marvel` | `marvel_deadpool` | `monopoly-e2033` | `manual_core` | `[x]` |
| P2 | `marvel` | `marvel_eternals` | `monopoly-f1659` | `manual_core` | `[x]` |
| P2 | `marvel` | `marvel_falcon_winter_soldier` | `monopoly-f5851` | `manual_core` | `[x]` |
| P2 | `marvel` | `marvel_flip` | `monopoly-f9931` | `manual_core` | `[x]` |
| P2 | `marvel` | `marvel_spider_man` | `monopoly-f3968` | `manual_core` | `[x]` |
| P2 | `marvel` | `marvel_super_villains` | `monopoly-f5270` | `manual_core` | `[x]` |
| P1 | `pokemon` | `pokemon` | `monopoly-g0716` | `manual_core` | `[x]` |
| P2 | `star` | `star_wars_40th` | `monopoly-c1990` | `manual_core` | `[x]` |
| P2 | `star` | `star_wars_boba_fett` | `monopoly-f5394` | `manual_core` | `[x]` |
| P2 | `star` | `star_wars_classic_edition` | `monopoly-b8613` | `manual_core` | `[x]` |
| P2 | `star` | `star_wars_complete_saga` | `monopoly-e8066` | `manual_core` | `[x]` |
| P2 | `star` | `star_wars_legacy` | `monopoly-b0324` | `manual_core` | `[x]` |
| P2 | `star` | `star_wars_light_side` | `monopoly-f8383` | `manual_core` | `[x]` |
| P2 | `star` | `star_wars_mandalorian` | `monopoly-f1276` | `manual_core` | `[x]` |
| P2 | `star` | `star_wars_mandalorian_s2` | `monopoly-f4257` | `manual_core` | `[x]` |
| P2 | `star` | `star_wars_saga` | `monopoly-42452` | `manual_core` | `[x]` |
| P2 | `star` | `star_wars_solo` | `monopoly-e1702` | `manual_core` | `[x]` |
| P2 | `star` | `star_wars_the_child` | `monopoly-f2013` | `manual_core` | `[x]` |
| P1 | `stranger` | `stranger_things` | `monopoly-c4550` | `manual_core` | `[x]` |
| P1 | `stranger` | `stranger_things_collectors` | `monopoly-e8194` | `manual_core` | `[x]` |
| P1 | `stranger` | `stranger_things_netflix` | `monopoly-f2544` | `manual_core` | `[x]` |
| P1 | `toy` | `toy_story` | `monopoly-e5065` | `manual_core` | `[x]` |
| P1 | `transformers` | `transformers` | `monopoly-f1660` | `manual_core` | `[x]` |
| P1 | `transformers` | `transformers_beast_wars` | `monopoly-f5269` | `manual_core` | `[x]` |

## Completed Boards

- [x] `animal_crossing`
- [x] `barbie`
- [x] `black_panther`
- [x] `deadpool_collectors`
- [x] `disney_animation`
- [x] `disney_legacy`
- [x] `disney_lightyear`
- [x] `disney_lion_king`
- [x] `disney_mickey_friends`
- [x] `disney_princesses`
- [x] `disney_star_wars_dark_side`
- [x] `disney_the_edition`
- [x] `disney_villains`
- [x] `fortnite`
- [x] `fortnite_collectors`
- [x] `fortnite_flip`
- [x] `game_of_thrones`
- [x] `ghostbusters`
- [x] `harry_potter`
- [x] `jurassic_park`
- [x] `lord_of_the_rings`
- [x] `lord_of_the_rings_trilogy`
- [x] `marvel_80_years`
- [x] `marvel_avengers`
- [x] `marvel_avengers_legacy`
- [x] `marvel_black_panther_wf`
- [x] `marvel_deadpool`
- [x] `marvel_eternals`
- [x] `marvel_falcon_winter_soldier`
- [x] `marvel_flip`
- [x] `marvel_spider_man`
- [x] `marvel_super_villains`
- [x] `pokemon`
- [x] `star_wars_40th`
- [x] `star_wars_boba_fett`
- [x] `star_wars_classic_edition`
- [x] `star_wars_complete_saga`
- [x] `star_wars_legacy`
- [x] `star_wars_light_side`
- [x] `star_wars_mandalorian`
- [x] `star_wars_mandalorian_s2`
- [x] `star_wars_saga`
- [x] `star_wars_solo`
- [x] `star_wars_the_child`
- [x] `stranger_things`
- [x] `stranger_things_collectors`
- [x] `stranger_things_netflix`
- [x] `toy_story`
- [x] `transformers`
- [x] `transformers_beast_wars`

## Overnight Runbook

Use this when you are away. It runs extraction/verification loops and leaves logs for review.

```bash
set -euo pipefail
cd /home/alek/git/PlayPalace
mkdir -p /tmp/monopoly-overnight-logs

# Optional: run inside tmux so it survives disconnects
# tmux new -s monopoly-night

# 1) Re-extract manual text sidecars (all special-board families)
./.venv/bin/python server/scripts/monopoly/extract_manual_text.py \
  --family animal --family barbie --family black --family deadpool --family disney \
  --family fortnite --family game --family ghostbusters --family harry --family junior \
  --family jurassic --family lord --family mario --family marvel --family pokemon \
  --family star --family stranger --family toy --family transformers \
  --ocr-when-text-below 4000 \
  > /tmp/monopoly-overnight-logs/extract.log 2>&1

# 2) Refresh card-candidate artifacts for all boards
./.venv/bin/python server/scripts/monopoly/extract_manual_card_candidates.py \
  > /tmp/monopoly-overnight-logs/candidates.log 2>&1

# 3) Run Monopoly regressions
cd server
../.venv/bin/pytest -k monopoly -q > /tmp/monopoly-overnight-logs/pytest-monopoly.log 2>&1
../.venv/bin/pytest tests/test_monopoly_manual_rule_payload_completeness.py -q > /tmp/monopoly-overnight-logs/pytest-payload.log 2>&1

# 4) Quick summary
tail -n 40 /tmp/monopoly-overnight-logs/pytest-monopoly.log
tail -n 40 /tmp/monopoly-overnight-logs/pytest-payload.log
```

## Done Criteria Per Board

- Manual-auth board/economy/cards/mechanics values confirmed against source manual text.
- `cards` rows use native deck IDs (with `legacy_id` compatibility where needed).
- Citations are page-precise and complete.
- Board-specific tests plus `pytest -k monopoly -q` are green.
