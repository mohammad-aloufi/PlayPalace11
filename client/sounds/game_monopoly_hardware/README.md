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
   - `client/sounds/game_monopoly_hardware/original/mario_question_block_sound.ogg`
   - `client/sounds/game_monopoly_hardware/original/jurassic_park_gate_theme.ogg`
   - `client/sounds/game_monopoly_hardware/original/jurassic_park_gate_roar.ogg`
   - `client/sounds/game_monopoly_hardware/original/mario_question_block_coin_ping.ogg`
   - `client/sounds/game_monopoly_hardware/original/mario_question_block_power_up.ogg`
   - `client/sounds/game_monopoly_hardware/original/mario_question_block_bowser.ogg`
   - `client/sounds/game_monopoly_hardware/original/mario_question_block_game_over.ogg`
   - `client/sounds/game_monopoly_hardware/original/pride_rock_celebration.ogg`
2. Runtime automatically prefers the `original/` asset when present and falls back to placeholder otherwise.
3. Optional helper script:
   - `uv run --project server --extra dev python -m server.scripts.monopoly.install_hardware_sound_replacement --event <event_id> --source /abs/path/file.ogg`
   - Add `--dry-run` to preview target path without copying.

## Current Sourced Stand-ins

Installed `original/` assets (runtime currently prefers these):

- `game_monopoly_hardware/original/play_theme.ogg`
  - Event: `play_theme`
  - Source: `https://opengameart.org/content/electric-sound-effects-library`
  - Direct file (pack): `https://opengameart.org/sites/default/files/Electric%20Sound%20Library.zip`
  - Original member: `Mp3/SpaceEngine/SpaceEngine_Start_01.mp3`
  - Conversion: transcoded MP3 -> OGG via `sox` for client runtime compatibility
  - Author: Little Robot Sound Factory
  - License: CC-BY 3.0
  - SHA256: `526727a5402cf9f99444347093f1789d27f15a6f3ed4fa43f38563acbdd560b0`

- `game_monopoly_hardware/original/star_wars_theme.ogg`
  - Event: `star_wars_theme`
  - Source: `https://opengameart.org/content/sci-fi-sound-effects-library`
  - Direct file (pack): `https://opengameart.org/sites/default/files/Sci-Fi%20Sound%20Library.zip`
  - Original member: `Sci-Fi Sound Library/Mp3/Jingle_Win_01.mp3`
  - Conversion: transcoded MP3 -> OGG via `sox` for client runtime compatibility
  - Author: Little Robot Sound Factory
  - License: CC-BY 3.0
  - SHA256: `e528de55318cb2a5357988aace63113e446e75658e411c6b23288f4cf536dc59`

- `game_monopoly_hardware/original/junior_coin_sound_powerup.ogg`
  - Event: `junior_coin_sound_powerup`
  - Source: `https://opengameart.org/content/8-bit-sound-effects-library`
  - Direct file (pack): `https://opengameart.org/sites/default/files/8-Bit%20Sound%20Library.zip`
  - Original member: `8-Bit Sound Library/Mp3/Collect_Point_00.mp3`
  - Conversion: transcoded MP3 -> OGG via `sox` for client runtime compatibility
  - Author: Little Robot Sound Factory
  - License: CC-BY 3.0
  - SHA256: `0039874caa6da78fcfc846505b11243254ff8cebca02fd1509810a7a16673a79`

- `game_monopoly_hardware/original/mario_question_block_sound.ogg`
  - Event: `mario_question_block_sound`
  - Source: `https://opengameart.org/content/8-bit-sound-effects-library`
  - Direct file (pack): `https://opengameart.org/sites/default/files/8-Bit%20Sound%20Library.zip`
  - Original member: `8-Bit Sound Library/Mp3/Collect_Point_00.mp3`
  - Conversion: transcoded MP3 -> OGG via `sox` for client runtime compatibility
  - Author: Little Robot Sound Factory
  - License: CC-BY 3.0
  - SHA256: `0039874caa6da78fcfc846505b11243254ff8cebca02fd1509810a7a16673a79`

- `game_monopoly_hardware/original/jurassic_park_gate_theme.ogg`
  - Event: `jurassic_park_gate_theme`
  - Source: `https://opengameart.org/content/sci-fi-sound-effects-library`
  - Direct file (pack): `https://opengameart.org/sites/default/files/Sci-Fi%20Sound%20Library.zip`
  - Original member: `Sci-Fi Sound Library/Mp3/Jingle_Achievement_00.mp3`
  - Conversion: transcoded MP3 -> OGG via `sox` for client runtime compatibility
  - Author: Little Robot Sound Factory
  - License: CC-BY 3.0
  - SHA256: `a5a6c940faaad6a0ce88675cdd4a7d275b9775f09dca7e187b44d0fc72ba7d3e`

- `game_monopoly_hardware/original/jurassic_park_gate_roar.ogg`
  - Event: `jurassic_park_gate_roar`
  - Source: `https://opengameart.org/content/sci-fi-sound-effects-library`
  - Direct file (pack): `https://opengameart.org/sites/default/files/Sci-Fi%20Sound%20Library.zip`
  - Original member: `Sci-Fi Sound Library/Mp3/Alarm_Loop_01.mp3`
  - Conversion: transcoded MP3 -> OGG via `sox` for client runtime compatibility
  - Author: Little Robot Sound Factory
  - License: CC-BY 3.0
  - SHA256: `1dc734d2d59a44c8a52ed2be8eb62d61b47197921ca12118445144c276be1d7d`

