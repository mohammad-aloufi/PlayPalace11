# Monopoly game messages

# Game info
game-name-monopoly = Monopoly

# Lobby options
monopoly-set-preset = Режим: { $preset }
monopoly-select-preset = Выберите режим Monopoly
monopoly-option-changed-preset = Режим установлен: { $preset }.

# Preset labels
monopoly-preset-classic-standard = Классический и тематический стандарт
monopoly-preset-junior = Monopoly Junior
monopoly-preset-junior-modern = Monopoly Junior (современный)
monopoly-preset-junior-legacy = Monopoly Junior (классический)
monopoly-preset-cheaters = Monopoly: издание для мошенников
monopoly-preset-electronic-banking = Электронный банк
monopoly-preset-voice-banking = Голосовой банк
monopoly-preset-sore-losers = Monopoly для плохих проигравших
monopoly-preset-speed = Monopoly Speed
monopoly-preset-builder = Monopoly Builder
monopoly-preset-city = Monopoly City
monopoly-preset-bid-card-game = Monopoly Bid
monopoly-preset-deal-card-game = Monopoly Deal
monopoly-preset-knockout = Monopoly Knockout
monopoly-preset-free-parking-jackpot = Джекпот на бесплатной парковке

# Scaffold status
monopoly-announce-preset = Объявить текущий режим
monopoly-current-preset = Текущий режим: { $preset } ({ $count } изданий).
monopoly-scaffold-started = Monopoly запущена в режиме { $preset } ({ $count } изданий).

# Turn actions
monopoly-roll-dice = Бросить кости
monopoly-buy-property = Купить собственность
monopoly-banking-balance = Проверить банковский баланс
monopoly-banking-transfer = Перевести деньги
monopoly-banking-ledger = Просмотреть банковский журнал
monopoly-voice-command = Голосовая команда
monopoly-cheaters-claim-reward = Получить награду жулика
monopoly-end-turn = Завершить ход

# Turn validation
monopoly-roll-first = Сначала нужно бросить кости.
monopoly-already-rolled = В этом ходу вы уже бросали кости.
monopoly-no-property-to-buy = Сейчас нет собственности для покупки.
monopoly-property-owned = Эта собственность уже принадлежит кому-то.
monopoly-not-enough-cash = У вас недостаточно денег.
monopoly-action-disabled-for-preset = Это действие отключено для выбранного режима.
monopoly-buy-disabled = В этом режиме нельзя покупать собственность напрямую.

# Turn events
monopoly-pass-go = { $player } прошёл GO и получил { $amount } (деньги: { $cash }).
monopoly-roll-result = { $player } выбросил { $die1 } + { $die2 } = { $total } и остановился на { $space }.
monopoly-roll-only = { $player } выбросил { $die1 } + { $die2 } = { $total }.
monopoly-you-roll-result = Вы выбросили { $die1 } + { $die2 } = { $total } и остановились на { $space }.
monopoly-player-roll-result = { $player } выбросил { $die1 } + { $die2 } = { $total } и остановился на { $space }.
monopoly-you-roll-only = Вы выбросили { $die1 } + { $die2 } = { $total }.
monopoly-player-roll-only = { $player } выбросил { $die1 } + { $die2 } = { $total }.
monopoly-you-roll-only-doubles = Вы выбросили { $die1 } + { $die2 } = { $total }. Дубль!
monopoly-player-roll-only-doubles = { $player } выбросил { $die1 } + { $die2 } = { $total }. Дубль!
monopoly-property-available = { $property } доступна за { $price }.
monopoly-property-bought = { $player } купил { $property } за { $price } (деньги: { $cash }).
monopoly-rent-paid = { $player } заплатил { $amount } ренты игроку { $owner } за { $property }.
monopoly-player-paid-player = { $player } заплатил { $amount } игроку { $target }.
monopoly-landed-owned = { $player } попал на свою собственность: { $property }.
monopoly-tax-paid = { $player } заплатил { $amount } за { $tax } (деньги: { $cash }).
monopoly-go-to-jail = { $player } отправляется в тюрьму (перемещён на { $space }).
monopoly-bankrupt-player = Вы банкрот и выбываете из игры.
monopoly-player-bankrupt = { $player } обанкротился. Кредитор: { $creditor }.
monopoly-winner-by-bankruptcy = { $player } побеждает через банкротство с остатком { $cash }.
monopoly-winner-by-cash = { $player } побеждает с наибольшей суммой денег: { $cash }.
monopoly-city-winner-by-value = { $player } побеждает в Monopoly City с итоговой стоимостью { $total }.

