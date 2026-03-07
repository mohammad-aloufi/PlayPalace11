# Monopoly game messages

# Game info
game-name-monopoly = Monopoly

# Lobby options
monopoly-set-preset = Modo: { $preset }
monopoly-select-preset = Selecione um modo de Monopoly
monopoly-option-changed-preset = Modo definido como { $preset }.

# Preset labels
monopoly-preset-classic-standard = Clássico e temático padrão
monopoly-preset-junior = Monopoly Junior
monopoly-preset-junior-modern = Monopoly Junior (moderno)
monopoly-preset-junior-legacy = Monopoly Junior (legado)
monopoly-preset-cheaters = Monopoly Edição dos Trapaceiros
monopoly-preset-electronic-banking = Banco eletrônico
monopoly-preset-voice-banking = Banco por voz
monopoly-preset-sore-losers = Monopoly para maus perdedores
monopoly-preset-speed = Monopoly Speed
monopoly-preset-builder = Monopoly Builder
monopoly-preset-city = Monopoly City
monopoly-preset-bid-card-game = Monopoly Bid
monopoly-preset-deal-card-game = Monopoly Deal
monopoly-preset-knockout = Monopoly Knockout
monopoly-preset-free-parking-jackpot = Jackpot do Estacionamento Livre

# Scaffold status
monopoly-announce-preset = Anunciar modo atual
monopoly-current-preset = Modo atual: { $preset } ({ $count } edições).
monopoly-scaffold-started = Monopoly iniciado com { $preset } ({ $count } edições).

# Turn actions
monopoly-roll-dice = Rolar dados
monopoly-buy-property = Comprar propriedade
monopoly-banking-balance = Ver saldo bancário
monopoly-banking-transfer = Transferir fundos
monopoly-banking-ledger = Revisar extrato bancário
monopoly-voice-command = Comando de voz
monopoly-cheaters-claim-reward = Receber recompensa de trapaça
monopoly-end-turn = Encerrar turno

# Turn validation
monopoly-roll-first = Você precisa rolar primeiro.
monopoly-already-rolled = Você já rolou neste turno.
monopoly-no-property-to-buy = Não há propriedade para comprar agora.
monopoly-property-owned = Essa propriedade já tem dono.
monopoly-not-enough-cash = Você não tem dinheiro suficiente.
monopoly-action-disabled-for-preset = Esta ação está desativada para o modo selecionado.
monopoly-buy-disabled = Comprar propriedade diretamente está desativado neste modo.

# Turn events
monopoly-pass-go = { $player } passou pelo INÍCIO e recebeu { $amount } (dinheiro: { $cash }).
monopoly-roll-result = { $player } rolou { $die1 } + { $die2 } = { $total } e caiu em { $space }.
monopoly-roll-only = { $player } rolou { $die1 } + { $die2 } = { $total }.
monopoly-you-roll-result = Você rolou { $die1 } + { $die2 } = { $total } e caiu em { $space }.
monopoly-player-roll-result = { $player } rolou { $die1 } + { $die2 } = { $total } e caiu em { $space }.
monopoly-you-roll-only = Você rolou { $die1 } + { $die2 } = { $total }.
monopoly-player-roll-only = { $player } rolou { $die1 } + { $die2 } = { $total }.
monopoly-you-roll-only-doubles = Você rolou { $die1 } + { $die2 } = { $total }. Dupla!
monopoly-player-roll-only-doubles = { $player } rolou { $die1 } + { $die2 } = { $total }. Dupla!
monopoly-property-available = { $property } está disponível por { $price }.
monopoly-property-bought = { $player } comprou { $property } por { $price } (dinheiro: { $cash }).
monopoly-rent-paid = { $player } pagou { $amount } de aluguel a { $owner } por { $property }.
monopoly-player-paid-player = { $player } pagou { $amount } a { $target }.
monopoly-landed-owned = { $player } caiu na própria propriedade: { $property }.
monopoly-tax-paid = { $player } pagou { $amount } por { $tax } (dinheiro: { $cash }).
monopoly-go-to-jail = { $player } vai para a prisão (movido para { $space }).
monopoly-bankrupt-player = Você faliu e saiu do jogo.
monopoly-player-bankrupt = { $player } faliu. Credor: { $creditor }.
monopoly-winner-by-bankruptcy = { $player } vence por falência com { $cash } restantes.
monopoly-winner-by-cash = { $player } vence com o maior total de dinheiro: { $cash }.
monopoly-city-winner-by-value = { $player } vence Monopoly City com valor final de { $total }.

