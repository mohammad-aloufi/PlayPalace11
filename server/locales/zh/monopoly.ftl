# Monopoly game messages

# Game info
game-name-monopoly = Monopoly

# Lobby options
monopoly-set-preset = 模式：{ $preset }
monopoly-select-preset = 选择 Monopoly 模式
monopoly-option-changed-preset = 模式已设为 { $preset }。

# Preset labels
monopoly-preset-classic-standard = 经典与主题标准模式
monopoly-preset-junior = Monopoly Junior
monopoly-preset-junior-modern = Monopoly Junior（现代）
monopoly-preset-junior-legacy = Monopoly Junior（传统）
monopoly-preset-cheaters = Monopoly 作弊者版
monopoly-preset-electronic-banking = 电子银行
monopoly-preset-voice-banking = 语音银行
monopoly-preset-sore-losers = Monopoly 输不起版
monopoly-preset-speed = Monopoly Speed
monopoly-preset-builder = Monopoly Builder
monopoly-preset-city = Monopoly City
monopoly-preset-bid-card-game = Monopoly Bid
monopoly-preset-deal-card-game = Monopoly Deal
monopoly-preset-knockout = Monopoly Knockout
monopoly-preset-free-parking-jackpot = 免费停车大奖池

# Scaffold status
monopoly-announce-preset = 报读当前模式
monopoly-current-preset = 当前模式：{ $preset }（{ $count } 个版本）。
monopoly-scaffold-started = Monopoly 已以 { $preset } 启动（{ $count } 个版本）。

# Turn actions
monopoly-roll-dice = 掷骰子
monopoly-buy-property = 购买地产
monopoly-banking-balance = 查询银行余额
monopoly-banking-transfer = 转账
monopoly-banking-ledger = 查看银行记录
monopoly-voice-command = 语音命令
monopoly-cheaters-claim-reward = 领取作弊奖励
monopoly-end-turn = 结束回合

# Turn validation
monopoly-roll-first = 你需要先掷骰子。
monopoly-already-rolled = 你本回合已经掷过骰子了。
monopoly-no-property-to-buy = 现在没有可购买的地产。
monopoly-property-owned = 该地产已经有主人了。
monopoly-not-enough-cash = 你的现金不足。
monopoly-action-disabled-for-preset = 此操作在所选模式下被禁用。
monopoly-buy-disabled = 该模式下禁止直接购买地产。

# Turn events
monopoly-pass-go = { $player } 经过 GO 并获得了 { $amount }（现金：{ $cash }）。
monopoly-roll-result = { $player } 掷出 { $die1 } + { $die2 } = { $total }，落在 { $space }。
monopoly-roll-only = { $player } 掷出 { $die1 } + { $die2 } = { $total }。
monopoly-you-roll-result = 你掷出 { $die1 } + { $die2 } = { $total }，落在 { $space }。
monopoly-player-roll-result = { $player } 掷出 { $die1 } + { $die2 } = { $total }，落在 { $space }。
monopoly-you-roll-only = 你掷出 { $die1 } + { $die2 } = { $total }。
monopoly-player-roll-only = { $player } 掷出 { $die1 } + { $die2 } = { $total }。
monopoly-you-roll-only-doubles = 你掷出 { $die1 } + { $die2 } = { $total }。双骰！
monopoly-player-roll-only-doubles = { $player } 掷出 { $die1 } + { $die2 } = { $total }。双骰！
monopoly-property-available = { $property } 可用，价格为 { $price }。
monopoly-property-bought = { $player } 以 { $price } 买下了 { $property }（现金：{ $cash }）。
monopoly-rent-paid = { $player } 为 { $property } 向 { $owner } 支付了 { $amount } 租金。
monopoly-player-paid-player = { $player } 向 { $target } 支付了 { $amount }。
monopoly-landed-owned = { $player } 落在自己的地产上：{ $property }。
monopoly-tax-paid = { $player } 为 { $tax } 支付了 { $amount }（现金：{ $cash }）。
monopoly-go-to-jail = { $player } 进监狱了（已移动到 { $space }）。
monopoly-bankrupt-player = 你已破产并退出游戏。
monopoly-player-bankrupt = { $player } 已破产。债权人：{ $creditor }。
monopoly-winner-by-bankruptcy = { $player } 以破产获胜，剩余现金 { $cash }。
monopoly-winner-by-cash = { $player } 以最高现金总额获胜：{ $cash }。
monopoly-city-winner-by-value = { $player } 以最终价值 { $total } 赢得 Monopoly City。

