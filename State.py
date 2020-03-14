from ShareStat import Price

class State:
    def __init__(self, cash, vltCoeff):
        self.exitPrice   = 0
        self.shareQty    = 0
        self.boughtPrice = 0
        self.cash        = cash
        self.vltCoeff    = vltCoeff
        self.commission  = 0.00075

    def buy(self, date, priceKit, volat):
        price            = (priceKit.get(Price.HIGH) + priceKit.get(Price.LOW)) / 2
        self.boughtPrice = price
        self.exitPrice   = price - self.vltCoeff * volat
        self.shareQty    = self.cash // price
        self.cash        = self.cash - price * self.shareQty * (1 + self.commission)
        print("Buy : at {0} price {1:0>5.2f}$ X {2:0>4n}"
            .format(date, price, self.shareQty))

    def updateExitPrice(self, priceKit, volat):
        highPrice      = priceKit.get(Price.HIGH)
        self.exitPrice = max(highPrice - self.vltCoeff * volat, self.exitPrice)

    def sell(self, date, priceKit):
        highPrice      = priceKit.get(Price.HIGH)
        sellPrice      = min(self.exitPrice, highPrice)

        self.cash      = self.cash + sellPrice * self.shareQty * (1 - self.commission)
        self.shareQty  = 0
        self.exitPrice = 0

        success     = "+" if sellPrice > self.boughtPrice else ""
        print("Sell: at {0} price {1:0>5.2f}$, cash {2:0>8.2f} {3}"
                .format(date, sellPrice, self.cash, success))
