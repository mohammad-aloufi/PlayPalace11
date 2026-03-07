# Monopoly game messages

# Game info
game-name-monopoly = Monopoly

# Lobby options
monopoly-set-preset = Tryb: { $preset }
monopoly-select-preset = Wybierz tryb Monopoly
monopoly-option-changed-preset = Ustawiono tryb { $preset }.

# Preset labels
monopoly-preset-classic-standard = Klasyczny i tematyczny standard
monopoly-preset-junior = Monopoly Junior
monopoly-preset-junior-modern = Monopoly Junior (nowoczesny)
monopoly-preset-junior-legacy = Monopoly Junior (klasyczny)
monopoly-preset-cheaters = Monopoly Edycja Oszustów
monopoly-preset-electronic-banking = Bankowość elektroniczna
monopoly-preset-voice-banking = Bankowość głosowa
monopoly-preset-sore-losers = Monopoly dla złych przegranych
monopoly-preset-speed = Monopoly Speed
monopoly-preset-builder = Monopoly Builder
monopoly-preset-city = Monopoly City
monopoly-preset-bid-card-game = Monopoly Bid
monopoly-preset-deal-card-game = Monopoly Deal
monopoly-preset-knockout = Monopoly Knockout
monopoly-preset-free-parking-jackpot = Jackpot na Darmowym Parkingu

# Scaffold status
monopoly-announce-preset = Odczytaj bieżący tryb
monopoly-current-preset = Bieżący tryb: { $preset } ({ $count } edycji).
monopoly-scaffold-started = Uruchomiono Monopoly w trybie { $preset } ({ $count } edycji).

# Turn actions
monopoly-roll-dice = Rzuć kostkami
monopoly-buy-property = Kup nieruchomość
monopoly-banking-balance = Sprawdź saldo bankowe
monopoly-banking-transfer = Przelej środki
monopoly-banking-ledger = Przejrzyj historię bankową
monopoly-voice-command = Polecenie głosowe
monopoly-cheaters-claim-reward = Odbierz nagrodę za oszustwo
monopoly-end-turn = Zakończ turę

# Turn validation
monopoly-roll-first = Musisz najpierw rzucić.
monopoly-already-rolled = W tej turze już rzuciłeś.
monopoly-no-property-to-buy = Obecnie nie ma nieruchomości do kupienia.
monopoly-property-owned = Ta nieruchomość ma już właściciela.
monopoly-not-enough-cash = Nie masz wystarczającej gotówki.
monopoly-action-disabled-for-preset = Ta akcja jest wyłączona dla wybranego trybu.
monopoly-buy-disabled = Bezpośredni zakup nieruchomości jest wyłączony w tym trybie.

# Turn events
monopoly-pass-go = { $player } przeszedł przez START i otrzymał { $amount } (gotówka: { $cash }).
monopoly-roll-result = { $player } wyrzucił { $die1 } + { $die2 } = { $total } i stanął na polu { $space }.
monopoly-roll-only = { $player } wyrzucił { $die1 } + { $die2 } = { $total }.
monopoly-you-roll-result = Wyrzuciłeś { $die1 } + { $die2 } = { $total } i stanąłeś na polu { $space }.
monopoly-player-roll-result = { $player } wyrzucił { $die1 } + { $die2 } = { $total } i stanął na polu { $space }.
monopoly-you-roll-only = Wyrzuciłeś { $die1 } + { $die2 } = { $total }.
monopoly-player-roll-only = { $player } wyrzucił { $die1 } + { $die2 } = { $total }.
monopoly-you-roll-only-doubles = Wyrzuciłeś { $die1 } + { $die2 } = { $total }. Dublet!
monopoly-player-roll-only-doubles = { $player } wyrzucił { $die1 } + { $die2 } = { $total }. Dublet!
monopoly-property-available = { $property } jest dostępna za { $price }.
monopoly-property-bought = { $player } kupił { $property } za { $price } (gotówka: { $cash }).
monopoly-rent-paid = { $player } zapłacił { $amount } czynszu graczowi { $owner } za { $property }.
monopoly-player-paid-player = { $player } zapłacił { $amount } graczowi { $target }.
monopoly-landed-owned = { $player } stanął na swojej własnej nieruchomości: { $property }.
monopoly-tax-paid = { $player } zapłacił { $amount } za pole { $tax } (gotówka: { $cash }).
monopoly-go-to-jail = { $player } idzie do więzienia (przeniesiono na { $space }).
monopoly-bankrupt-player = Zbankrutowałeś i odpadasz z gry.
monopoly-player-bankrupt = { $player } zbankrutował. Wierzyciel: { $creditor }.
monopoly-winner-by-bankruptcy = { $player } wygrywa przez bankructwo z pozostałą gotówką { $cash }.
monopoly-winner-by-cash = { $player } wygrywa z najwyższą ilością gotówki: { $cash }.
monopoly-city-winner-by-value = { $player } wygrywa Monopoly City z końcową wartością { $total }.