# Additional actions
monopoly-auction-property = 拍卖地产
monopoly-auction-bid = 参与竞拍
monopoly-auction-pass = 拍卖中跳过
monopoly-mortgage-property = 抵押地产
monopoly-unmortgage-property = 解除抵押
monopoly-build-house = 建造房屋或旅馆
monopoly-sell-house = 卖出房屋或旅馆
monopoly-offer-trade = 发起交易
monopoly-accept-trade = 接受交易
monopoly-decline-trade = 拒绝交易
monopoly-read-cash = 读出现金
monopoly-pay-bail = 支付保释金
monopoly-use-jail-card = 使用出狱卡
monopoly-cash-report = 现金：{ $cash }。
monopoly-property-amount-option = { $property }，价格 { $amount }
monopoly-banking-transfer-option = 向 { $target } 转账 { $amount }

# Additional prompts
monopoly-select-property-mortgage = 选择要抵押的地产
monopoly-select-property-unmortgage = 选择要解除抵押的地产
monopoly-select-property-build = 选择要建造的地产
monopoly-select-property-sell = 选择要卖出建筑的地产
monopoly-select-trade-offer = 选择一项交易提议
monopoly-select-auction-bid = 选择你的拍卖报价
monopoly-select-banking-transfer = 选择一笔转账
monopoly-select-voice-command = 输入以 voice: 开头的语音命令：

# Additional validation
monopoly-no-property-to-auction = 现在没有可拍卖的地产。
monopoly-auction-active = 请先处理当前拍卖。
monopoly-no-auction-active = 当前没有拍卖进行中。
monopoly-not-your-auction-turn = 现在不是你在拍卖中的回合。
monopoly-no-mortgage-options = 你没有可抵押的地产。
monopoly-no-unmortgage-options = 你没有可解除抵押的地产。
monopoly-no-build-options = 你没有可建造的地产。
monopoly-no-sell-options = 你没有可卖出建筑的地产。
monopoly-no-trade-options = 你现在没有可用的交易方案。
monopoly-no-trade-pending = 当前没有等待你处理的交易。
monopoly-trade-pending = 已有交易正在等待处理。
monopoly-trade-no-longer-valid = 该交易已失效。
monopoly-not-in-jail = 你不在监狱中。
monopoly-no-jail-card = 你没有出狱卡。
monopoly-roll-again-required = 你掷出了双骰，必须再掷一次。
monopoly-resolve-property-first = 请先处理待决的地产决定。

# Additional turn events
monopoly-roll-again = { $player } 掷出了双骰，可以再掷一次。
monopoly-you-roll-again = 你掷出了双骰，可以再掷一次。
monopoly-player-roll-again = { $player } 掷出了双骰，可以再掷一次。
monopoly-jail-roll-doubles = { $player } 在监狱中掷出双骰（{ $die1 } 和 { $die2 }），离开监狱。
monopoly-you-jail-roll-doubles = 你在监狱中掷出双骰（{ $die1 } 和 { $die2 }），离开监狱。
monopoly-player-jail-roll-doubles = { $player } 在监狱中掷出双骰（{ $die1 } 和 { $die2 }），离开监狱。
monopoly-jail-roll-failed = { $player } 在监狱中掷出 { $die1 } 和 { $die2 }（第 { $attempts } 次）。
monopoly-bail-paid = { $player } 支付了 { $amount } 保释金（现金：{ $cash }）。
monopoly-three-doubles-jail = { $player } 在同一回合掷出三次双骰，被送进监狱。
monopoly-you-three-doubles-jail = 你在同一回合掷出三次双骰，被送进监狱。
monopoly-player-three-doubles-jail = { $player } 在同一回合掷出三次双骰，被送进监狱。
monopoly-jail-card-used = { $player } 使用了一张出狱卡（剩余 { $cards } 张）。
monopoly-sore-loser-rebate = { $player } 获得了 { $amount } 的输不起补贴（现金：{ $cash }）。
monopoly-cheaters-early-end-turn-blocked = { $player } 试图过早结束回合，并支付了 { $amount } 的作弊罚金（现金：{ $cash }）。
monopoly-cheaters-payment-avoidance-blocked = { $player } 触发了 { $amount } 的逃避付款作弊罚金（现金：{ $cash }）。
monopoly-cheaters-reward-granted = { $player } 领取了 { $amount } 的作弊奖励（现金：{ $cash }）。
monopoly-cheaters-reward-unavailable = { $player } 本回合已经领取过作弊奖励。

