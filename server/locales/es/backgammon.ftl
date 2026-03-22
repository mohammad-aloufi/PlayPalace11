# Localización de Backgammon

game-name-backgammon = Backgammon

# Inicio de partida
backgammon-game-started = { $red } juega con Rojo, { $white } juega con Blanco.
backgammon-opening-roll = Tirada inicial: { $red } saca { $red_die }, { $white } saca { $white_die }.
backgammon-opening-tie = Ambos sacaron { $die }, tirando de nuevo.
backgammon-opening-winner = { $player } empieza con { $die1 } y { $die2 }.

# Dados
backgammon-roll = { $player } saca { $die1 } y { $die2 }.

# Sin movimientos
backgammon-no-moves = { $player } no tiene movimientos legales.

# Comentario de movimientos (abreviado)
backgammon-move-normal = { $src } a { $dest }, { $remain } { $count }.
backgammon-move-emptying = Vaciando { $src } a { $dest }, { $count }.
backgammon-move-hit = { $src } captura en { $dest }, { $remain }.
backgammon-move-emptying-hit = Vaciando { $src } captura en { $dest }.
backgammon-move-bar = Barra a { $dest }, { $count }.
backgammon-move-bar-hit = Barra captura en { $dest }, { $count }.
backgammon-move-bearoff = Sacando de { $src }, { $remain }.

# Doblaje
backgammon-doubles = { $player } dobla a { $value }.
backgammon-accepts = { $player } acepta.
backgammon-drops = { $player } rechaza.
backgammon-accept = Aceptar
backgammon-drop = Rechazar

# Etiquetas de puntos
backgammon-point-empty = { $point } vacío
backgammon-point-empty-selected = { $point } vacío seleccionado
backgammon-point-occupied = { $point } { $color }, { $count }
backgammon-point-occupied-selected = { $point } { $color }, { $count } seleccionado

# Pista local
backgammon-hint-bar = barra
backgammon-hint-off = fuera

# Etiquetas de acciones
backgammon-label-double = Doblar
backgammon-label-undo = Deshacer
backgammon-label-hint = Pista
backgammon-label-cube-hint = Pista del cubo

# Retroalimentación de selección
backgammon-selected-point = Seleccionado punto { $point }, { $count } fichas.
backgammon-selected-bar = Barra seleccionada.
backgammon-deselected = Deseleccionado.
backgammon-no-checkers-there = No hay fichas ahí.
backgammon-no-moves-from-here = No hay movimientos legales desde aquí.
backgammon-must-enter-from-bar = Primero debes entrar desde la barra.
backgammon-illegal-move = Movimiento ilegal.
backgammon-bearoff-blocked = No puedes sacar del punto { $point } con un { $die }, porque hay fichas en tu punto { $blocking_point }.
backgammon-bearoff-no-die = No puedes sacar del punto { $point } con tus dados restantes ({ $die }).
backgammon-nothing-to-undo = Nada que deshacer.
backgammon-undone = Movimiento deshecho.
backgammon-cannot-double = No puedes doblar ahora.
backgammon-cannot-undo = Nada que deshacer.
backgammon-not-doubling-phase = No hay doble al que responder.

# Pistas
backgammon-hint = { $player } pide una pista: { $hint }
backgammon-hint-not-now = Las pistas solo están disponibles durante la fase de movimiento.
backgammon-hints-disabled = Las pistas están desactivadas. Actívalas en las opciones de partida.
backgammon-hint-unavailable = Motor de pistas no disponible.
backgammon-cube-hint = { $player } pide consejo del cubo: { $hint }
backgammon-cube-hint-not-now = Las pistas del cubo solo están disponibles antes de tirar o al enfrentar un doble.
backgammon-cube-hints-disabled = Las pistas del cubo están desactivadas. Actívalas en las opciones de partida.
backgammon-gnubg-fallback = Motor GNUBG no disponible. El bot usa estrategia simple.

# Atajos de información
backgammon-check-status = Estado
backgammon-check-cube = Cubo
backgammon-check-pip = Conteo de pips
backgammon-check-score = Puntuación
backgammon-check-dice = Dados
backgammon-status = Barra rojo: { $bar_red }. Barra blanco: { $bar_white }. Fuera rojo: { $off_red }. Fuera blanco: { $off_white }.
backgammon-dice = { $dice }
backgammon-dice-none = Sin dados.
backgammon-cube-status = Cubo en { $value }. { $owner ->
    [center] Centrado, cualquier jugador puede doblar.
    *[other] Lo tiene { $owner }.
} { $can_double ->
    [yes] El doblaje está disponible ahora.
    [crawford] Esta es una partida Crawford, no se permite doblar.
    *[no] El doblaje no está disponible ahora.
}
backgammon-cube-no-match = No hay cubo de doblaje en partidas individuales.
backgammon-pip-count = Pips rojo: { $red_pip }. Pips blanco: { $white_pip }.
backgammon-match-score = { $red } { $red_score }, { $white } { $white_score }. Match a { $match_length }. Cubo: { $cube }.

# Puntuación
backgammon-wins-game = { $player } gana { $points } punto{ $points ->
    [one] {""}
    *[other] s
}.
backgammon-new-game = Comenzando partida { $number }.
backgammon-match-winner = ¡{ $player } gana el match!
backgammon-crawford = Partida Crawford: no se permite doblar en esta partida.
# Niveles de dificultad
backgammon-difficulty-random = Aleatorio
backgammon-difficulty-simple = Simple
backgammon-difficulty-gnubg-0ply = GNUBG 0-ply
backgammon-difficulty-gnubg-1ply = GNUBG 1-ply
backgammon-difficulty-gnubg-2ply = GNUBG 2-ply
backgammon-difficulty-whackgammon = Whackgammon

# Opciones
backgammon-option-match-length = Longitud del match: { $match_length }
backgammon-option-select-match-length = Establecer longitud del match (1-25)
backgammon-option-changed-match-length = Longitud del match establecida a { $match_length }.
backgammon-option-bot-difficulty = Dificultad del bot: { $bot_difficulty }
backgammon-option-select-bot-difficulty = Seleccionar dificultad del bot
backgammon-option-changed-bot-difficulty = Dificultad del bot establecida a { $bot_difficulty }.
backgammon-option-verbose-commentary = Comentario detallado: { $verbose_commentary }
backgammon-option-changed-verbose-commentary = Comentario detallado establecido a { $verbose_commentary }.
backgammon-option-hints = Pistas: { $hints_enabled }
backgammon-option-changed-hints = Pistas establecidas a { $hints_enabled }.
backgammon-option-cube-hints = Pistas del cubo: { $cube_hints_enabled }
backgammon-option-changed-cube-hints = Pistas del cubo establecidas a { $cube_hints_enabled }.