# Additional actions
monopoly-auction-property = Zlicytuj nieruchomość
monopoly-auction-bid = Złóż ofertę w licytacji
monopoly-auction-pass = Pasuj w licytacji
monopoly-mortgage-property = Zastaw nieruchomość
monopoly-unmortgage-property = Wykup nieruchomość z zastawu
monopoly-build-house = Zbuduj dom lub hotel
monopoly-sell-house = Sprzedaj dom lub hotel
monopoly-offer-trade = Zaoferuj wymianę
monopoly-accept-trade = Przyjmij wymianę
monopoly-decline-trade = Odrzuć wymianę
monopoly-read-cash = Odczytaj gotówkę
monopoly-pay-bail = Zapłać kaucję
monopoly-use-jail-card = Użyj karty wyjścia z więzienia
monopoly-cash-report = Masz { $cash } gotówki.
monopoly-property-amount-option = { $property } za { $amount }
monopoly-banking-transfer-option = Przelej { $amount } do gracza { $target }

# Additional prompts
monopoly-select-property-mortgage = Wybierz nieruchomość do zastawienia
monopoly-select-property-unmortgage = Wybierz nieruchomość do wykupu z zastawu
monopoly-select-property-build = Wybierz nieruchomość do zabudowy
monopoly-select-property-sell = Wybierz nieruchomość, z której chcesz sprzedać budynek
monopoly-select-trade-offer = Wybierz ofertę wymiany
monopoly-select-auction-bid = Wybierz swoją ofertę licytacji
monopoly-select-banking-transfer = Wybierz przelew
monopoly-select-voice-command = Wpisz polecenie głosowe rozpoczynające się od voice:

# Additional validation
monopoly-no-property-to-auction = Obecnie nie ma nieruchomości do licytacji.
monopoly-auction-active = Najpierw zakończ aktywną licytację.
monopoly-no-auction-active = Żadna licytacja nie jest w toku.
monopoly-not-your-auction-turn = To nie twoja kolej w licytacji.
monopoly-no-mortgage-options = Nie masz nieruchomości dostępnych do zastawienia.
monopoly-no-unmortgage-options = Nie masz zastawionych nieruchomości do wykupu.
monopoly-no-build-options = Nie masz nieruchomości dostępnych do zabudowy.
monopoly-no-sell-options = Nie masz nieruchomości z budynkami dostępnych do sprzedaży.
monopoly-no-trade-options = Nie masz obecnie żadnych prawidłowych ofert wymiany.
monopoly-no-trade-pending = Nie ma dla ciebie oczekującej wymiany.
monopoly-trade-pending = Wymiana już oczekuje.
monopoly-trade-no-longer-valid = Ta wymiana nie jest już ważna.
monopoly-not-in-jail = Nie jesteś w więzieniu.
monopoly-no-jail-card = Nie masz karty wyjścia z więzienia.
monopoly-roll-again-required = Wyrzuciłeś dublet i musisz rzucić ponownie.
monopoly-resolve-property-first = Najpierw rozstrzygnij oczekującą decyzję dotyczącą nieruchomości.

