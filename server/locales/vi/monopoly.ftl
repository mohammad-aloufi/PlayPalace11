# Monopoly game messages

# Game info
game-name-monopoly = Monopoly

# Lobby options
monopoly-set-preset = Chế độ: { $preset }
monopoly-select-preset = Chọn chế độ Monopoly
monopoly-option-changed-preset = Đã đặt chế độ thành { $preset }.

# Preset labels
monopoly-preset-classic-standard = Cổ điển và chủ đề tiêu chuẩn
monopoly-preset-junior = Monopoly Junior
monopoly-preset-junior-modern = Monopoly Junior (hiện đại)
monopoly-preset-junior-legacy = Monopoly Junior (cũ)
monopoly-preset-cheaters = Monopoly bản gian lận
monopoly-preset-electronic-banking = Ngân hàng điện tử
monopoly-preset-voice-banking = Ngân hàng giọng nói
monopoly-preset-sore-losers = Monopoly cho người thua cay cú
monopoly-preset-speed = Monopoly Speed
monopoly-preset-builder = Monopoly Builder
monopoly-preset-city = Monopoly City
monopoly-preset-bid-card-game = Monopoly Bid
monopoly-preset-deal-card-game = Monopoly Deal
monopoly-preset-knockout = Monopoly Knockout
monopoly-preset-free-parking-jackpot = Jackpot Bãi đỗ xe miễn phí

# Scaffold status
monopoly-announce-preset = Đọc chế độ hiện tại
monopoly-current-preset = Chế độ hiện tại: { $preset } ({ $count } phiên bản).
monopoly-scaffold-started = Đã khởi động Monopoly với { $preset } ({ $count } phiên bản).

# Turn actions
monopoly-roll-dice = Tung xúc xắc
monopoly-buy-property = Mua bất động sản
monopoly-banking-balance = Kiểm tra số dư ngân hàng
monopoly-banking-transfer = Chuyển tiền
monopoly-banking-ledger = Xem nhật ký ngân hàng
monopoly-voice-command = Lệnh giọng nói
monopoly-cheaters-claim-reward = Nhận thưởng gian lận
monopoly-end-turn = Kết thúc lượt

# Turn validation
monopoly-roll-first = Bạn cần tung xúc xắc trước.
monopoly-already-rolled = Bạn đã tung xúc xắc trong lượt này rồi.
monopoly-no-property-to-buy = Hiện không có bất động sản nào để mua.
monopoly-property-owned = Bất động sản đó đã có chủ.
monopoly-not-enough-cash = Bạn không có đủ tiền mặt.
monopoly-action-disabled-for-preset = Hành động này bị tắt trong chế độ đã chọn.
monopoly-buy-disabled = Chế độ này không cho phép mua bất động sản trực tiếp.

# Turn events
monopoly-pass-go = { $player } đi qua GO và nhận { $amount } (tiền mặt: { $cash }).
monopoly-roll-result = { $player } tung { $die1 } + { $die2 } = { $total } và dừng ở { $space }.
monopoly-roll-only = { $player } tung { $die1 } + { $die2 } = { $total }.
monopoly-you-roll-result = Bạn tung { $die1 } + { $die2 } = { $total } và dừng ở { $space }.
monopoly-player-roll-result = { $player } tung { $die1 } + { $die2 } = { $total } và dừng ở { $space }.
monopoly-you-roll-only = Bạn tung { $die1 } + { $die2 } = { $total }.
monopoly-player-roll-only = { $player } tung { $die1 } + { $die2 } = { $total }.
monopoly-you-roll-only-doubles = Bạn tung { $die1 } + { $die2 } = { $total }. Đôi!
monopoly-player-roll-only-doubles = { $player } tung { $die1 } + { $die2 } = { $total }. Đôi!
monopoly-property-available = { $property } đang được bán với giá { $price }.
monopoly-property-bought = { $player } đã mua { $property } với giá { $price } (tiền mặt: { $cash }).
monopoly-rent-paid = { $player } đã trả { $amount } tiền thuê cho { $owner } vì { $property }.
monopoly-player-paid-player = { $player } đã trả { $amount } cho { $target }.
monopoly-landed-owned = { $player } đáp xuống chính bất động sản của mình: { $property }.
monopoly-tax-paid = { $player } đã trả { $amount } cho { $tax } (tiền mặt: { $cash }).
monopoly-go-to-jail = { $player } vào tù (được chuyển đến { $space }).
monopoly-bankrupt-player = Bạn đã phá sản và bị loại khỏi trò chơi.
monopoly-player-bankrupt = { $player } đã phá sản. Chủ nợ: { $creditor }.
monopoly-winner-by-bankruptcy = { $player } thắng do các người chơi khác phá sản với { $cash } còn lại.
monopoly-winner-by-cash = { $player } thắng với số tiền mặt cao nhất: { $cash }.
monopoly-city-winner-by-value = { $player } thắng Monopoly City với tổng giá trị cuối cùng là { $total }.

