# Monopoly game messages

# Game info
game-name-monopoly = Monopoly

# Lobby options
monopoly-set-preset = Preset: { $preset }
monopoly-select-preset = Select a Monopoly preset
monopoly-option-changed-preset = Preset set to { $preset }.

# Preset labels
monopoly-preset-classic-standard = Classic and Themed Standard
monopoly-preset-junior = Monopoly Junior
monopoly-preset-junior-modern = Monopoly Junior (Modern)
monopoly-preset-junior-legacy = Monopoly Junior (Legacy)
monopoly-preset-cheaters = Monopoly Cheaters Edition
monopoly-preset-electronic-banking = Electronic Banking
monopoly-preset-voice-banking = Voice Banking
monopoly-preset-sore-losers = Monopoly for Sore Losers
monopoly-preset-speed = Monopoly Speed
monopoly-preset-builder = Monopoly Builder
monopoly-preset-city = Monopoly City
monopoly-preset-bid-card-game = Monopoly Bid
monopoly-preset-deal-card-game = Monopoly Deal
monopoly-preset-knockout = Monopoly Knockout
monopoly-preset-free-parking-jackpot = Free Parking Jackpot

# Scaffold status
monopoly-announce-preset = Announce current preset
monopoly-current-preset = Current preset: { $preset } ({ $count } editions).
monopoly-scaffold-started = Monopoly scaffold started with { $preset } ({ $count } editions).

# Turn actions
monopoly-roll-dice = Roll dice
monopoly-buy-property = Buy property
monopoly-banking-balance = Check bank balance
monopoly-banking-transfer = Transfer funds
monopoly-banking-ledger = Review bank ledger
monopoly-end-turn = End turn

# Turn validation
monopoly-roll-first = You need to roll first.
monopoly-already-rolled = You already rolled this turn.
monopoly-no-property-to-buy = There is no property to buy right now.
monopoly-property-owned = That property is already owned.
monopoly-not-enough-cash = You don't have enough cash.
monopoly-action-disabled-for-preset = This action is disabled for the selected preset.
monopoly-buy-disabled = Buying property directly is disabled for this preset.

# Turn events
monopoly-pass-go = { $player } passed GO and collected { $amount } (cash: { $cash }).
monopoly-roll-result = { $player } rolled { $die1 } + { $die2 } = { $total } and landed on { $space }.
monopoly-property-available = { $property } is available for { $price }.
monopoly-property-bought = { $player } bought { $property } for { $price } (cash: { $cash }).
monopoly-rent-paid = { $player } paid { $amount } in rent to { $owner } for { $property }.
monopoly-landed-owned = { $player } landed on their own property: { $property }.
monopoly-tax-paid = { $player } paid { $amount } for { $tax } (cash: { $cash }).
monopoly-go-to-jail = { $player } goes to jail (moved to { $space }).
monopoly-bankrupt-player = You are bankrupt and out of the game.
monopoly-player-bankrupt = { $player } is bankrupt. Creditor: { $creditor }.
monopoly-winner-by-bankruptcy = { $player } wins by bankruptcy with { $cash } cash remaining.
monopoly-winner-by-cash = { $player } wins with the highest cash total: { $cash }.

# Additional actions
monopoly-auction-property = Auction property
monopoly-auction-bid = Place auction bid
monopoly-auction-pass = Pass in auction
monopoly-mortgage-property = Mortgage property
monopoly-unmortgage-property = Unmortgage property
monopoly-build-house = Build house or hotel
monopoly-sell-house = Sell house or hotel
monopoly-offer-trade = Offer trade
monopoly-accept-trade = Accept trade
monopoly-decline-trade = Decline trade
monopoly-pay-bail = Pay bail
monopoly-use-jail-card = Use get-out-of-jail card

# Additional prompts
monopoly-select-property-mortgage = Select a property to mortgage
monopoly-select-property-unmortgage = Select a property to unmortgage
monopoly-select-property-build = Select a property to build on
monopoly-select-property-sell = Select a property to sell from
monopoly-select-trade-offer = Select a trade offer
monopoly-select-auction-bid = Select your auction bid
monopoly-select-banking-transfer = Select a transfer