# Additional turn events
monopoly-roll-again = { $player } wyrzucił dublet i rzuca jeszcze raz.
monopoly-you-roll-again = Wyrzuciłeś dublet i możesz rzucić ponownie.
monopoly-player-roll-again = { $player } wyrzucił dublet i rzuca jeszcze raz.
monopoly-jail-roll-doubles = { $player } wyrzucił dublet ({ $die1 } i { $die2 }) i wychodzi z więzienia.
monopoly-you-jail-roll-doubles = Wyrzuciłeś dublet ({ $die1 } i { $die2 }) i wychodzisz z więzienia.
monopoly-player-jail-roll-doubles = { $player } wyrzucił dublet ({ $die1 } i { $die2 }) i wychodzi z więzienia.
monopoly-jail-roll-failed = { $player } wyrzucił w więzieniu { $die1 } i { $die2 } (próba { $attempts }).
monopoly-bail-paid = { $player } zapłacił { $amount } kaucji (gotówka: { $cash }).
monopoly-three-doubles-jail = { $player } wyrzucił trzy dublety w jednej turze i trafia do więzienia.
monopoly-you-three-doubles-jail = Wyrzuciłeś trzy dublety w jednej turze i trafiasz do więzienia.
monopoly-player-three-doubles-jail = { $player } wyrzucił trzy dublety w jednej turze i trafia do więzienia.
monopoly-jail-card-used = { $player } użył karty wyjścia z więzienia (pozostało: { $cards }).
monopoly-sore-loser-rebate = { $player } otrzymał zwrot dla przegranego w wysokości { $amount } (gotówka: { $cash }).
monopoly-cheaters-early-end-turn-blocked = { $player } próbował za wcześnie zakończyć turę i zapłacił karę za oszustwo w wysokości { $amount } (gotówka: { $cash }).
monopoly-cheaters-payment-avoidance-blocked = { $player } uruchomił karę za unikanie płatności w wysokości { $amount } (gotówka: { $cash }).
monopoly-cheaters-reward-granted = { $player } odebrał nagrodę oszusta w wysokości { $amount } (gotówka: { $cash }).
monopoly-cheaters-reward-unavailable = { $player } już odebrał nagrodę oszusta w tej turze.

# Auctions and mortgages
monopoly-auction-no-bids = Brak ofert dla { $property }. Pole pozostaje niesprzedane.
monopoly-auction-started = Rozpoczęto licytację dla pola { $property } (oferta otwarcia: { $amount }).
monopoly-auction-turn = Tura licytacji: ruch gracza { $player } dla pola { $property } (bieżąca oferta: { $amount }).
monopoly-auction-bid-placed = { $player } zaoferował { $amount } za { $property }.
monopoly-auction-pass-event = { $player } spasował przy polu { $property }.
monopoly-auction-won = { $player } wygrał licytację pola { $property } za { $amount } (gotówka: { $cash }).
monopoly-property-mortgaged = { $player } zastawił { $property } za { $amount } (gotówka: { $cash }).
monopoly-property-unmortgaged = { $player } wykupił z zastawu { $property } za { $amount } (gotówka: { $cash }).
monopoly-house-built = { $player } zabudował pole { $property } za { $amount } (poziom: { $level }, gotówka: { $cash }).
monopoly-house-sold = { $player } sprzedał budynek na polu { $property } za { $amount } (poziom: { $level }, gotówka: { $cash }).
monopoly-trade-offered = { $proposer } zaoferował graczowi { $target } wymianę: { $offer }.
monopoly-trade-completed = Wymiana między { $proposer } a { $target } została zakończona: { $offer }.
monopoly-trade-declined = { $target } odrzucił wymianę od { $proposer }: { $offer }.
monopoly-trade-cancelled = Wymiana anulowana: { $offer }.
monopoly-free-parking-jackpot = { $player } zebrał jackpot z Darmowego Parkingu w wysokości { $amount } (gotówka: { $cash }).
monopoly-mortgaged-no-rent = { $player } stanął na zastawionym polu { $property }; czynsz nie jest należny.
monopoly-builder-blocks-awarded = { $player } zdobył { $amount } bloków budowniczego ({ $blocks } łącznie).
monopoly-builder-block-spent = { $player } zużył blok budowniczego (pozostało: { $blocks }).
monopoly-banking-transfer-success = { $from_player } przelał { $amount } do gracza { $to_player }.
monopoly-banking-transfer-failed = Przelew bankowy gracza { $player } nie powiódł się ({ $reason }).
monopoly-banking-balance-report = Saldo bankowe gracza { $player }: { $cash }.
monopoly-banking-ledger-report = Ostatnia aktywność bankowa: { $entries }.
monopoly-banking-ledger-empty = Brak transakcji bankowych.
monopoly-voice-command-error = Błąd polecenia głosowego: { $reason }.
monopoly-voice-command-accepted = Polecenie głosowe zaakceptowane: { $intent }.
monopoly-voice-command-repeat = Powtarzam ostatni kod odpowiedzi bankowej: { $response }.
monopoly-voice-transfer-staged = Przygotowano przelew głosowy: { $amount } do gracza { $target }. Powiedz voice: confirm transfer.
monopoly-mortgage-transfer-interest-paid = { $player } zapłacił { $amount } odsetek za przejęcie zastawu (gotówka: { $cash }).