# Auctions and mortgages
monopoly-auction-no-bids = { $property } 没有竞价，仍未售出。
monopoly-auction-started = { $property } 的拍卖已开始（起拍价：{ $amount }）。
monopoly-auction-turn = 拍卖回合：轮到 { $player } 对 { $property } 操作（当前报价：{ $amount }）。
monopoly-auction-bid-placed = { $player } 为 { $property } 出价 { $amount }。
monopoly-auction-pass-event = { $player } 放弃了 { $property } 的竞拍。
monopoly-auction-won = { $player } 以 { $amount } 赢得了 { $property } 的拍卖（现金：{ $cash }）。
monopoly-property-mortgaged = { $player } 以 { $amount } 抵押了 { $property }（现金：{ $cash }）。
monopoly-property-unmortgaged = { $player } 以 { $amount } 解除了 { $property } 的抵押（现金：{ $cash }）。
monopoly-house-built = { $player } 在 { $property } 上建造，花费 { $amount }（等级：{ $level }，现金：{ $cash }）。
monopoly-house-sold = { $player } 卖出了 { $property } 上的一处建筑，获得 { $amount }（等级：{ $level }，现金：{ $cash }）。
monopoly-trade-offered = { $proposer } 向 { $target } 提出交易：{ $offer }。
monopoly-trade-completed = { $proposer } 与 { $target } 的交易已完成：{ $offer }。
monopoly-trade-declined = { $target } 拒绝了来自 { $proposer } 的交易：{ $offer }。
monopoly-trade-cancelled = 交易已取消：{ $offer }。
monopoly-free-parking-jackpot = { $player } 获得了免费停车大奖池 { $amount }（现金：{ $cash }）。
monopoly-mortgaged-no-rent = { $player } 落在已抵押的 { $property } 上；无需支付租金。
monopoly-builder-blocks-awarded = { $player } 获得了 { $amount } 个建造方块（共 { $blocks } 个）。
monopoly-builder-block-spent = { $player } 使用了一个建造方块（剩余 { $blocks } 个）。
monopoly-banking-transfer-success = { $from_player } 向 { $to_player } 转账了 { $amount }。
monopoly-banking-transfer-failed = { $player } 的银行转账失败（{ $reason }）。
monopoly-banking-balance-report = { $player } 的银行余额：{ $cash }。
monopoly-banking-ledger-report = 最近的银行活动：{ $entries }。
monopoly-banking-ledger-empty = 目前还没有银行交易。
monopoly-voice-command-error = 语音命令错误：{ $reason }。
monopoly-voice-command-accepted = 语音命令已接受：{ $intent }。
monopoly-voice-command-repeat = 重复上一条银行回应代码：{ $response }。
monopoly-voice-transfer-staged = 已准备语音转账：向 { $target } 转 { $amount }。请说 voice: confirm transfer。
monopoly-mortgage-transfer-interest-paid = { $player } 支付了 { $amount } 的抵押转移利息（现金：{ $cash }）。

# Card engine
monopoly-card-drawn = { $player } 抽到一张 { $deck } 卡：{ $card }。
monopoly-card-collect = { $player } 收到 { $amount }（现金：{ $cash }）。
monopoly-card-pay = { $player } 支付了 { $amount }（现金：{ $cash }）。
monopoly-card-move = { $player } 被移动到 { $space }。
monopoly-card-jail-free = { $player } 获得了一张出狱卡（共 { $cards } 张）。
monopoly-card-utility-roll = { $player } 为公用事业租金掷出 { $die1 } + { $die2 } = { $total }。
monopoly-deck-chance = 机会
monopoly-deck-community-chest = 公益金

# Card descriptions
monopoly-card-advance-to-go = 前进到 GO 并领取 { $amount }
monopoly-card-advance-to-illinois-avenue = 前进到 Illinois Avenue
monopoly-card-advance-to-st-charles-place = 前进到 St. Charles Place
monopoly-card-advance-to-nearest-utility = 前进到最近的公用事业公司
monopoly-card-advance-to-nearest-railroad = 前进到最近的铁路；如果已被拥有则支付双倍租金
monopoly-card-bank-dividend-50 = 银行向你支付 { $amount } 的红利
monopoly-card-go-back-three = 后退 3 格
monopoly-card-go-to-jail = 直接进入监狱
monopoly-card-general-repairs = 对你所有地产进行大修：每栋房屋 { $per_house }，每间旅馆 { $per_hotel }
monopoly-card-poor-tax-15 = 支付 { $amount } 的税
monopoly-card-reading-railroad = 前往 Reading Railroad
monopoly-card-boardwalk = 漫步到 Boardwalk
monopoly-card-chairman-of-the-board = 董事长，向每位玩家支付 { $amount }
monopoly-card-building-loan-matures = 你的建筑贷款到期，领取 { $amount }
monopoly-card-crossword-competition = 你赢得了填字比赛，领取 { $amount }
monopoly-card-bank-error-200 = 银行出错对你有利，领取 { $amount }
monopoly-card-doctor-fee-50 = 医疗费，支付 { $amount }
monopoly-card-sale-of-stock-50 = 卖出股票获利 { $amount }
monopoly-card-holiday-fund = 假日基金到期，领取 { $amount }
monopoly-card-tax-refund-20 = 所得税退税，领取 { $amount }
monopoly-card-birthday = 今天是你的生日，向每位玩家收取 { $amount }
monopoly-card-life-insurance = 人寿保险到期，领取 { $amount }
monopoly-card-hospital-fees-100 = 支付 { $amount } 的住院费
monopoly-card-school-fees-50 = 支付 { $amount } 的学费
monopoly-card-consultancy-fee-25 = 收取 { $amount } 的咨询费
monopoly-card-street-repairs = 街道维修费：每栋房屋 { $per_house }，每间旅馆 { $per_hotel }
monopoly-card-beauty-contest-10 = 你在选美比赛中获得第二名，领取 { $amount }
monopoly-card-inherit-100 = 你继承了 { $amount }
monopoly-card-get-out-of-jail = 免费出狱