# Additional actions
monopoly-auction-property = Leiloar propriedade
monopoly-auction-bid = Dar lance no leilão
monopoly-auction-pass = Passar no leilão
monopoly-mortgage-property = Hipotecar propriedade
monopoly-unmortgage-property = Deshipotecar propriedade
monopoly-build-house = Construir casa ou hotel
monopoly-sell-house = Vender casa ou hotel
monopoly-offer-trade = Oferecer troca
monopoly-accept-trade = Aceitar troca
monopoly-decline-trade = Recusar troca
monopoly-read-cash = Ler dinheiro
monopoly-pay-bail = Pagar fiança
monopoly-use-jail-card = Usar carta de saída da prisão
monopoly-cash-report = { $cash } em dinheiro.
monopoly-property-amount-option = { $property } por { $amount }
monopoly-banking-transfer-option = Transferir { $amount } para { $target }

# Additional prompts
monopoly-select-property-mortgage = Selecione uma propriedade para hipotecar
monopoly-select-property-unmortgage = Selecione uma propriedade para deshipotecar
monopoly-select-property-build = Selecione uma propriedade para construir
monopoly-select-property-sell = Selecione uma propriedade de onde vender
monopoly-select-trade-offer = Selecione uma oferta de troca
monopoly-select-auction-bid = Selecione seu lance no leilão
monopoly-select-banking-transfer = Selecione uma transferência
monopoly-select-voice-command = Digite um comando de voz começando com voice:

# Additional validation
monopoly-no-property-to-auction = Não há propriedade para leiloar agora.
monopoly-auction-active = Resolva primeiro o leilão ativo.
monopoly-no-auction-active = Não há leilão em andamento.
monopoly-not-your-auction-turn = Não é sua vez no leilão.
monopoly-no-mortgage-options = Você não tem propriedades disponíveis para hipotecar.
monopoly-no-unmortgage-options = Você não tem propriedades hipotecadas para deshipotecar.
monopoly-no-build-options = Você não tem propriedades disponíveis para construir.
monopoly-no-sell-options = Você não tem propriedades com prédios disponíveis para vender.
monopoly-no-trade-options = Você não tem trocas válidas para oferecer agora.
monopoly-no-trade-pending = Não há troca pendente para você.
monopoly-trade-pending = Já existe uma troca pendente.
monopoly-trade-no-longer-valid = Essa troca não é mais válida.
monopoly-not-in-jail = Você não está na prisão.
monopoly-no-jail-card = Você não tem uma carta de saída da prisão.
monopoly-roll-again-required = Você rolou uma dupla e deve rolar de novo.
monopoly-resolve-property-first = Resolva primeiro a decisão pendente da propriedade.