# Additional actions
monopoly-auction-property = Выставить на аукцион
monopoly-auction-bid = Сделать ставку
monopoly-auction-pass = Пас в аукционе
monopoly-mortgage-property = Заложить собственность
monopoly-unmortgage-property = Выкупить залог
monopoly-build-house = Построить дом или отель
monopoly-sell-house = Продать дом или отель
monopoly-offer-trade = Предложить обмен
monopoly-accept-trade = Принять обмен
monopoly-decline-trade = Отклонить обмен
monopoly-read-cash = Озвучить наличные
monopoly-pay-bail = Заплатить залог
monopoly-use-jail-card = Использовать карту выхода из тюрьмы
monopoly-cash-report = Наличными: { $cash }.
monopoly-property-amount-option = { $property } за { $amount }
monopoly-banking-transfer-option = Перевести { $amount } игроку { $target }

# Additional prompts
monopoly-select-property-mortgage = Выберите собственность для залога
monopoly-select-property-unmortgage = Выберите собственность для выкупа из залога
monopoly-select-property-build = Выберите собственность для строительства
monopoly-select-property-sell = Выберите собственность, с которой продаётся здание
monopoly-select-trade-offer = Выберите предложение обмена
monopoly-select-auction-bid = Выберите свою ставку
monopoly-select-banking-transfer = Выберите перевод
monopoly-select-voice-command = Введите голосовую команду, начиная с voice:

# Additional validation
monopoly-no-property-to-auction = Сейчас нет собственности для аукциона.
monopoly-auction-active = Сначала завершите текущий аукцион.
monopoly-no-auction-active = Сейчас нет активного аукциона.
monopoly-not-your-auction-turn = Сейчас не ваш ход в аукционе.
monopoly-no-mortgage-options = У вас нет собственности, доступной для залога.
monopoly-no-unmortgage-options = У вас нет заложенной собственности для выкупа.
monopoly-no-build-options = У вас нет собственности, доступной для строительства.
monopoly-no-sell-options = У вас нет собственности с постройками для продажи.
monopoly-no-trade-options = У вас сейчас нет допустимых вариантов обмена.
monopoly-no-trade-pending = Для вас нет ожидающего обмена.
monopoly-trade-pending = Обмен уже ожидает ответа.
monopoly-trade-no-longer-valid = Этот обмен больше недействителен.
monopoly-not-in-jail = Вы не в тюрьме.
monopoly-no-jail-card = У вас нет карты выхода из тюрьмы.
monopoly-roll-again-required = Вы выбросили дубль и должны бросить ещё раз.
monopoly-resolve-property-first = Сначала решите ожидающий вопрос по собственности.