# Additional actions
monopoly-auction-property = Đấu giá bất động sản
monopoly-auction-bid = Đặt giá đấu
monopoly-auction-pass = Bỏ lượt đấu giá
monopoly-mortgage-property = Thế chấp bất động sản
monopoly-unmortgage-property = Chuộc thế chấp
monopoly-build-house = Xây nhà hoặc khách sạn
monopoly-sell-house = Bán nhà hoặc khách sạn
monopoly-offer-trade = Đề nghị trao đổi
monopoly-accept-trade = Chấp nhận trao đổi
monopoly-decline-trade = Từ chối trao đổi
monopoly-read-cash = Đọc số tiền mặt
monopoly-pay-bail = Trả tiền bảo lãnh
monopoly-use-jail-card = Dùng thẻ ra tù
monopoly-cash-report = Bạn có { $cash } tiền mặt.
monopoly-property-amount-option = { $property } với giá { $amount }
monopoly-banking-transfer-option = Chuyển { $amount } cho { $target }

# Additional prompts
monopoly-select-property-mortgage = Chọn bất động sản để thế chấp
monopoly-select-property-unmortgage = Chọn bất động sản để chuộc thế chấp
monopoly-select-property-build = Chọn bất động sản để xây dựng
monopoly-select-property-sell = Chọn bất động sản để bán công trình
monopoly-select-trade-offer = Chọn một đề nghị trao đổi
monopoly-select-auction-bid = Chọn mức giá đấu của bạn
monopoly-select-banking-transfer = Chọn một khoản chuyển tiền
monopoly-select-voice-command = Nhập lệnh giọng nói bắt đầu bằng voice:

# Additional validation
monopoly-no-property-to-auction = Hiện không có bất động sản nào để đấu giá.
monopoly-auction-active = Hãy giải quyết cuộc đấu giá hiện tại trước.
monopoly-no-auction-active = Không có cuộc đấu giá nào đang diễn ra.
monopoly-not-your-auction-turn = Bây giờ không phải lượt của bạn trong đấu giá.
monopoly-no-mortgage-options = Bạn không có bất động sản nào có thể thế chấp.
monopoly-no-unmortgage-options = Bạn không có bất động sản nào đang thế chấp để chuộc.
monopoly-no-build-options = Bạn không có bất động sản nào có thể xây dựng.
monopoly-no-sell-options = Bạn không có bất động sản nào có công trình để bán.
monopoly-no-trade-options = Hiện bạn không có đề nghị trao đổi hợp lệ nào.
monopoly-no-trade-pending = Không có giao dịch nào đang chờ bạn.
monopoly-trade-pending = Đã có một giao dịch đang chờ xử lý.
monopoly-trade-no-longer-valid = Giao dịch đó không còn hợp lệ nữa.
monopoly-not-in-jail = Bạn không ở trong tù.
monopoly-no-jail-card = Bạn không có thẻ ra tù.
monopoly-roll-again-required = Bạn đã tung đôi và phải tung lại.
monopoly-resolve-property-first = Hãy giải quyết quyết định bất động sản đang chờ trước.