# Card engine
monopoly-card-drawn = { $player } dobrał kartę { $deck }: { $card }.
monopoly-card-collect = { $player } otrzymał { $amount } (gotówka: { $cash }).
monopoly-card-pay = { $player } zapłacił { $amount } (gotówka: { $cash }).
monopoly-card-move = { $player } przeniósł się na pole { $space }.
monopoly-card-jail-free = { $player } otrzymał kartę wyjścia z więzienia ({ $cards } łącznie).
monopoly-card-utility-roll = { $player } wyrzucił { $die1 } + { $die2 } = { $total } dla czynszu za wodociągi/elektrownię.
monopoly-deck-chance = Szansa
monopoly-deck-community-chest = Kasa Społeczna

# Card descriptions
monopoly-card-advance-to-go = Idź na START i pobierz { $amount }
monopoly-card-advance-to-illinois-avenue = Przejdź na Illinois Avenue
monopoly-card-advance-to-st-charles-place = Przejdź na St. Charles Place
monopoly-card-advance-to-nearest-utility = Przejdź do najbliższych wodociągów lub elektrowni
monopoly-card-advance-to-nearest-railroad = Przejdź do najbliższej kolei i zapłać podwójny czynsz, jeśli ma właściciela
monopoly-card-bank-dividend-50 = Bank wypłaca ci dywidendę { $amount }
monopoly-card-go-back-three = Cofnij się o 3 pola
monopoly-card-go-to-jail = Idź prosto do więzienia
monopoly-card-general-repairs = Wykonaj generalne naprawy wszystkich swoich nieruchomości: { $per_house } za dom, { $per_hotel } za hotel
monopoly-card-poor-tax-15 = Zapłać podatek { $amount }
monopoly-card-reading-railroad = Udaj się na Reading Railroad
monopoly-card-boardwalk = Udaj się na Boardwalk
monopoly-card-chairman-of-the-board = Przewodniczący zarządu, zapłać każdemu graczowi { $amount }
monopoly-card-building-loan-matures = Twój kredyt budowlany dojrzewa, pobierz { $amount }
monopoly-card-crossword-competition = Wygrałeś konkurs krzyżówkowy, pobierz { $amount }
monopoly-card-bank-error-200 = Błąd banku na twoją korzyść, pobierz { $amount }
monopoly-card-doctor-fee-50 = Opłata lekarska, zapłać { $amount }
monopoly-card-sale-of-stock-50 = Ze sprzedaży akcji otrzymujesz { $amount }
monopoly-card-holiday-fund = Fundusz urlopowy dojrzał, otrzymaj { $amount }
monopoly-card-tax-refund-20 = Zwrot podatku dochodowego, pobierz { $amount }
monopoly-card-birthday = To twoje urodziny, pobierz { $amount } od każdego gracza
monopoly-card-life-insurance = Polisa na życie dojrzała, pobierz { $amount }
monopoly-card-hospital-fees-100 = Zapłać rachunki szpitalne w wysokości { $amount }
monopoly-card-school-fees-50 = Zapłać czesne w wysokości { $amount }
monopoly-card-consultancy-fee-25 = Otrzymaj { $amount } za konsultacje
monopoly-card-street-repairs = Zapłać za naprawy ulic: { $per_house } za dom, { $per_hotel } za hotel
monopoly-card-beauty-contest-10 = Zdobyłeś drugą nagrodę w konkursie piękności, pobierz { $amount }
monopoly-card-inherit-100 = Dziedziczysz { $amount }
monopoly-card-get-out-of-jail = Wyjdź z więzienia za darmo

# Board profile options
monopoly-set-board = Plansza: { $board }
monopoly-select-board = Wybierz planszę Monopoly
monopoly-option-changed-board = Ustawiono planszę { $board }.
monopoly-set-board-rules-mode = Tryb zasad planszy: { $mode }
monopoly-select-board-rules-mode = Wybierz tryb zasad planszy
monopoly-option-changed-board-rules-mode = Ustawiono tryb zasad planszy na { $mode }.