# Additional validation
monopoly-no-property-to-auction = There is no property to auction right now.
monopoly-auction-active = Resolve the active auction first.
monopoly-no-auction-active = There is no auction in progress.
monopoly-not-your-auction-turn = It is not your turn in the auction.
monopoly-no-mortgage-options = You do not have properties available to mortgage.
monopoly-no-unmortgage-options = You do not have mortgaged properties to unmortgage.
monopoly-no-build-options = You do not have properties available to build on.
monopoly-no-sell-options = You do not have properties with buildings available to sell.
monopoly-no-trade-options = You do not have any valid trades to offer right now.
monopoly-no-trade-pending = There is no pending trade for you.
monopoly-trade-pending = A trade is already pending.
monopoly-trade-no-longer-valid = That trade is no longer valid.
monopoly-not-in-jail = You are not in jail.
monopoly-no-jail-card = You do not have a get-out-of-jail card.
monopoly-roll-again-required = You rolled doubles and must roll again.
monopoly-resolve-property-first = Resolve the pending property decision first.

# Additional turn events
monopoly-roll-again = { $player } rolled doubles and gets another roll.
monopoly-jail-roll-doubles = { $player } rolled doubles ({ $die1 } and { $die2 }) and leaves jail.
monopoly-jail-roll-failed = { $player } rolled { $die1 } and { $die2 } in jail (attempt { $attempts }).
monopoly-bail-paid = { $player } paid { $amount } bail (cash: { $cash }).
monopoly-three-doubles-jail = { $player } rolled three doubles in one turn and is sent to jail.
monopoly-jail-card-used = { $player } used a get-out-of-jail card ({ $cards } remaining).
monopoly-sore-loser-rebate = { $player } received a sore loser rebate of { $amount } (cash: { $cash }).

# Auctions and mortgages
monopoly-auction-no-bids = No bids for { $property }. It remains unsold.
monopoly-auction-started = Auction started for { $property } (opening bid: { $amount }).
monopoly-auction-turn = Auction turn: { $player } to act on { $property } (current bid: { $amount }).
monopoly-auction-bid-placed = { $player } bid { $amount } for { $property }.
monopoly-auction-pass-event = { $player } passed on { $property }.
monopoly-auction-won = { $player } won the auction for { $property } at { $amount } (cash: { $cash }).
monopoly-property-mortgaged = { $player } mortgaged { $property } for { $amount } (cash: { $cash }).
monopoly-property-unmortgaged = { $player } unmortgaged { $property } for { $amount } (cash: { $cash }).
monopoly-house-built = { $player } built on { $property } for { $amount } (level: { $level }, cash: { $cash }).
monopoly-house-sold = { $player } sold a building on { $property } for { $amount } (level: { $level }, cash: { $cash }).
monopoly-trade-offered = { $proposer } offered { $target } a trade: { $offer }.
monopoly-trade-completed = Trade completed between { $proposer } and { $target }: { $offer }.
monopoly-trade-declined = { $target } declined trade from { $proposer }: { $offer }.
monopoly-trade-cancelled = Trade cancelled: { $offer }.
monopoly-free-parking-jackpot = { $player } collected the Free Parking jackpot of { $amount } (cash: { $cash }).
monopoly-mortgaged-no-rent = { $player } landed on mortgaged { $property }; no rent is due.
monopoly-builder-blocks-awarded = { $player } gained { $amount } builder blocks ({ $blocks } total).
monopoly-builder-block-spent = { $player } spent a builder block ({ $blocks } remaining).
monopoly-banking-transfer-success = { $from_player } transferred { $amount } to { $to_player }.
monopoly-banking-transfer-failed = { $player } bank transfer failed ({ $reason }).
monopoly-banking-balance-report = { $player } bank balance: { $cash }.
monopoly-banking-ledger-report = Recent banking activity: { $entries }.
monopoly-banking-ledger-empty = No banking transactions yet.

# Card engine
monopoly-card-drawn = { $player } drew a { $deck } card: { $card }.
monopoly-card-collect = { $player } collected { $amount } (cash: { $cash }).
monopoly-card-pay = { $player } paid { $amount } (cash: { $cash }).
monopoly-card-move = { $player } moved to { $space }.
monopoly-card-jail-free = { $player } received a get-out-of-jail card ({ $cards } total).

# Card descriptions
monopoly-card-advance-to-go = Advance to GO and collect 200
monopoly-card-bank-dividend-50 = Bank pays you dividend of 50
monopoly-card-go-back-three = Go back 3 spaces
monopoly-card-go-to-jail = Go directly to jail
monopoly-card-poor-tax-15 = Pay poor tax of 15
monopoly-card-bank-error-200 = Bank error in your favor, collect 200
monopoly-card-doctor-fee-50 = Doctor's fee, pay 50
monopoly-card-tax-refund-20 = Income tax refund, collect 20
monopoly-card-get-out-of-jail = Get out of jail free