# Additional turn events
monopoly-roll-again = { $player } tung đôi và được tung tiếp.
monopoly-you-roll-again = Bạn tung đôi và được tung tiếp.
monopoly-player-roll-again = { $player } tung đôi và được tung tiếp.
monopoly-jail-roll-doubles = { $player } tung đôi ({ $die1 } và { $die2 }) và ra khỏi tù.
monopoly-you-jail-roll-doubles = Bạn tung đôi ({ $die1 } và { $die2 }) và ra khỏi tù.
monopoly-player-jail-roll-doubles = { $player } tung đôi ({ $die1 } và { $die2 }) và ra khỏi tù.
monopoly-jail-roll-failed = { $player } tung { $die1 } và { $die2 } trong tù (lần thử { $attempts }).
monopoly-bail-paid = { $player } đã trả { $amount } tiền bảo lãnh (tiền mặt: { $cash }).
monopoly-three-doubles-jail = { $player } tung ba lần đôi trong một lượt và bị đưa vào tù.
monopoly-you-three-doubles-jail = Bạn tung ba lần đôi trong một lượt và bị đưa vào tù.
monopoly-player-three-doubles-jail = { $player } tung ba lần đôi trong một lượt và bị đưa vào tù.
monopoly-jail-card-used = { $player } đã dùng thẻ ra tù ({ $cards } còn lại).
monopoly-sore-loser-rebate = { $player } nhận khoản hoàn lại cho người thua cay cú là { $amount } (tiền mặt: { $cash }).
monopoly-cheaters-early-end-turn-blocked = { $player } cố kết thúc lượt quá sớm và bị phạt gian lận { $amount } (tiền mặt: { $cash }).
monopoly-cheaters-payment-avoidance-blocked = { $player } bị phạt vì né thanh toán số tiền { $amount } (tiền mặt: { $cash }).
monopoly-cheaters-reward-granted = { $player } nhận thưởng gian lận { $amount } (tiền mặt: { $cash }).
monopoly-cheaters-reward-unavailable = { $player } đã nhận thưởng gian lận trong lượt này rồi.

# Auctions and mortgages
monopoly-auction-no-bids = Không có ai trả giá cho { $property }. Ô đó vẫn chưa được bán.
monopoly-auction-started = Đã bắt đầu đấu giá cho { $property } (giá mở đầu: { $amount }).
monopoly-auction-turn = Lượt đấu giá: { $player } hành động với { $property } (giá hiện tại: { $amount }).
monopoly-auction-bid-placed = { $player } đã trả { $amount } cho { $property }.
monopoly-auction-pass-event = { $player } đã bỏ qua { $property }.
monopoly-auction-won = { $player } thắng cuộc đấu giá { $property } với giá { $amount } (tiền mặt: { $cash }).
monopoly-property-mortgaged = { $player } đã thế chấp { $property } với giá { $amount } (tiền mặt: { $cash }).
monopoly-property-unmortgaged = { $player } đã chuộc thế chấp { $property } với giá { $amount } (tiền mặt: { $cash }).
monopoly-house-built = { $player } đã xây trên { $property } với giá { $amount } (cấp: { $level }, tiền mặt: { $cash }).
monopoly-house-sold = { $player } đã bán một công trình trên { $property } với giá { $amount } (cấp: { $level }, tiền mặt: { $cash }).
monopoly-trade-offered = { $proposer } đã đề nghị { $target } một giao dịch: { $offer }.
monopoly-trade-completed = Giao dịch giữa { $proposer } và { $target } đã hoàn tất: { $offer }.
monopoly-trade-declined = { $target } đã từ chối giao dịch từ { $proposer }: { $offer }.
monopoly-trade-cancelled = Đã hủy giao dịch: { $offer }.
monopoly-free-parking-jackpot = { $player } nhận jackpot Bãi đỗ xe miễn phí là { $amount } (tiền mặt: { $cash }).
monopoly-mortgaged-no-rent = { $player } đáp xuống { $property } đang thế chấp; không phải trả tiền thuê.
monopoly-builder-blocks-awarded = { $player } nhận được { $amount } khối xây dựng ({ $blocks } tổng cộng).
monopoly-builder-block-spent = { $player } đã dùng một khối xây dựng ({ $blocks } còn lại).
monopoly-banking-transfer-success = { $from_player } đã chuyển { $amount } cho { $to_player }.
monopoly-banking-transfer-failed = Chuyển khoản ngân hàng của { $player } thất bại ({ $reason }).
monopoly-banking-balance-report = Số dư ngân hàng của { $player }: { $cash }.
monopoly-banking-ledger-report = Hoạt động ngân hàng gần đây: { $entries }.
monopoly-banking-ledger-empty = Chưa có giao dịch ngân hàng nào.
monopoly-voice-command-error = Lỗi lệnh giọng nói: { $reason }.
monopoly-voice-command-accepted = Lệnh giọng nói đã được chấp nhận: { $intent }.
monopoly-voice-command-repeat = Lặp lại mã phản hồi ngân hàng gần nhất: { $response }.
monopoly-voice-transfer-staged = Đã chuẩn bị chuyển tiền bằng giọng nói: { $amount } cho { $target }. Hãy nói voice: confirm transfer.
monopoly-mortgage-transfer-interest-paid = { $player } đã trả { $amount } tiền lãi khi nhận bất động sản thế chấp (tiền mặt: { $cash }).