- `game_monopoly_hardware/original/mario_question_block_coin_ping.ogg`
  - Event: `mario_question_block_coin_ping`
  - Source: `https://opengameart.org/content/8-bit-sound-effects-library`
  - Direct file (pack): `https://opengameart.org/sites/default/files/8-Bit%20Sound%20Library.zip`
  - Original member: `8-Bit Sound Library/Mp3/Collect_Point_01.mp3`
  - Conversion: transcoded MP3 -> OGG via `sox` for client runtime compatibility
  - Author: Little Robot Sound Factory
  - License: CC-BY 3.0
  - SHA256: `5002bbe3882c81d4d456e881e715f8aabaf9e426069657715e29aa528bd024fd`

- `game_monopoly_hardware/original/mario_question_block_power_up.ogg`
  - Event: `mario_question_block_power_up`
  - Source: `https://opengameart.org/content/8-bit-sound-effects-library`
  - Direct file (pack): `https://opengameart.org/sites/default/files/8-Bit%20Sound%20Library.zip`
  - Original member: `8-Bit Sound Library/Mp3/Pickup_00.mp3`
  - Conversion: transcoded MP3 -> OGG via `sox` for client runtime compatibility
  - Author: Little Robot Sound Factory
  - License: CC-BY 3.0
  - SHA256: `a99e5712b3d9ee88d2b1d177a687f780019273278cf473aa4104c0c214a6d4d2`

- `game_monopoly_hardware/original/mario_question_block_bowser.ogg`
  - Event: `mario_question_block_bowser`
  - Source: `https://opengameart.org/content/8-bit-sound-effects-library`
  - Direct file (pack): `https://opengameart.org/sites/default/files/8-Bit%20Sound%20Library.zip`
  - Original member: `8-Bit Sound Library/Mp3/Hit_00.mp3`
  - Conversion: transcoded MP3 -> OGG via `sox` for client runtime compatibility
  - Author: Little Robot Sound Factory
  - License: CC-BY 3.0
  - SHA256: `f5b3ddd6dd910e61cecb6a52e9dd9db43955d0da1af9d98daa8e0081046e9ce4`

- `game_monopoly_hardware/original/mario_question_block_game_over.ogg`
  - Event: `mario_question_block_game_over`
  - Source: `https://opengameart.org/content/8-bit-sound-effects-library`
  - Direct file (pack): `https://opengameart.org/sites/default/files/8-Bit%20Sound%20Library.zip`
  - Original member: `8-Bit Sound Library/Mp3/Hero_Death_00.mp3`
  - Conversion: transcoded MP3 -> OGG via `sox` for client runtime compatibility
  - Author: Little Robot Sound Factory
  - License: CC-BY 3.0
  - SHA256: `3f91cb3790c16fba5186affd362aaabdffa5b0d9803d90c74869bd317385ad60`

- `game_monopoly_hardware/original/pride_rock_celebration.ogg`
  - Event: `pride_rock_celebration`
  - Source: `https://opengameart.org/content/sci-fi-sound-effects-library`
  - Direct file (pack): `https://opengameart.org/sites/default/files/Sci-Fi%20Sound%20Library.zip`
  - Original member: `Sci-Fi Sound Library/Mp3/Jingle_Win_00.mp3`
  - Conversion: transcoded MP3 -> OGG via `sox` for client runtime compatibility
  - Author: Little Robot Sound Factory
  - License: CC-BY 3.0
  - SHA256: `2ffb29330ef15beae154dea9345e1d83b8f230c774754f40fe813facafe9cd46`

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

- `mario_question_block_sound_placeholder.ogg`
  - Event: `mario_question_block_sound`
  - Current source: copied from `client/sounds/game_pig/bank.ogg`
  - Replacement needed: yes
  - Original target: `game_monopoly_hardware/original/mario_question_block_sound.ogg`

- `jurassic_park_gate_theme_placeholder.ogg`
  - Event: `jurassic_park_gate_theme`
  - Current source: copied from `client/sounds/game_pig/roundstart.ogg`
  - Replacement needed: yes
  - Original target: `game_monopoly_hardware/original/jurassic_park_gate_theme.ogg`

- `jurassic_park_gate_roar_placeholder.ogg`
  - Event: `jurassic_park_gate_roar`
  - Current source: copied from `client/sounds/game_pig/bank.ogg`
  - Replacement needed: yes
  - Original target: `game_monopoly_hardware/original/jurassic_park_gate_roar.ogg`

- `mario_question_block_coin_ping_placeholder.ogg`
  - Event: `mario_question_block_coin_ping`
  - Current source: copied from `client/sounds/game_pig/bank.ogg`
  - Replacement needed: yes
  - Original target: `game_monopoly_hardware/original/mario_question_block_coin_ping.ogg`

- `mario_question_block_power_up_placeholder.ogg`
  - Event: `mario_question_block_power_up`
  - Current source: copied from `client/sounds/game_pig/roundstart.ogg`
  - Replacement needed: yes
  - Original target: `game_monopoly_hardware/original/mario_question_block_power_up.ogg`

- `mario_question_block_bowser_placeholder.ogg`
  - Event: `mario_question_block_bowser`
  - Current source: copied from `client/sounds/game_pig/bank.ogg`
  - Replacement needed: yes
  - Original target: `game_monopoly_hardware/original/mario_question_block_bowser.ogg`

- `mario_question_block_game_over_placeholder.ogg`
  - Event: `mario_question_block_game_over`
  - Current source: copied from `client/sounds/game_pig/bank.ogg`
  - Replacement needed: yes
  - Original target: `game_monopoly_hardware/original/mario_question_block_game_over.ogg`

- `pride_rock_celebration_placeholder.ogg`
  - Event: `pride_rock_celebration`
  - Current source: copied from `client/sounds/game_monopoly_hardware/play_theme_placeholder.ogg`
  - Replacement needed: yes
  - Original target: `game_monopoly_hardware/original/pride_rock_celebration.ogg`