# Additional turn events
monopoly-roll-again = { $player } rolou uma dupla e joga novamente.
monopoly-you-roll-again = Você rolou uma dupla e joga novamente.
monopoly-player-roll-again = { $player } rolou uma dupla e joga novamente.
monopoly-jail-roll-doubles = { $player } rolou uma dupla ({ $die1 } e { $die2 }) e sai da prisão.
monopoly-you-jail-roll-doubles = Você rolou uma dupla ({ $die1 } e { $die2 }) e sai da prisão.
monopoly-player-jail-roll-doubles = { $player } rolou uma dupla ({ $die1 } e { $die2 }) e sai da prisão.
monopoly-jail-roll-failed = { $player } rolou { $die1 } e { $die2 } na prisão (tentativa { $attempts }).
monopoly-bail-paid = { $player } pagou { $amount } de fiança (dinheiro: { $cash }).
monopoly-three-doubles-jail = { $player } rolou três duplas em um turno e foi para a prisão.
monopoly-you-three-doubles-jail = Você rolou três duplas em um turno e foi para a prisão.
monopoly-player-three-doubles-jail = { $player } rolou três duplas em um turno e foi para a prisão.
monopoly-jail-card-used = { $player } usou uma carta de saída da prisão ({ $cards } restantes).
monopoly-sore-loser-rebate = { $player } recebeu um reembolso de mau perdedor de { $amount } (dinheiro: { $cash }).
monopoly-cheaters-early-end-turn-blocked = { $player } tentou encerrar o turno cedo e pagou uma penalidade de trapaça de { $amount } (dinheiro: { $cash }).
monopoly-cheaters-payment-avoidance-blocked = { $player } ativou uma penalidade por evitar pagamento de { $amount } (dinheiro: { $cash }).
monopoly-cheaters-reward-granted = { $player } recebeu uma recompensa de trapaça de { $amount } (dinheiro: { $cash }).
monopoly-cheaters-reward-unavailable = { $player } já recebeu a recompensa de trapaça neste turno.

# Auctions and mortgages
monopoly-auction-no-bids = Nenhum lance para { $property }. Ela continua sem dono.
monopoly-auction-started = Leilão iniciado para { $property } (lance inicial: { $amount }).
monopoly-auction-turn = Turno do leilão: { $player } deve agir em { $property } (lance atual: { $amount }).
monopoly-auction-bid-placed = { $player } ofertou { $amount } por { $property }.
monopoly-auction-pass-event = { $player } passou em { $property }.
monopoly-auction-won = { $player } venceu o leilão de { $property } por { $amount } (dinheiro: { $cash }).
monopoly-property-mortgaged = { $player } hipotecou { $property } por { $amount } (dinheiro: { $cash }).
monopoly-property-unmortgaged = { $player } deshipotecou { $property } por { $amount } (dinheiro: { $cash }).
monopoly-house-built = { $player } construiu em { $property } por { $amount } (nível: { $level }, dinheiro: { $cash }).
monopoly-house-sold = { $player } vendeu uma construção em { $property } por { $amount } (nível: { $level }, dinheiro: { $cash }).
monopoly-trade-offered = { $proposer } ofereceu a { $target } uma troca: { $offer }.
monopoly-trade-completed = Troca concluída entre { $proposer } e { $target }: { $offer }.
monopoly-trade-declined = { $target } recusou a troca de { $proposer }: { $offer }.
monopoly-trade-cancelled = Troca cancelada: { $offer }.
monopoly-free-parking-jackpot = { $player } recebeu o jackpot do Estacionamento Livre de { $amount } (dinheiro: { $cash }).
monopoly-mortgaged-no-rent = { $player } caiu em { $property } hipotecada; nenhum aluguel é devido.
monopoly-builder-blocks-awarded = { $player } ganhou { $amount } blocos de construtor ({ $blocks } no total).
monopoly-builder-block-spent = { $player } gastou um bloco de construtor ({ $blocks } restantes).
monopoly-banking-transfer-success = { $from_player } transferiu { $amount } para { $to_player }.
monopoly-banking-transfer-failed = A transferência bancária de { $player } falhou ({ $reason }).
monopoly-banking-balance-report = Saldo bancário de { $player }: { $cash }.
monopoly-banking-ledger-report = Atividade bancária recente: { $entries }.
monopoly-banking-ledger-empty = Ainda não há transações bancárias.
monopoly-voice-command-error = Erro no comando de voz: { $reason }.
monopoly-voice-command-accepted = Comando de voz aceito: { $intent }.
monopoly-voice-command-repeat = Repetindo o último código de resposta bancária: { $response }.
monopoly-voice-transfer-staged = Transferência por voz preparada: { $amount } para { $target }. Diga voice: confirm transfer.
monopoly-mortgage-transfer-interest-paid = { $player } pagou { $amount } de juros por transferência de hipoteca (dinheiro: { $cash }).

