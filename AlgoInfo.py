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
