from State     import State
from ShareStat import Price

class AlgoInfo:
    def __init__(self):
        self.axisDT       = []
        self.fnLowPrice   = []
        self.fnHighPrice  = []
        self.fnCount      = []
        self.fnCash       = []
        self.fnVolatility = []
        self.fnSoldPrice  = []
        self.fnCapital    = []

        self.axisBuyPrice = []
        self.axisSellSucc = []
        self.axisSellFail = []
        self.fnBuyPrice   = []
        self.fnSellSucc   = []
        self.fnSellFail   = []

    def append(self, date, priceKit, state, volatility):
        lowPrice  = priceKit.get(Price.LOW)
        highPrice = priceKit.get(Price.HIGH)

        self.axisDT.append(date)
        self.fnLowPrice.append(lowPrice)
        self.fnHighPrice.append(highPrice)
        self.fnCount.append(state.shareQty)
        self.fnCash.append(state.cash)
        self.fnVolatility.append(volatility)
        self.fnSoldPrice.append(state.exitPrice)
        self.fnCapital.append(state.cash + (highPrice + lowPrice) * state.shareQty / 2.0)
        if state.buyResult != 0:
            self.fnBuyPrice.append(state.buyPrice)
            self.axisBuyPrice.append(date)
            state.buyResult = 0

        if state.sellResult != 0:
            if state.sellResult > 0:
                self.fnSellSucc.append(state.sellPrice)
                self.axisSellSucc.append(date)
            else:
                self.fnSellFail.append(state.sellPrice)
                self.axisSellFail.append(date)
            state.sellResult = 0