# Board labels
monopoly-board-classic-default = Klasyczna plansza
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
monopoly-board-star-wars-mandalorian-s2 = Star Wars Mandalorian Season 2
monopoly-board-transformers-beast-wars = Transformers Beast Wars
monopoly-board-marvel-falcon-winter-soldier = Marvel Falcon and Winter Soldier
monopoly-board-fortnite-flip = Fortnite Flip Edition
monopoly-board-marvel-flip = Marvel Flip Edition
monopoly-board-pokemon = Pokemon Edition

# Board rules mode labels
monopoly-board-rules-mode-auto = Automatycznie
monopoly-board-rules-mode-skin-only = Tylko skórka

# Board runtime announcements
monopoly-board-preset-autofixed = Plansza { $board } jest niezgodna z trybem { $from_preset }; przełączono na { $to_preset }.
monopoly-board-rules-simplified = Zasady planszy { $board } są zaimplementowane częściowo; dla brakujących mechanik używane są zasady podstawowe.
monopoly-board-active = Aktywna plansza: { $board } (tryb: { $mode }).

# Deed and ownership browsing
monopoly-view-active-deed = Pokaż aktywny akt własności
monopoly-view-active-deed-space = Pokaż { $property }
monopoly-browse-all-deeds = Przeglądaj wszystkie akty własności
monopoly-view-my-properties = Pokaż moje nieruchomości
monopoly-view-player-properties = Pokaż informacje o graczu
monopoly-view-selected-deed = Pokaż wybrany akt własności
monopoly-view-selected-owner-property-deed = Pokaż akt własności wybranego gracza
monopoly-select-property-deed = Wybierz akt własności nieruchomości
monopoly-select-player-properties = Wybierz gracza
monopoly-select-player-property-deed = Wybierz akt własności nieruchomości gracza
monopoly-no-active-deed = Nie ma teraz aktywnego aktu własności do wyświetlenia.
monopoly-no-deeds-available = Na tej planszy nie ma pól z aktami własności.
monopoly-no-owned-properties = Brak posiadanych nieruchomości do tego widoku.
monopoly-no-players-with-properties = Brak dostępnych graczy.
monopoly-buy-for = Kup za { $amount }
monopoly-you-have-no-owned-properties = Nie posiadasz żadnych nieruchomości.
monopoly-player-has-no-owned-properties = { $player } nie posiada żadnych nieruchomości.
monopoly-owner-bank = Bank
monopoly-owner-unknown = Nieznany
monopoly-building-status-hotel = z hotelem
monopoly-building-status-one-house = z 1 domem
monopoly-building-status-houses = z { $count } domami
monopoly-mortgaged-short = zastawione
monopoly-deed-menu-label = { $property } ({ $owner })
monopoly-deed-menu-label-extra = { $property } ({ $owner }; { $extras })
monopoly-color-brown = Brązowy
monopoly-color-light_blue = Jasnoniebieski
monopoly-color-pink = Różowy
monopoly-color-orange = Pomarańczowy
monopoly-color-red = Czerwony
monopoly-color-yellow = Żółty
monopoly-color-green = Zielony
monopoly-color-dark_blue = Ciemnoniebieski
monopoly-deed-type-color-group = Typ: grupa koloru { $color }
monopoly-deed-type-railroad = Typ: kolej
monopoly-deed-type-utility = Typ: przedsiębiorstwo użyteczności publicznej
monopoly-deed-type-generic = Typ: { $kind }
monopoly-deed-purchase-price = Cena zakupu: { $amount }
monopoly-deed-rent = Czynsz: { $amount }
monopoly-deed-full-set-rent = Jeśli właściciel ma pełny komplet koloru: { $amount }
monopoly-deed-rent-one-house = Z 1 domem: { $amount }
monopoly-deed-rent-houses = Z { $count } domami: { $amount }
monopoly-deed-rent-hotel = Z hotelem: { $amount }
monopoly-deed-house-cost = Koszt domu: { $amount }
monopoly-deed-railroad-rent = Czynsz przy { $count } kolejach: { $amount }
monopoly-deed-utility-one-owned = Jeśli posiadane jest jedno przedsiębiorstwo: 4x wynik rzutu
monopoly-deed-utility-both-owned = Jeśli posiadane są oba przedsiębiorstwa: 10x wynik rzutu
monopoly-deed-utility-base-rent = Bazowy czynsz przedsiębiorstwa (stary wariant): { $amount }
monopoly-deed-mortgage-value = Wartość zastawu: { $amount }
monopoly-deed-unmortgage-cost = Koszt wykupu z zastawu: { $amount }
monopoly-deed-owner = Właściciel: { $owner }
monopoly-deed-current-buildings = Obecna zabudowa: { $buildings }
monopoly-deed-status-mortgaged = Status: zastawione
monopoly-player-properties-label = { $player }, na polu { $space }, pole { $position }
monopoly-player-properties-label-no-space = { $player }, pole { $position }
monopoly-banking-ledger-entry-success = { $tx_id } { $kind } { $from_id }->{ $to_id } { $amount } ({ $reason })
monopoly-banking-ledger-entry-failed = { $tx_id } { $kind } niepowodzenie ({ $reason })