# Additional turn events
monopoly-roll-again = { $player } выбросил дубль и бросает снова.
monopoly-you-roll-again = Вы выбросили дубль и бросаете снова.
monopoly-player-roll-again = { $player } выбросил дубль и бросает снова.
monopoly-jail-roll-doubles = { $player } выбросил дубль ({ $die1 } и { $die2 }) и выходит из тюрьмы.
monopoly-you-jail-roll-doubles = Вы выбросили дубль ({ $die1 } и { $die2 }) и выходите из тюрьмы.
monopoly-player-jail-roll-doubles = { $player } выбросил дубль ({ $die1 } и { $die2 }) и выходит из тюрьмы.
monopoly-jail-roll-failed = { $player } выбросил { $die1 } и { $die2 } в тюрьме (попытка { $attempts }).
monopoly-bail-paid = { $player } заплатил { $amount } залога (деньги: { $cash }).
monopoly-three-doubles-jail = { $player } выбросил три дубля за один ход и отправлен в тюрьму.
monopoly-you-three-doubles-jail = Вы выбросили три дубля за один ход и отправлены в тюрьму.
monopoly-player-three-doubles-jail = { $player } выбросил три дубля за один ход и отправлен в тюрьму.
monopoly-jail-card-used = { $player } использовал карту выхода из тюрьмы ({ $cards } осталось).
monopoly-sore-loser-rebate = { $player } получил компенсацию плохому проигравшему в размере { $amount } (деньги: { $cash }).
monopoly-cheaters-early-end-turn-blocked = { $player } попытался закончить ход слишком рано и заплатил штраф за жульничество { $amount } (деньги: { $cash }).
monopoly-cheaters-payment-avoidance-blocked = { $player } получил штраф за уклонение от оплаты { $amount } (деньги: { $cash }).
monopoly-cheaters-reward-granted = { $player } получил награду жулика { $amount } (деньги: { $cash }).
monopoly-cheaters-reward-unavailable = { $player } уже получал награду жулика в этом ходу.

# Auctions and mortgages
monopoly-auction-no-bids = На { $property } не было ставок. Поле остаётся непроданным.
monopoly-auction-started = Аукцион по { $property } начался (стартовая ставка: { $amount }).
monopoly-auction-turn = Ход аукциона: игрок { $player } действует по { $property } (текущая ставка: { $amount }).
monopoly-auction-bid-placed = { $player } поставил { $amount } за { $property }.
monopoly-auction-pass-event = { $player } спасовал по { $property }.
monopoly-auction-won = { $player } выиграл аукцион за { $property } за { $amount } (деньги: { $cash }).
monopoly-property-mortgaged = { $player } заложил { $property } за { $amount } (деньги: { $cash }).
monopoly-property-unmortgaged = { $player } выкупил из залога { $property } за { $amount } (деньги: { $cash }).
monopoly-house-built = { $player } построил на { $property } за { $amount } (уровень: { $level }, деньги: { $cash }).
monopoly-house-sold = { $player } продал постройку на { $property } за { $amount } (уровень: { $level }, деньги: { $cash }).
monopoly-trade-offered = { $proposer } предложил игроку { $target } обмен: { $offer }.
monopoly-trade-completed = Обмен между { $proposer } и { $target } завершён: { $offer }.
monopoly-trade-declined = { $target } отклонил обмен от { $proposer }: { $offer }.
monopoly-trade-cancelled = Обмен отменён: { $offer }.
monopoly-free-parking-jackpot = { $player } получил джекпот бесплатной парковки { $amount } (деньги: { $cash }).
monopoly-mortgaged-no-rent = { $player } попал на заложенное поле { $property }; рента не взымается.
monopoly-builder-blocks-awarded = { $player } получил { $amount } строительных блоков ({ $blocks } всего).
monopoly-builder-block-spent = { $player } потратил строительный блок ({ $blocks } осталось).
monopoly-banking-transfer-success = { $from_player } перевёл { $amount } игроку { $to_player }.
monopoly-banking-transfer-failed = Банковский перевод игрока { $player } не удался ({ $reason }).
monopoly-banking-balance-report = Банковский баланс игрока { $player }: { $cash }.
monopoly-banking-ledger-report = Недавняя банковская активность: { $entries }.
monopoly-banking-ledger-empty = Банковских операций пока нет.
monopoly-voice-command-error = Ошибка голосовой команды: { $reason }.
monopoly-voice-command-accepted = Голосовая команда принята: { $intent }.
monopoly-voice-command-repeat = Повтор последнего банковского кода ответа: { $response }.
monopoly-voice-transfer-staged = Подготовлен голосовой перевод: { $amount } игроку { $target }. Скажите voice: confirm transfer.
monopoly-mortgage-transfer-interest-paid = { $player } заплатил { $amount } процентов за передачу залога (деньги: { $cash }).