# Card engine
monopoly-card-drawn = { $player } rút một thẻ { $deck }: { $card }.
monopoly-card-collect = { $player } nhận được { $amount } (tiền mặt: { $cash }).
monopoly-card-pay = { $player } đã trả { $amount } (tiền mặt: { $cash }).
monopoly-card-move = { $player } được chuyển đến { $space }.
monopoly-card-jail-free = { $player } nhận một thẻ ra tù ({ $cards } tổng cộng).
monopoly-card-utility-roll = { $player } tung { $die1 } + { $die2 } = { $total } để tính tiền thuê tiện ích.
monopoly-deck-chance = Cơ hội
monopoly-deck-community-chest = Quỹ cộng đồng

# Card descriptions
monopoly-card-advance-to-go = Đi đến GO và nhận { $amount }
monopoly-card-advance-to-illinois-avenue = Tiến đến Illinois Avenue
monopoly-card-advance-to-st-charles-place = Tiến đến St. Charles Place
monopoly-card-advance-to-nearest-utility = Tiến đến công ty tiện ích gần nhất
monopoly-card-advance-to-nearest-railroad = Tiến đến tuyến đường sắt gần nhất và trả gấp đôi tiền thuê nếu đã có chủ
monopoly-card-bank-dividend-50 = Ngân hàng trả cho bạn cổ tức { $amount }
monopoly-card-go-back-three = Lùi 3 ô
monopoly-card-go-to-jail = Đi thẳng vào tù
monopoly-card-general-repairs = Sửa chữa toàn bộ tài sản của bạn: { $per_house } cho mỗi nhà, { $per_hotel } cho mỗi khách sạn
monopoly-card-poor-tax-15 = Trả thuế { $amount }
monopoly-card-reading-railroad = Đi đến Reading Railroad
monopoly-card-boardwalk = Đi dạo đến Boardwalk
monopoly-card-chairman-of-the-board = Chủ tịch hội đồng, trả cho mỗi người chơi { $amount }
monopoly-card-building-loan-matures = Khoản vay xây dựng của bạn đến hạn, nhận { $amount }
monopoly-card-crossword-competition = Bạn thắng cuộc thi ô chữ, nhận { $amount }
monopoly-card-bank-error-200 = Lỗi ngân hàng có lợi cho bạn, nhận { $amount }
monopoly-card-doctor-fee-50 = Phí bác sĩ, trả { $amount }
monopoly-card-sale-of-stock-50 = Bán cổ phiếu, bạn nhận { $amount }
monopoly-card-holiday-fund = Quỹ nghỉ lễ đến hạn, nhận { $amount }
monopoly-card-tax-refund-20 = Hoàn thuế thu nhập, nhận { $amount }
monopoly-card-birthday = Hôm nay là sinh nhật bạn, nhận { $amount } từ mỗi người chơi
monopoly-card-life-insurance = Bảo hiểm nhân thọ đến hạn, nhận { $amount }
monopoly-card-hospital-fees-100 = Trả phí bệnh viện { $amount }
monopoly-card-school-fees-50 = Trả học phí { $amount }
monopoly-card-consultancy-fee-25 = Nhận phí tư vấn { $amount }
monopoly-card-street-repairs = Bạn bị tính phí sửa đường: { $per_house } cho mỗi nhà, { $per_hotel } cho mỗi khách sạn
monopoly-card-beauty-contest-10 = Bạn đoạt giải nhì cuộc thi sắc đẹp, nhận { $amount }
monopoly-card-inherit-100 = Bạn được thừa kế { $amount }
monopoly-card-get-out-of-jail = Ra tù miễn phí