# Card engine
monopoly-card-drawn = { $player } tirou uma carta de { $deck }: { $card }.
monopoly-card-collect = { $player } recebeu { $amount } (dinheiro: { $cash }).
monopoly-card-pay = { $player } pagou { $amount } (dinheiro: { $cash }).
monopoly-card-move = { $player } foi movido para { $space }.
monopoly-card-jail-free = { $player } recebeu uma carta de saída da prisão ({ $cards } no total).
monopoly-card-utility-roll = { $player } rolou { $die1 } + { $die2 } = { $total } para aluguel de companhia.
monopoly-deck-chance = Sorte
monopoly-deck-community-chest = Caixa da Comunidade

# Card descriptions
monopoly-card-advance-to-go = Vá para o INÍCIO e receba { $amount }
monopoly-card-advance-to-illinois-avenue = Vá para Illinois Avenue
monopoly-card-advance-to-st-charles-place = Vá para St. Charles Place
monopoly-card-advance-to-nearest-utility = Vá para a companhia mais próxima
monopoly-card-advance-to-nearest-railroad = Vá para a ferrovia mais próxima e pague aluguel em dobro se tiver dono
monopoly-card-bank-dividend-50 = O banco paga a você um dividendo de { $amount }
monopoly-card-go-back-three = Volte 3 casas
monopoly-card-go-to-jail = Vá diretamente para a prisão
monopoly-card-general-repairs = Faça reparos gerais em todas as suas propriedades: { $per_house } por casa, { $per_hotel } por hotel
monopoly-card-poor-tax-15 = Pague imposto de { $amount }
monopoly-card-reading-railroad = Faça uma viagem para Reading Railroad
monopoly-card-boardwalk = Faça um passeio até Boardwalk
monopoly-card-chairman-of-the-board = Presidente do conselho, pague { $amount } a cada jogador
monopoly-card-building-loan-matures = Seu empréstimo de construção venceu, receba { $amount }
monopoly-card-crossword-competition = Você venceu um concurso de palavras cruzadas, receba { $amount }
monopoly-card-bank-error-200 = Erro do banco a seu favor, receba { $amount }
monopoly-card-doctor-fee-50 = Honorários médicos, pague { $amount }
monopoly-card-sale-of-stock-50 = Pela venda de ações você recebe { $amount }
monopoly-card-holiday-fund = Fundo de férias venceu, receba { $amount }
monopoly-card-tax-refund-20 = Restituição de imposto de renda, receba { $amount }
monopoly-card-birthday = É seu aniversário, receba { $amount } de cada jogador
monopoly-card-life-insurance = Seguro de vida venceu, receba { $amount }
monopoly-card-hospital-fees-100 = Pague despesas hospitalares de { $amount }
monopoly-card-school-fees-50 = Pague taxas escolares de { $amount }
monopoly-card-consultancy-fee-25 = Receba { $amount } de honorários de consultoria
monopoly-card-street-repairs = Você foi cobrado por reparos de rua: { $per_house } por casa, { $per_hotel } por hotel
monopoly-card-beauty-contest-10 = Você ganhou o segundo prêmio em um concurso de beleza, receba { $amount }
monopoly-card-inherit-100 = Você herda { $amount }
monopoly-card-get-out-of-jail = Saia da prisão grátis