# Board profile options
monopoly-set-board = 棋盘：{ $board }
monopoly-select-board = 选择 Monopoly 棋盘
monopoly-option-changed-board = 棋盘已设为 { $board }。
monopoly-set-board-rules-mode = 棋盘规则模式：{ $mode }
monopoly-select-board-rules-mode = 选择棋盘规则模式
monopoly-option-changed-board-rules-mode = 棋盘规则模式已设为 { $mode }。

# Board labels
monopoly-board-classic-default = 经典默认棋盘
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
monopoly-board-rules-mode-auto = 自动
monopoly-board-rules-mode-skin-only = 仅外观

# Board runtime announcements
monopoly-board-preset-autofixed = 棋盘 { $board } 与 { $from_preset } 不兼容；已切换到 { $to_preset }。
monopoly-board-rules-simplified = 棋盘 { $board } 的规则只实现了一部分；缺失机制将使用基础模式行为。
monopoly-board-active = 当前棋盘：{ $board }（模式：{ $mode }）。

# Deed and ownership browsing
monopoly-view-active-deed = 查看当前地契
monopoly-view-active-deed-space = 查看 { $property }
monopoly-browse-all-deeds = 浏览全部地契
monopoly-view-my-properties = 查看我的地产
monopoly-view-player-properties = 查看玩家信息
monopoly-view-selected-deed = 查看所选地契
monopoly-view-selected-owner-property-deed = 查看所选玩家地契
monopoly-select-property-deed = 选择地产地契
monopoly-select-player-properties = 选择玩家
monopoly-select-player-property-deed = 选择玩家地产地契
monopoly-no-active-deed = 当前没有可查看的活动地契。
monopoly-no-deeds-available = 该棋盘上没有可查看地契的地产。
monopoly-no-owned-properties = 此视图中没有已拥有地产。
monopoly-no-players-with-properties = 没有可用的玩家。
monopoly-buy-for = 购买价 { $amount }
monopoly-you-have-no-owned-properties = 你没有任何地产。
monopoly-player-has-no-owned-properties = { $player } 没有任何地产。
monopoly-owner-bank = 银行
monopoly-owner-unknown = 未知
monopoly-building-status-hotel = 有旅馆
monopoly-building-status-one-house = 有 1 栋房屋
monopoly-building-status-houses = 有 { $count } 栋房屋
monopoly-mortgaged-short = 已抵押
monopoly-deed-menu-label = { $property }（{ $owner }）
monopoly-deed-menu-label-extra = { $property }（{ $owner }；{ $extras }）
monopoly-color-brown = 棕色
monopoly-color-light_blue = 浅蓝色
monopoly-color-pink = 粉色
monopoly-color-orange = 橙色
monopoly-color-red = 红色
monopoly-color-yellow = 黄色
monopoly-color-green = 绿色
monopoly-color-dark_blue = 深蓝色
monopoly-deed-type-color-group = 类型：{ $color } 色组
monopoly-deed-type-railroad = 类型：铁路
monopoly-deed-type-utility = 类型：公用事业
monopoly-deed-type-generic = 类型：{ $kind }
monopoly-deed-purchase-price = 购买价格：{ $amount }
monopoly-deed-rent = 租金：{ $amount }
monopoly-deed-full-set-rent = 如果拥有完整色组：{ $amount }
monopoly-deed-rent-one-house = 1 栋房屋时：{ $amount }
monopoly-deed-rent-houses = { $count } 栋房屋时：{ $amount }
monopoly-deed-rent-hotel = 旅馆时：{ $amount }
monopoly-deed-house-cost = 房屋价格：{ $amount }
monopoly-deed-railroad-rent = 拥有 { $count } 条铁路时租金：{ $amount }
monopoly-deed-utility-one-owned = 拥有一个公用事业时：骰子点数 x4
monopoly-deed-utility-both-owned = 拥有两个公用事业时：骰子点数 x10
monopoly-deed-utility-base-rent = 公用事业基础租金（旧规则）：{ $amount }
monopoly-deed-mortgage-value = 抵押价值：{ $amount }
monopoly-deed-unmortgage-cost = 解除抵押费用：{ $amount }
monopoly-deed-owner = 所有者：{ $owner }
monopoly-deed-current-buildings = 当前建筑：{ $buildings }
monopoly-deed-status-mortgaged = 状态：已抵押
monopoly-player-properties-label = { $player }，位于 { $space }，格子 { $position }
monopoly-player-properties-label-no-space = { $player }，格子 { $position }
monopoly-banking-ledger-entry-success = { $tx_id } { $kind } { $from_id }->{ $to_id } { $amount }（{ $reason }）
monopoly-banking-ledger-entry-failed = { $tx_id } { $kind } 失败（{ $reason }）