# Card engine
monopoly-card-drawn = { $player } вытянул карту { $deck }: { $card }.
monopoly-card-collect = { $player } получил { $amount } (деньги: { $cash }).
monopoly-card-pay = { $player } заплатил { $amount } (деньги: { $cash }).
monopoly-card-move = { $player } перемещён на { $space }.
monopoly-card-jail-free = { $player } получил карту выхода из тюрьмы ({ $cards } всего).
monopoly-card-utility-roll = { $player } выбросил { $die1 } + { $die2 } = { $total } для оплаты коммунальной ренты.
monopoly-deck-chance = Шанс
monopoly-deck-community-chest = Общественная казна

# Card descriptions
monopoly-card-advance-to-go = Идите на GO и получите { $amount }
monopoly-card-advance-to-illinois-avenue = Перейдите на Illinois Avenue
monopoly-card-advance-to-st-charles-place = Перейдите на St. Charles Place
monopoly-card-advance-to-nearest-utility = Перейдите к ближайшей коммунальной компании
monopoly-card-advance-to-nearest-railroad = Перейдите к ближайшей железной дороге и заплатите двойную ренту, если у неё есть владелец
monopoly-card-bank-dividend-50 = Банк выплачивает вам дивиденды { $amount }
monopoly-card-go-back-three = Вернитесь на 3 клетки назад
monopoly-card-go-to-jail = Немедленно отправляйтесь в тюрьму
monopoly-card-general-repairs = Проведите капитальный ремонт всей собственности: { $per_house } за дом, { $per_hotel } за отель
monopoly-card-poor-tax-15 = Заплатите налог { $amount }
monopoly-card-reading-railroad = Отправляйтесь на Reading Railroad
monopoly-card-boardwalk = Прогуляйтесь до Boardwalk
monopoly-card-chairman-of-the-board = Председатель совета, заплатите каждому игроку { $amount }
monopoly-card-building-loan-matures = Ваш строительный заём погашен, получите { $amount }
monopoly-card-crossword-competition = Вы выиграли конкурс кроссвордов, получите { $amount }
monopoly-card-bank-error-200 = Ошибка банка в вашу пользу, получите { $amount }
monopoly-card-doctor-fee-50 = Оплата врачу, заплатите { $amount }
monopoly-card-sale-of-stock-50 = За продажу акций вы получаете { $amount }
monopoly-card-holiday-fund = Отпускной фонд созрел, получите { $amount }
monopoly-card-tax-refund-20 = Возврат подоходного налога, получите { $amount }
monopoly-card-birthday = У вас день рождения, получите по { $amount } от каждого игрока
monopoly-card-life-insurance = Страхование жизни созрело, получите { $amount }
monopoly-card-hospital-fees-100 = Заплатите больничные расходы { $amount }
monopoly-card-school-fees-50 = Заплатите школьный сбор { $amount }
monopoly-card-consultancy-fee-25 = Получите { $amount } за консультацию
monopoly-card-street-repairs = Ремонт улиц: { $per_house } за дом, { $per_hotel } за отель
monopoly-card-beauty-contest-10 = Вы заняли второе место в конкурсе красоты, получите { $amount }
monopoly-card-inherit-100 = Вы наследуете { $amount }
monopoly-card-get-out-of-jail = Бесплатный выход из тюрьмы

# Board profile options
monopoly-set-board = Поле: { $board }
monopoly-select-board = Выберите поле Monopoly
monopoly-option-changed-board = Поле установлено: { $board }.
monopoly-set-board-rules-mode = Режим правил поля: { $mode }
monopoly-select-board-rules-mode = Выберите режим правил поля
monopoly-option-changed-board-rules-mode = Режим правил поля установлен: { $mode }.

