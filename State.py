from ShareStat import Price

class State:
    def __init__(self, cash):
        self.exitPrice   = 0
        self.shareQty = 0
        self.boughtPrice = 0
        self.cash        = cash

    def buy(self, priceKit, volat):
        price            = priceKit.get(Price.OPEN)
        self.boughtPrice = price
        self.exitPrice   = price - 2 * volat
        self.shareQty    = self.cash // price
        self.cash        = self.cash - price * self.shareQty * 1.0005
        #  print("Buy : at {0} price {1:0>5.2f}$ X {2:0>4n}"
        #      .format(date, price, self.shareQty))

    def updateExitPrice(self, priceKit, volat):
        highPrice      = priceKit.get(Price.HIGH)
        self.exitPrice = max(highPrice - 2 * volat, self.exitPrice)

    def sell(self, priceKit):
        highPrice      = priceKit.get(Price.HIGH)
        self.cash      = self.cash + min(self.exitPrice, highPrice) * self.shareQty * 0.9995
        self.shareQty  = 0
        self.exitPrice = 0
        #  success     = "+" if lowPrice > state.boughtPrice else ""
        #  print("Sell: at {0} price {1:0>5.2f}$, cash {3:0>8.2f} {4}"
        #          .format(date, openPrice cash, success))