# Board profile options
monopoly-set-board = Tabuleiro: { $board }
monopoly-select-board = Selecione um tabuleiro de Monopoly
monopoly-option-changed-board = Tabuleiro definido como { $board }.
monopoly-set-board-rules-mode = Modo de regras do tabuleiro: { $mode }
monopoly-select-board-rules-mode = Selecione o modo de regras do tabuleiro
monopoly-option-changed-board-rules-mode = Modo de regras do tabuleiro definido como { $mode }.

# Board labels
monopoly-board-classic-default = Clássico padrão
monopoly-board-mario-collectors = Super Mario Bros. Collector's Edition
monopoly-board-mario-kart = Monopoly Gamer Mario Kart
monopoly-board-mario-celebration = Super Mario Celebration
monopoly-board-mario-movie = Super Mario Bros. Movie Edition
monopoly-board-junior-super-mario = Junior Super Mario Edition
monopoly-board-disney-princesses = Disney Princesses
monopoly-board-disney-animation = Disney Animation
monopoly-board-disney-lion-king = Disney Lion King
monopoly-board-disney-mickey-friends = Disney Mickey and Friends
monopoly-board-disney-villains = Disney Villains
monopoly-board-disney-lightyear = Disney Lightyear
monopoly-board-marvel-80-years = Marvel 80 Years
monopoly-board-marvel-avengers = Marvel Avengers
monopoly-board-marvel-spider-man = Marvel Spider-Man
monopoly-board-marvel-black-panther-wf = Marvel Black Panther Wakanda Forever
monopoly-board-marvel-super-villains = Marvel Super Villains
monopoly-board-marvel-deadpool = Marvel Deadpool
monopoly-board-star-wars-40th = Star Wars 40th
monopoly-board-star-wars-boba-fett = Star Wars Boba Fett
monopoly-board-star-wars-light-side = Star Wars Light Side
monopoly-board-star-wars-the-child = Star Wars The Child
monopoly-board-star-wars-mandalorian = Star Wars The Mandalorian
monopoly-board-star-wars-complete-saga = Star Wars Complete Saga
monopoly-board-harry-potter = Harry Potter
monopoly-board-fortnite = Fortnite
monopoly-board-stranger-things = Stranger Things
monopoly-board-jurassic-park = Jurassic Park
monopoly-board-lord-of-the-rings = Lord of the Rings
monopoly-board-animal-crossing = Animal Crossing
monopoly-board-barbie = Barbie
monopoly-board-disney-star-wars-dark-side = Disney Star Wars Dark Side
monopoly-board-disney-legacy = Disney Legacy Edition
monopoly-board-disney-the-edition = Disney The Edition
monopoly-board-lord-of-the-rings-trilogy = Lord of the Rings Trilogy
monopoly-board-star-wars-saga = Star Wars Saga
monopoly-board-marvel-avengers-legacy = Marvel Avengers Legacy
monopoly-board-star-wars-legacy = Star Wars Legacy
monopoly-board-star-wars-classic-edition = Star Wars Classic Edition
monopoly-board-star-wars-solo = Star Wars Solo
monopoly-board-game-of-thrones = Game of Thrones
monopoly-board-deadpool-collectors = Deadpool Collector's Edition
monopoly-board-toy-story = Toy Story
monopoly-board-black-panther = Black Panther
monopoly-board-stranger-things-collectors = Stranger Things Collector's Edition
monopoly-board-ghostbusters = Ghostbusters
monopoly-board-marvel-eternals = Marvel Eternals
monopoly-board-transformers = Transformers
monopoly-board-stranger-things-netflix = Stranger Things Netflix Edition
monopoly-board-fortnite-collectors = Fortnite Collector's Edition
monopoly-board-star-wars-mandalorian-s2 = Star Wars The Mandalorian Season 2
monopoly-board-transformers-beast-wars = Transformers Beast Wars
monopoly-board-marvel-falcon-winter-soldier = Marvel Falcon and Winter Soldier
monopoly-board-fortnite-flip = Fortnite Flip Edition
monopoly-board-marvel-flip = Marvel Flip Edition
monopoly-board-pokemon = Pokemon Edition