# Board labels
monopoly-board-classic-default = Классическое поле
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
monopoly-board-rules-mode-auto = Авто
monopoly-board-rules-mode-skin-only = Только оформление

# Board runtime announcements
monopoly-board-preset-autofixed = Поле { $board } несовместимо с { $from_preset }; переключено на { $to_preset }.
monopoly-board-rules-simplified = Правила поля { $board } реализованы частично; для отсутствующих механик используется базовое поведение режима.
monopoly-board-active = Активное поле: { $board } (режим: { $mode }).

# Deed and ownership browsing
monopoly-view-active-deed = Просмотреть активный титул
monopoly-view-active-deed-space = Просмотреть { $property }
monopoly-browse-all-deeds = Просмотреть все титулы
monopoly-view-my-properties = Просмотреть мои собственности
monopoly-view-player-properties = Просмотреть сведения об игроке
monopoly-view-selected-deed = Просмотреть выбранный титул
monopoly-view-selected-owner-property-deed = Просмотреть титул выбранного игрока
monopoly-select-property-deed = Выберите титул собственности
monopoly-select-player-properties = Выберите игрока
monopoly-select-player-property-deed = Выберите титул собственности игрока
monopoly-no-active-deed = Сейчас нет активного титула для просмотра.
monopoly-no-deeds-available = На этом поле нет объектов, для которых можно показать титул.
monopoly-no-owned-properties = Для этого просмотра нет принадлежащих объектов.
monopoly-no-players-with-properties = Нет доступных игроков.
monopoly-buy-for = Купить за { $amount }
monopoly-you-have-no-owned-properties = У вас нет собственности.
monopoly-player-has-no-owned-properties = У игрока { $player } нет собственности.
monopoly-owner-bank = Банк
monopoly-owner-unknown = Неизвестно
monopoly-building-status-hotel = с отелем
monopoly-building-status-one-house = с 1 домом
monopoly-building-status-houses = с { $count } домами
monopoly-mortgaged-short = заложено
monopoly-deed-menu-label = { $property } ({ $owner })
monopoly-deed-menu-label-extra = { $property } ({ $owner }; { $extras })
monopoly-color-brown = Коричневый
monopoly-color-light_blue = Голубой
monopoly-color-pink = Розовый
monopoly-color-orange = Оранжевый
monopoly-color-red = Красный
monopoly-color-yellow = Жёлтый
monopoly-color-green = Зелёный
monopoly-color-dark_blue = Тёмно-синий
monopoly-deed-type-color-group = Тип: группа цвета { $color }
monopoly-deed-type-railroad = Тип: железная дорога
monopoly-deed-type-utility = Тип: коммунальная компания
monopoly-deed-type-generic = Тип: { $kind }
monopoly-deed-purchase-price = Цена покупки: { $amount }
monopoly-deed-rent = Рента: { $amount }
monopoly-deed-full-set-rent = Если у владельца полный комплект цвета: { $amount }
monopoly-deed-rent-one-house = С 1 домом: { $amount }
monopoly-deed-rent-houses = С { $count } домами: { $amount }
monopoly-deed-rent-hotel = С отелем: { $amount }
monopoly-deed-house-cost = Стоимость дома: { $amount }
monopoly-deed-railroad-rent = Рента при { $count } железных дорогах: { $amount }
monopoly-deed-utility-one-owned = Если принадлежит одна коммунальная компания: 4x бросок
monopoly-deed-utility-both-owned = Если принадлежат обе коммунальные компании: 10x бросок
monopoly-deed-utility-base-rent = Базовая рента коммунальной компании (старый вариант): { $amount }
monopoly-deed-mortgage-value = Залоговая стоимость: { $amount }
monopoly-deed-unmortgage-cost = Стоимость выкупа из залога: { $amount }
monopoly-deed-owner = Владелец: { $owner }
monopoly-deed-current-buildings = Текущие постройки: { $buildings }
monopoly-deed-status-mortgaged = Статус: заложено
monopoly-player-properties-label = { $player }, на { $space }, клетка { $position }
monopoly-player-properties-label-no-space = { $player }, клетка { $position }
monopoly-banking-ledger-entry-success = { $tx_id } { $kind } { $from_id }->{ $to_id } { $amount } ({ $reason })
monopoly-banking-ledger-entry-failed = { $tx_id } { $kind } ошибка ({ $reason })

