# PlayPalace Monopoly Handoff (for Claude)

## Session Goal
Continue Monopoly special-board parity/hardware audio work without losing context.

## Current Git State
- Repo: `/home/alek/git/PlayPalace`
- Branch: `monopoly`
- Worktree: clean
- Latest commit: `8da4b3f` (`Merge branch 'main' into monopoly`)

## Recent Commit Chain (newest first)
- `8da4b3f` Merge branch 'main' into monopoly
- `4374591` Implement Mario Celebration Question Block deeper mechanic modeling
- `69636e3` Add document browsing UI (read-only) to main menu
- `e386fbc` Fixed several spelling mistakes in the cards against humanity card data
- `086b0ca` Add focus_lang parameter to show_language_menu and fix duplicate @classmethod

## What Is Done
- All 55 special boards are `manual_core`.
- Hardware audio framework is in place with original/placeholder fallback.
- Legal-source stand-in assets are installed and documented.
- Deterministic Mario Celebration Question Block mechanic (4 outcomes, hardware events).
- Jurassic Park Electronic Gate mechanic (theme/roar pass-GO payout).
- Universal card text seeded across all 55 boards (advance_to_go, go_to_jail, get_out_of_jail_free).
- Cash override evidence metadata (`text_note`) on all 29 boards with `CARD_CASH_OVERRIDES`.
- Added/updated tests for registry, parity, hardware resolver, card text coverage, and wave audio behavior.

## Current Hardware Events
- `play_theme`
- `star_wars_theme`
- `junior_coin_sound_powerup`
- `mario_question_block_coin_ping`
- `mario_question_block_bowser`
- `mario_question_block_power_up`
- `mario_question_block_game_over`
- `jurassic_park_gate_theme`
- `jurassic_park_gate_roar`

## Key Files To Start From
- `server/games/monopoly/game.py`
- `server/games/monopoly/hardware_emulation.py`
- `server/games/monopoly/board_rules_registry.py`
- `server/games/monopoly/board_rules/mario_celebration.py`
- `server/tests/test_monopoly_card_text_coverage.py`
- `client/sounds/game_monopoly_hardware/README.md`
- `docs/plans/2026-02-26-monopoly-special-boards-final-part-status.md`
- `docs/plans/2026-02-28-monopoly-hardware-audio-legal-shortlist.md`

## Last Verification Results
- Card text coverage tests: `84 passed, 26 skipped`
- Note: full monopoly test suite currently blocked by broken `server.ui.keybinds` import (module moved to `server.core.ui.keybinds` in main merge at `8da4b3f`; import in `game.py` line 15 needs updating).

## Resume Commands
- Card text coverage:
  - `cd server && nix shell nixpkgs#uv -c uv run --extra dev pytest tests/test_monopoly_card_text_coverage.py -q`
- Targeted hardware/audio:
  - `cd server && nix shell nixpkgs#uv -c uv run --extra dev pytest tests/test_monopoly_hardware_emulation.py tests/test_monopoly_wave_special_audio_star_wars.py tests/test_monopoly_wave_special_audio_junior.py tests/test_monopoly_wave_special_audio_mario_celebration.py -q`
- Full Monopoly:
  - `cd server && nix shell nixpkgs#uv -c uv run --extra dev pytest -k monopoly -q`

## Recommended Next Work
- Fix broken `from ...ui.keybinds import KeybindState` in `game.py` (should be `from ...core.ui.keybinds import KeybindState` after main merge).
- Continue option-2 expansion: add hardware event mappings only where manual text shows deterministic sound-unit behavior.
- Keep legal-source stand-ins for new events with provenance in `client/sounds/game_monopoly_hardware/README.md`.
- Update parity/status docs each time a new hardware capability/event is added.

## Important Constraints
- Pac-Man game-unit behavior remains intentionally out of scope.
- Use manual evidence before enabling board hardware/audio capability flags.
- Keep old behavior safe: non-hardware boards should not emit hardware events.