# Trade menu summaries
monopoly-trade-buy-property-summary = Kup { $property } od gracza { $target } za { $amount }
monopoly-trade-offer-cash-for-property-summary = Zaoferuj { $amount } graczowi { $target } za { $property }
monopoly-trade-sell-property-summary = Sprzedaj { $property } graczowi { $target } za { $amount }
monopoly-trade-offer-property-for-cash-summary = Zaoferuj { $property } graczowi { $target } za { $amount }
monopoly-trade-swap-summary = Wymień { $give_property } z graczem { $target } na { $receive_property }
monopoly-trade-swap-plus-cash-summary = Wymień { $give_property } + { $amount } z graczem { $target } na { $receive_property }
monopoly-trade-swap-receive-cash-summary = Wymień { $give_property } na { $receive_property } + { $amount } od gracza { $target }
monopoly-trade-buy-jail-card-summary = Kup kartę wyjścia z więzienia od gracza { $target } za { $amount }
monopoly-trade-sell-jail-card-summary = Sprzedaj kartę wyjścia z więzienia graczowi { $target } za { $amount }

# Board space names
monopoly-space-go = START
monopoly-space-mediterranean_avenue = Mediterranean Avenue
monopoly-space-community_chest_1 = Kasa Społeczna
monopoly-space-baltic_avenue = Baltic Avenue
monopoly-space-income_tax = Podatek dochodowy
monopoly-space-reading_railroad = Reading Railroad
monopoly-space-oriental_avenue = Oriental Avenue
monopoly-space-chance_1 = Szansa
monopoly-space-vermont_avenue = Vermont Avenue
monopoly-space-connecticut_avenue = Connecticut Avenue
monopoly-space-jail = Więzienie / Tylko w odwiedzinach
monopoly-space-st_charles_place = St. Charles Place
monopoly-space-electric_company = Elektrownia
monopoly-space-states_avenue = States Avenue
monopoly-space-virginia_avenue = Virginia Avenue
monopoly-space-pennsylvania_railroad = Pennsylvania Railroad
monopoly-space-st_james_place = St. James Place
monopoly-space-community_chest_2 = Kasa Społeczna
monopoly-space-tennessee_avenue = Tennessee Avenue
monopoly-space-new_york_avenue = New York Avenue
monopoly-space-free_parking = Darmowy Parking
monopoly-space-kentucky_avenue = Kentucky Avenue
monopoly-space-chance_2 = Szansa
monopoly-space-indiana_avenue = Indiana Avenue
monopoly-space-illinois_avenue = Illinois Avenue
monopoly-space-bo_railroad = B. & O. Railroad
monopoly-space-atlantic_avenue = Atlantic Avenue
monopoly-space-ventnor_avenue = Ventnor Avenue
monopoly-space-water_works = Wodociągi
monopoly-space-marvin_gardens = Marvin Gardens
monopoly-space-go_to_jail = Idź do więzienia
monopoly-space-pacific_avenue = Pacific Avenue
monopoly-space-north_carolina_avenue = North Carolina Avenue
monopoly-space-community_chest_3 = Kasa Społeczna
monopoly-space-pennsylvania_avenue = Pennsylvania Avenue
monopoly-space-short_line = Short Line
monopoly-space-chance_3 = Szansa
monopoly-space-park_place = Park Place
monopoly-space-luxury_tax = Podatek od luksusu
monopoly-space-boardwalk = Boardwalk