# Board profile options
monopoly-set-board = Bàn cờ: { $board }
monopoly-select-board = Chọn bàn cờ Monopoly
monopoly-option-changed-board = Đã đặt bàn cờ thành { $board }.
monopoly-set-board-rules-mode = Chế độ luật của bàn cờ: { $mode }
monopoly-select-board-rules-mode = Chọn chế độ luật của bàn cờ
monopoly-option-changed-board-rules-mode = Đã đặt chế độ luật của bàn cờ thành { $mode }.

# Board labels
monopoly-board-classic-default = Cổ điển mặc định
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
monopoly-board-rules-mode-auto = Tự động
monopoly-board-rules-mode-skin-only = Chỉ giao diện

# Board runtime announcements
monopoly-board-preset-autofixed = Bàn cờ { $board } không tương thích với { $from_preset }; đã chuyển sang { $to_preset }.
monopoly-board-rules-simplified = Luật của bàn cờ { $board } mới chỉ được triển khai một phần; những cơ chế còn thiếu sẽ dùng hành vi cơ bản của chế độ.
monopoly-board-active = Bàn cờ hiện tại: { $board } (chế độ: { $mode }).

# Deed and ownership browsing
monopoly-view-active-deed = Xem giấy chủ quyền hiện tại
monopoly-view-active-deed-space = Xem { $property }
monopoly-browse-all-deeds = Duyệt tất cả giấy chủ quyền
monopoly-view-my-properties = Xem bất động sản của tôi
monopoly-view-player-properties = Xem thông tin người chơi
monopoly-view-selected-deed = Xem giấy chủ quyền đã chọn
monopoly-view-selected-owner-property-deed = Xem giấy chủ quyền của người chơi đã chọn
monopoly-select-property-deed = Chọn giấy chủ quyền bất động sản
monopoly-select-player-properties = Chọn người chơi
monopoly-select-player-property-deed = Chọn giấy chủ quyền bất động sản của người chơi
monopoly-no-active-deed = Hiện không có giấy chủ quyền nào để xem.
monopoly-no-deeds-available = Không có ô bất động sản nào trên bàn cờ này có giấy chủ quyền để xem.
monopoly-no-owned-properties = Không có bất động sản đã sở hữu nào cho chế độ xem này.
monopoly-no-players-with-properties = Không có người chơi nào khả dụng.
monopoly-buy-for = Mua với giá { $amount }
monopoly-you-have-no-owned-properties = Bạn không sở hữu bất động sản nào.
monopoly-player-has-no-owned-properties = { $player } không sở hữu bất động sản nào.
monopoly-owner-bank = Ngân hàng
monopoly-owner-unknown = Không rõ
monopoly-building-status-hotel = có khách sạn
monopoly-building-status-one-house = có 1 căn nhà
monopoly-building-status-houses = có { $count } căn nhà
monopoly-mortgaged-short = đang thế chấp
monopoly-deed-menu-label = { $property } ({ $owner })
monopoly-deed-menu-label-extra = { $property } ({ $owner }; { $extras })
monopoly-color-brown = Nâu
monopoly-color-light_blue = Xanh nhạt
monopoly-color-pink = Hồng
monopoly-color-orange = Cam
monopoly-color-red = Đỏ
monopoly-color-yellow = Vàng
monopoly-color-green = Xanh lá
monopoly-color-dark_blue = Xanh đậm
monopoly-deed-type-color-group = Loại: nhóm màu { $color }
monopoly-deed-type-railroad = Loại: đường sắt
monopoly-deed-type-utility = Loại: tiện ích
monopoly-deed-type-generic = Loại: { $kind }
monopoly-deed-purchase-price = Giá mua: { $amount }
monopoly-deed-rent = Tiền thuê: { $amount }
monopoly-deed-full-set-rent = Nếu chủ sở hữu có đủ bộ màu: { $amount }
monopoly-deed-rent-one-house = Với 1 nhà: { $amount }
monopoly-deed-rent-houses = Với { $count } nhà: { $amount }
monopoly-deed-rent-hotel = Với khách sạn: { $amount }
monopoly-deed-house-cost = Giá nhà: { $amount }
monopoly-deed-railroad-rent = Tiền thuê với { $count } đường sắt: { $amount }
monopoly-deed-utility-one-owned = Nếu sở hữu một công ty tiện ích: 4x tổng xúc xắc
monopoly-deed-utility-both-owned = Nếu sở hữu cả hai công ty tiện ích: 10x tổng xúc xắc
monopoly-deed-utility-base-rent = Tiền thuê cơ bản của tiện ích (kiểu cũ): { $amount }
monopoly-deed-mortgage-value = Giá trị thế chấp: { $amount }
monopoly-deed-unmortgage-cost = Chi phí chuộc thế chấp: { $amount }
monopoly-deed-owner = Chủ sở hữu: { $owner }
monopoly-deed-current-buildings = Công trình hiện tại: { $buildings }
monopoly-deed-status-mortgaged = Trạng thái: đang thế chấp
monopoly-player-properties-label = { $player }, ở { $space }, ô số { $position }
monopoly-player-properties-label-no-space = { $player }, ô số { $position }
monopoly-banking-ledger-entry-success = { $tx_id } { $kind } { $from_id }->{ $to_id } { $amount } ({ $reason })
monopoly-banking-ledger-entry-failed = { $tx_id } { $kind } thất bại ({ $reason })