# Board rules mode labels
monopoly-board-rules-mode-auto = Automático
monopoly-board-rules-mode-skin-only = Apenas visual

# Board runtime announcements
monopoly-board-preset-autofixed = O tabuleiro { $board } é incompatível com { $from_preset }; alterado para { $to_preset }.
monopoly-board-rules-simplified = As regras do tabuleiro { $board } estão implementadas parcialmente; o comportamento básico do modo é usado para as mecânicas ausentes.
monopoly-board-active = Tabuleiro ativo: { $board } (modo: { $mode }).

# Deed and ownership browsing
monopoly-view-active-deed = Ver título ativo
monopoly-view-active-deed-space = Ver { $property }
monopoly-browse-all-deeds = Navegar por todos os títulos
monopoly-view-my-properties = Ver minhas propriedades
monopoly-view-player-properties = Ver informações do jogador
monopoly-view-selected-deed = Ver título selecionado
monopoly-view-selected-owner-property-deed = Ver título do jogador selecionado
monopoly-select-property-deed = Selecione um título de propriedade
monopoly-select-player-properties = Selecione um jogador
monopoly-select-player-property-deed = Selecione um título de propriedade do jogador
monopoly-no-active-deed = Não há título ativo para ver agora.
monopoly-no-deeds-available = Não há propriedades com título disponíveis neste tabuleiro.
monopoly-no-owned-properties = Não há propriedades possuídas disponíveis para esta visualização.
monopoly-no-players-with-properties = Não há jogadores disponíveis.
monopoly-buy-for = Comprar por { $amount }
monopoly-you-have-no-owned-properties = Você não possui nenhuma propriedade.
monopoly-player-has-no-owned-properties = { $player } não possui nenhuma propriedade.
monopoly-owner-bank = Banco
monopoly-owner-unknown = Desconhecido
monopoly-building-status-hotel = com hotel
monopoly-building-status-one-house = com 1 casa
monopoly-building-status-houses = com { $count } casas
monopoly-mortgaged-short = hipotecada
monopoly-deed-menu-label = { $property } ({ $owner })
monopoly-deed-menu-label-extra = { $property } ({ $owner }; { $extras })
monopoly-color-brown = Marrom
monopoly-color-light_blue = Azul-claro
monopoly-color-pink = Rosa
monopoly-color-orange = Laranja
monopoly-color-red = Vermelho
monopoly-color-yellow = Amarelo
monopoly-color-green = Verde
monopoly-color-dark_blue = Azul-escuro
monopoly-deed-type-color-group = Tipo: grupo de cor { $color }
monopoly-deed-type-railroad = Tipo: ferrovia
monopoly-deed-type-utility = Tipo: companhia
monopoly-deed-type-generic = Tipo: { $kind }
monopoly-deed-purchase-price = Preço de compra: { $amount }
monopoly-deed-rent = Aluguel: { $amount }
monopoly-deed-full-set-rent = Se o dono tiver o conjunto completo da cor: { $amount }
monopoly-deed-rent-one-house = Com 1 casa: { $amount }
monopoly-deed-rent-houses = Com { $count } casas: { $amount }
monopoly-deed-rent-hotel = Com hotel: { $amount }
monopoly-deed-house-cost = Custo da casa: { $amount }
monopoly-deed-railroad-rent = Aluguel com { $count } ferrovias: { $amount }
monopoly-deed-utility-one-owned = Se uma companhia for possuída: 4x o valor do dado
monopoly-deed-utility-both-owned = Se as duas companhias forem possuídas: 10x o valor do dado
monopoly-deed-utility-base-rent = Aluguel base da companhia (legado): { $amount }
monopoly-deed-mortgage-value = Valor da hipoteca: { $amount }
monopoly-deed-unmortgage-cost = Custo para deshipotecar: { $amount }
monopoly-deed-owner = Dono: { $owner }
monopoly-deed-current-buildings = Construções atuais: { $buildings }
monopoly-deed-status-mortgaged = Status: hipotecada
monopoly-player-properties-label = { $player }, em { $space }, casa { $position }
monopoly-player-properties-label-no-space = { $player }, casa { $position }
monopoly-banking-ledger-entry-success = { $tx_id } { $kind } { $from_id }->{ $to_id } { $amount } ({ $reason })
monopoly-banking-ledger-entry-failed = { $tx_id } { $kind } falhou ({ $reason })

