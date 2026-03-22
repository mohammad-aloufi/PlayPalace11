# Backgammon localization

game-name-backgammon = Backgammon

# Game start
backgammon-game-started = { $red } plays Red, { $white } plays White.
backgammon-opening-roll = Opening roll: { $red } rolls { $red_die }, { $white } rolls { $white_die }.
backgammon-opening-tie = Both rolled { $die }, re-rolling.
backgammon-opening-winner = { $player } goes first with { $die1 } and { $die2 }.

# Dice
backgammon-roll = { $player } rolls { $die1 } and { $die2 }.

# No moves
backgammon-no-moves = { $player } has no legal moves.

# Move commentary (shorthand)
backgammon-move-normal = { $player }: { $src } to { $dest }, { $remain } { $count }.
backgammon-move-emptying = { $player }: Emptying { $src } to { $dest }, { $count }.
backgammon-move-hit = { $player }: { $src } to capture on { $dest }, { $remain }.
backgammon-move-bar = { $player }: Bar to { $dest }, { $count }.
backgammon-move-bar-hit = { $player }: Bar to capture on { $dest }, { $count }.
backgammon-move-bearoff = { $player }: Bearing off from { $src }, { $remain }.

# Doubling
backgammon-doubles = { $player } doubles to { $value }.
backgammon-accepts = { $player } accepts.
backgammon-drops = { $player } drops.
backgammon-accept = Accept
backgammon-drop = Drop

# Selection feedback
backgammon-selected-point = Selected point { $point }, { $count } checkers.
backgammon-selected-bar = Selected bar.
backgammon-deselected = Deselected.
backgammon-no-checkers-there = No checkers there.
backgammon-no-moves-from-here = No legal moves from here.
backgammon-must-enter-from-bar = Must enter from bar first.
backgammon-illegal-move = Illegal move.
backgammon-nothing-to-undo = Nothing to undo.
backgammon-undone = Move undone.

# Hints
backgammon-hint = { $player } asks for a hint: { $hint }
backgammon-hint-not-now = Hints are only available during the moving phase.
backgammon-hints-disabled = Hints are disabled. Enable them in game options.
backgammon-hint-unavailable = Hint engine not available.
backgammon-gnubg-fallback = GNUBG engine unavailable. Bot is using simple fallback.

# Info keybinds
backgammon-check-status = Status
backgammon-check-pip = Pip count
backgammon-check-score = Score
backgammon-check-dice = Dice
backgammon-status = Red bar: { $bar_red }. White bar: { $bar_white }. Red off: { $off_red }. White off: { $off_white }. Dice: { $dice }.
backgammon-dice = { $dice }
backgammon-dice-none = No dice.
backgammon-pip-count = Red pip count: { $red_pip }. White pip count: { $white_pip }.
backgammon-match-score = { $red } { $red_score }, { $white } { $white_score }. Match to { $match_length }. Cube: { $cube }.

# Scoring
backgammon-wins-game = { $player } wins { $points } point{ $points ->
    [one] {""}
    *[other] s
}.
backgammon-new-game = Starting game { $number }.
backgammon-match-winner = { $player } wins the match!
backgammon-crawford = Crawford game: no doubling this game.
backgammon-resigns = { $player } resigns.
backgammon-resign = Resign

# Difficulty levels
backgammon-difficulty-random = Random
backgammon-difficulty-simple = Simple
backgammon-difficulty-gnubg-0ply = GNUBG 0-ply
backgammon-difficulty-gnubg-1ply = GNUBG 1-ply
backgammon-difficulty-gnubg-2ply = GNUBG 2-ply
backgammon-difficulty-whackgammon = Whackgammon

# Options
backgammon-option-match-length = Match length: { $match_length }
backgammon-option-select-match-length = Set match length (1-25)
backgammon-option-changed-match-length = Match length set to { $match_length }.
backgammon-option-bot-difficulty = Bot difficulty: { $bot_difficulty }
backgammon-option-select-bot-difficulty = Select bot difficulty
backgammon-option-changed-bot-difficulty = Bot difficulty set to { $bot_difficulty }.
backgammon-option-verbose-commentary = Verbose commentary: { $verbose_commentary }
backgammon-option-changed-verbose-commentary = Verbose commentary set to { $verbose_commentary }.
backgammon-option-hints = Hints: { $hints_enabled }
backgammon-option-changed-hints = Hints set to { $hints_enabled }.
