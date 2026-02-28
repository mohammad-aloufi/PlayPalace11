# Monopoly Hardware Sound Assets

This folder contains temporary placeholder sounds and optional sourced stand-ins for
Monopoly hardware-emulation events.

The sourced stand-ins are not board-authentic captures. They keep gameplay audible until
original board captures are sourced and licensed.

## Original Intake Pipeline

No code changes are required to swap in originals.

1. Put an original capture at one of these target paths:
   - `client/sounds/game_monopoly_hardware/original/play_theme.ogg`
   - `client/sounds/game_monopoly_hardware/original/star_wars_theme.ogg`
   - `client/sounds/game_monopoly_hardware/original/junior_coin_sound_powerup.ogg`
2. Runtime automatically prefers the `original/` asset when present and falls back to placeholder otherwise.
3. Optional helper script:
   - `uv run --project server --extra dev python -m server.scripts.monopoly.install_hardware_sound_replacement --event <event_id> --source /abs/path/file.ogg`
   - Add `--dry-run` to preview target path without copying.

## Current Sourced Stand-ins

Installed `original/` assets (runtime currently prefers these):

- `game_monopoly_hardware/original/play_theme.ogg`
  - Event: `play_theme`
  - Source: `https://opengameart.org/content/fanfares`
  - Direct file: `https://opengameart.org/sites/default/files/TITLE%20BOUT_0.ogg`
  - Author: Spring Spring
  - License: CC-BY 4.0 / CC-BY 3.0 / CC-BY-SA 4.0 / CC-BY-SA 3.0 (asset page offers multiple; project uses attribution model)
  - SHA256: `657f76c74d869ff935837a03e3b33d81f31056f1d67eeddf906bee53095369df`

- `game_monopoly_hardware/original/star_wars_theme.ogg`
  - Event: `star_wars_theme`
  - Source: `https://opengameart.org/content/fanfares`
  - Direct file: `https://opengameart.org/sites/default/files/WIN_AGAINST_CHAMPION_0.ogg`
  - Author: Spring Spring
  - License: CC-BY 4.0 / CC-BY 3.0 / CC-BY-SA 4.0 / CC-BY-SA 3.0 (asset page offers multiple; project uses attribution model)
  - SHA256: `6af3e4d45e22c2b2e46d4fbb04ea3e691c1991f2199eef50283f5918c87b7766`

- `game_monopoly_hardware/original/junior_coin_sound_powerup.ogg`
  - Event: `junior_coin_sound_powerup`
  - Source: `https://opengameart.org/content/8-bit-sound-effects-library`
  - Direct file (pack): `https://opengameart.org/sites/default/files/8-Bit%20Sound%20Library.zip`
  - Original member: `8-Bit Sound Library/Mp3/Collect_Point_00.mp3`
  - Conversion: transcoded MP3 -> OGG via `sox` for client runtime compatibility
  - Author: Little Robot Sound Factory
  - License: CC-BY 3.0
  - SHA256: `0039874caa6da78fcfc846505b11243254ff8cebca02fd1509810a7a16673a79`

## Mapping

- `play_theme_placeholder.ogg`
  - Event: `play_theme`
  - Current source: copied from `client/sounds/game_pig/roundstart.ogg`
  - Replacement needed: yes
  - Original target: `game_monopoly_hardware/original/play_theme.ogg`

- `star_wars_theme_placeholder.ogg`
  - Event: `star_wars_theme`
  - Current source: copied from `client/sounds/game_pig/roundstart.ogg`
  - Replacement needed: yes
  - Original target: `game_monopoly_hardware/original/star_wars_theme.ogg`

- `junior_coin_sound_placeholder.ogg`
  - Event: `junior_coin_sound_powerup`
  - Current source: copied from `client/sounds/game_pig/bank.ogg`
  - Replacement needed: yes
  - Original target: `game_monopoly_hardware/original/junior_coin_sound_powerup.ogg`