# Trade menu summaries
monopoly-trade-buy-property-summary = Comprar { $property } de { $target } por { $amount }
monopoly-trade-offer-cash-for-property-summary = Oferecer { $amount } a { $target } por { $property }
monopoly-trade-sell-property-summary = Vender { $property } a { $target } por { $amount }
monopoly-trade-offer-property-for-cash-summary = Oferecer { $property } a { $target } por { $amount }
monopoly-trade-swap-summary = Trocar { $give_property } com { $target } por { $receive_property }
monopoly-trade-swap-plus-cash-summary = Trocar { $give_property } + { $amount } com { $target } por { $receive_property }
monopoly-trade-swap-receive-cash-summary = Trocar { $give_property } por { $receive_property } + { $amount } de { $target }
monopoly-trade-buy-jail-card-summary = Comprar carta de saída da prisão de { $target } por { $amount }
monopoly-trade-sell-jail-card-summary = Vender carta de saída da prisão a { $target } por { $amount }

# Board space names
monopoly-space-go = INÍCIO
monopoly-space-mediterranean_avenue = Mediterranean Avenue
monopoly-space-community_chest_1 = Caixa da Comunidade
monopoly-space-baltic_avenue = Baltic Avenue
monopoly-space-income_tax = Imposto de Renda
monopoly-space-reading_railroad = Reading Railroad
monopoly-space-oriental_avenue = Oriental Avenue
monopoly-space-chance_1 = Sorte
monopoly-space-vermont_avenue = Vermont Avenue
monopoly-space-connecticut_avenue = Connecticut Avenue
monopoly-space-jail = Prisão / Apenas visitando
monopoly-space-st_charles_place = St. Charles Place
monopoly-space-electric_company = Companhia Elétrica
monopoly-space-states_avenue = States Avenue
monopoly-space-virginia_avenue = Virginia Avenue
monopoly-space-pennsylvania_railroad = Pennsylvania Railroad
monopoly-space-st_james_place = St. James Place
monopoly-space-community_chest_2 = Caixa da Comunidade
monopoly-space-tennessee_avenue = Tennessee Avenue
monopoly-space-new_york_avenue = New York Avenue
monopoly-space-free_parking = Estacionamento Livre
monopoly-space-kentucky_avenue = Kentucky Avenue
monopoly-space-chance_2 = Sorte
monopoly-space-indiana_avenue = Indiana Avenue
monopoly-space-illinois_avenue = Illinois Avenue
monopoly-space-bo_railroad = B. & O. Railroad
monopoly-space-atlantic_avenue = Atlantic Avenue
monopoly-space-ventnor_avenue = Ventnor Avenue
monopoly-space-water_works = Companhia de Água
monopoly-space-marvin_gardens = Marvin Gardens
monopoly-space-go_to_jail = Vá para a prisão
monopoly-space-pacific_avenue = Pacific Avenue
monopoly-space-north_carolina_avenue = North Carolina Avenue
monopoly-space-community_chest_3 = Caixa da Comunidade
monopoly-space-pennsylvania_avenue = Pennsylvania Avenue
monopoly-space-short_line = Short Line
monopoly-space-chance_3 = Sorte
monopoly-space-park_place = Park Place
monopoly-space-luxury_tax = Imposto de Luxo
monopoly-space-boardwalk = Boardwalk
