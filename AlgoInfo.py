from State     import State
from ShareStat import Price

class AlgoInfo:
    def __init__(self):
        self.axisDT       = []
        self.fnPrice      = []
        self.fnCount      = []
        self.fnCash       = []
        self.fnVolatility = []
        self.fnSoldPrice  = []
        self.fnCapital    = []

    def append(self, date, priceKit, state, volatility):
        price = priceKit.get(Price.OPEN)
        self.axisDT.append(date)
        self.fnPrice.append(price)
        self.fnCount.append(state.shareQty)
        self.fnCash.append(state.cash)
        self.fnVolatility.append(volatility)
        self.fnSoldPrice.append(state.exitPrice)
        self.fnCapital.append(state.cash + price * state.shareQty)