# Trade menu summaries
monopoly-trade-buy-property-summary = 以 { $amount } 从 { $target } 购买 { $property }
monopoly-trade-offer-cash-for-property-summary = 向 { $target } 出价 { $amount } 购买 { $property }
monopoly-trade-sell-property-summary = 以 { $amount } 向 { $target } 出售 { $property }
monopoly-trade-offer-property-for-cash-summary = 向 { $target } 提供 { $property }，价格 { $amount }
monopoly-trade-swap-summary = 用 { $give_property } 与 { $target } 交换 { $receive_property }
monopoly-trade-swap-plus-cash-summary = 用 { $give_property } 加 { $amount } 与 { $target } 交换 { $receive_property }
monopoly-trade-swap-receive-cash-summary = 用 { $give_property } 交换 { $receive_property }，并从 { $target } 获得 { $amount }
monopoly-trade-buy-jail-card-summary = 以 { $amount } 从 { $target } 购买出狱卡
monopoly-trade-sell-jail-card-summary = 以 { $amount } 向 { $target } 出售出狱卡

# Board space names
monopoly-space-go = GO
monopoly-space-mediterranean_avenue = Mediterranean Avenue
monopoly-space-community_chest_1 = 公益金
monopoly-space-baltic_avenue = Baltic Avenue
monopoly-space-income_tax = 所得税
monopoly-space-reading_railroad = Reading Railroad
monopoly-space-oriental_avenue = Oriental Avenue
monopoly-space-chance_1 = 机会
monopoly-space-vermont_avenue = Vermont Avenue
monopoly-space-connecticut_avenue = Connecticut Avenue
monopoly-space-jail = 监狱 / 探监
monopoly-space-st_charles_place = St. Charles Place
monopoly-space-electric_company = 电力公司
monopoly-space-states_avenue = States Avenue
monopoly-space-virginia_avenue = Virginia Avenue
monopoly-space-pennsylvania_railroad = Pennsylvania Railroad
monopoly-space-st_james_place = St. James Place
monopoly-space-community_chest_2 = 公益金
monopoly-space-tennessee_avenue = Tennessee Avenue
monopoly-space-new_york_avenue = New York Avenue
monopoly-space-free_parking = 免费停车
monopoly-space-kentucky_avenue = Kentucky Avenue
monopoly-space-chance_2 = 机会
monopoly-space-indiana_avenue = Indiana Avenue
monopoly-space-illinois_avenue = Illinois Avenue
monopoly-space-bo_railroad = B. & O. Railroad
monopoly-space-atlantic_avenue = Atlantic Avenue
monopoly-space-ventnor_avenue = Ventnor Avenue
monopoly-space-water_works = 自来水厂
monopoly-space-marvin_gardens = Marvin Gardens
monopoly-space-go_to_jail = 进监狱
monopoly-space-pacific_avenue = Pacific Avenue
monopoly-space-north_carolina_avenue = North Carolina Avenue
monopoly-space-community_chest_3 = 公益金
monopoly-space-pennsylvania_avenue = Pennsylvania Avenue
monopoly-space-short_line = Short Line
monopoly-space-chance_3 = 机会
monopoly-space-park_place = Park Place
monopoly-space-luxury_tax = 奢侈税
monopoly-space-boardwalk = Boardwalk
