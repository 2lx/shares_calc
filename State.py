from ShareStat import Price

class State:
    def __init__(self, cash, vltCoeff):
        self.exitPrice   = 0
        self.shareQty    = 0
        self.cash        = cash
        self.vltCoeff    = vltCoeff
        self.commission  = 0.00075
        self.buyPrice    = 0
        self.buyDate     = None
        self.buyResult   = 0
        self.sellPrice   = 0
        self.sellResult  = 0

    def buy(self, date, priceKit, countPercent):
        price            = (priceKit.get(Price.HIGH) + priceKit.get(Price.LOW)) / 2
        shareQty         = self.cash * countPercent // price
        if shareQty > 0:
            self.buyPrice    = price
            self.buyDate     = date
            self.cash        = self.cash - price * shareQty * (1 + self.commission)
            self.shareQty   += shareQty
            self.buyResult   = 1
        #  print("Buy : at {0} price {1:0>5.2f}$ X {2:0>4n}"
        #      .format(date, price, self.shareQty))

    def updateExitPrice(self, priceKit, volat):
        highPrice      = priceKit.get(Price.HIGH)
        self.exitPrice = max(highPrice - self.vltCoeff * volat, self.exitPrice)

    def sell(self, date, priceKit):
        highPrice      = priceKit.get(Price.HIGH)
        sellPrice      = min(self.exitPrice, highPrice)

        self.cash       = self.cash + sellPrice * self.shareQty * (1 - self.commission)
        self.shareQty   = 0
        self.exitPrice  = 0
        self.sellResult = 1 if sellPrice > self.buyPrice else -1
        self.sellPrice  = sellPrice

        #  success     = "+" if sellPrice > self.buyPrice else ""
        #  print("Sell: at {0} price {1:0>5.2f}$, cash {2:0>8.2f} {3}"
        #          .format(date, sellPrice, self.cash, success))