# Trade menu summaries
monopoly-trade-buy-property-summary = Mua { $property } từ { $target } với giá { $amount }
monopoly-trade-offer-cash-for-property-summary = Đề nghị { $amount } cho { $target } để lấy { $property }
monopoly-trade-sell-property-summary = Bán { $property } cho { $target } với giá { $amount }
monopoly-trade-offer-property-for-cash-summary = Đề nghị { $property } cho { $target } với giá { $amount }
monopoly-trade-swap-summary = Đổi { $give_property } với { $target } lấy { $receive_property }
monopoly-trade-swap-plus-cash-summary = Đổi { $give_property } + { $amount } với { $target } lấy { $receive_property }
monopoly-trade-swap-receive-cash-summary = Đổi { $give_property } lấy { $receive_property } + { $amount } từ { $target }
monopoly-trade-buy-jail-card-summary = Mua thẻ ra tù từ { $target } với giá { $amount }
monopoly-trade-sell-jail-card-summary = Bán thẻ ra tù cho { $target } với giá { $amount }

# Board space names
monopoly-space-go = GO
monopoly-space-mediterranean_avenue = Mediterranean Avenue
monopoly-space-community_chest_1 = Quỹ cộng đồng
monopoly-space-baltic_avenue = Baltic Avenue
monopoly-space-income_tax = Thuế thu nhập
monopoly-space-reading_railroad = Reading Railroad
monopoly-space-oriental_avenue = Oriental Avenue
monopoly-space-chance_1 = Cơ hội
monopoly-space-vermont_avenue = Vermont Avenue
monopoly-space-connecticut_avenue = Connecticut Avenue
monopoly-space-jail = Tù / Chỉ ghé thăm
monopoly-space-st_charles_place = St. Charles Place
monopoly-space-electric_company = Công ty điện
monopoly-space-states_avenue = States Avenue
monopoly-space-virginia_avenue = Virginia Avenue
monopoly-space-pennsylvania_railroad = Pennsylvania Railroad
monopoly-space-st_james_place = St. James Place
monopoly-space-community_chest_2 = Quỹ cộng đồng
monopoly-space-tennessee_avenue = Tennessee Avenue
monopoly-space-new_york_avenue = New York Avenue
monopoly-space-free_parking = Bãi đỗ xe miễn phí
monopoly-space-kentucky_avenue = Kentucky Avenue
monopoly-space-chance_2 = Cơ hội
monopoly-space-indiana_avenue = Indiana Avenue
monopoly-space-illinois_avenue = Illinois Avenue
monopoly-space-bo_railroad = B. & O. Railroad
monopoly-space-atlantic_avenue = Atlantic Avenue
monopoly-space-ventnor_avenue = Ventnor Avenue
monopoly-space-water_works = Công ty nước
monopoly-space-marvin_gardens = Marvin Gardens
monopoly-space-go_to_jail = Đi vào tù
monopoly-space-pacific_avenue = Pacific Avenue
monopoly-space-north_carolina_avenue = North Carolina Avenue
monopoly-space-community_chest_3 = Quỹ cộng đồng
monopoly-space-pennsylvania_avenue = Pennsylvania Avenue
monopoly-space-short_line = Short Line
monopoly-space-chance_3 = Cơ hội
monopoly-space-park_place = Park Place
monopoly-space-luxury_tax = Thuế xa xỉ
monopoly-space-boardwalk = Boardwalk
