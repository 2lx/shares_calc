from State     import State
from ShareStat import Price

class AlgoInfo:
    def __init__(self):
        self.axisGlobal   = []
        self.fnMarketClose = []

        self.axisDT       = []
        self.fnLowPrice   = []
        self.fnHighPrice  = []
        self.fnCount      = []
        self.fnCash       = []
        self.fnSoldPrice  = []
        self.fnCapital    = []

        self.axisBuyPrice = []
        self.axisSellSucc = []
        self.axisSellFail = []
        self.fnBuyPrice   = []
        self.fnSellSucc   = []
        self.fnSellFail   = []
        self.fnVol15Days  = []
        self.fnVol60MinP  = []

    def appendGlobal(self, date, marketOpen):
        self.axisGlobal.append(date)
        self.fnMarketClose.append(not marketOpen)

    def append(self, date, priceKit, state, volatility, vol60Perc):
        lowPrice  = priceKit.get(Price.LOW)
        highPrice = priceKit.get(Price.HIGH)

        self.axisDT.append(date)
        self.fnLowPrice.append(lowPrice)
        self.fnHighPrice.append(highPrice)
        self.fnCount.append(state.shareQty)
        self.fnCash.append(state.cash)
        self.fnVol15Days.append(volatility)
        self.fnVol60MinP.append(vol60Perc * 100.0)
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