# Trade menu summaries
monopoly-trade-buy-property-summary = Купить { $property } у { $target } за { $amount }
monopoly-trade-offer-cash-for-property-summary = Предложить { $amount } игроку { $target } за { $property }
monopoly-trade-sell-property-summary = Продать { $property } игроку { $target } за { $amount }
monopoly-trade-offer-property-for-cash-summary = Предложить { $property } игроку { $target } за { $amount }
monopoly-trade-swap-summary = Обменять { $give_property } с { $target } на { $receive_property }
monopoly-trade-swap-plus-cash-summary = Обменять { $give_property } + { $amount } с { $target } на { $receive_property }
monopoly-trade-swap-receive-cash-summary = Обменять { $give_property } на { $receive_property } + { $amount } от { $target }
monopoly-trade-buy-jail-card-summary = Купить у { $target } карту выхода из тюрьмы за { $amount }
monopoly-trade-sell-jail-card-summary = Продать игроку { $target } карту выхода из тюрьмы за { $amount }

# Board space names
monopoly-space-go = GO
monopoly-space-mediterranean_avenue = Mediterranean Avenue
monopoly-space-community_chest_1 = Общественная казна
monopoly-space-baltic_avenue = Baltic Avenue
monopoly-space-income_tax = Подоходный налог
monopoly-space-reading_railroad = Reading Railroad
monopoly-space-oriental_avenue = Oriental Avenue
monopoly-space-chance_1 = Шанс
monopoly-space-vermont_avenue = Vermont Avenue
monopoly-space-connecticut_avenue = Connecticut Avenue
monopoly-space-jail = Тюрьма / Просто в гостях
monopoly-space-st_charles_place = St. Charles Place
monopoly-space-electric_company = Электрическая компания
monopoly-space-states_avenue = States Avenue
monopoly-space-virginia_avenue = Virginia Avenue
monopoly-space-pennsylvania_railroad = Pennsylvania Railroad
monopoly-space-st_james_place = St. James Place
monopoly-space-community_chest_2 = Общественная казна
monopoly-space-tennessee_avenue = Tennessee Avenue
monopoly-space-new_york_avenue = New York Avenue
monopoly-space-free_parking = Бесплатная парковка
monopoly-space-kentucky_avenue = Kentucky Avenue
monopoly-space-chance_2 = Шанс
monopoly-space-indiana_avenue = Indiana Avenue
monopoly-space-illinois_avenue = Illinois Avenue
monopoly-space-bo_railroad = B. & O. Railroad
monopoly-space-atlantic_avenue = Atlantic Avenue
monopoly-space-ventnor_avenue = Ventnor Avenue
monopoly-space-water_works = Водоканал
monopoly-space-marvin_gardens = Marvin Gardens
monopoly-space-go_to_jail = Идите в тюрьму
monopoly-space-pacific_avenue = Pacific Avenue
monopoly-space-north_carolina_avenue = North Carolina Avenue
monopoly-space-community_chest_3 = Общественная казна
monopoly-space-pennsylvania_avenue = Pennsylvania Avenue
monopoly-space-short_line = Short Line
monopoly-space-chance_3 = Шанс
monopoly-space-park_place = Park Place
monopoly-space-luxury_tax = Налог на роскошь
monopoly-space-boardwalk = Boardwalk
