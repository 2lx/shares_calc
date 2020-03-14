from AlgoInfo  import AlgoInfo
from ShareStat import ShareStat, Price
from State     import State

from datetime  import datetime, timedelta

class SimpleAlgo:
    def __init__(self, shareStat):
        self.stat = shareStat
        self.info = AlgoInfo()

    def process(self, startDate, endDate, cash):
        date  = startDate
        state = State(cash)

        while date < endDate:
            priceKit  = self.stat.getPrices(date)

            if priceKit is not None:
                volatility15             = self.stat.getVolatilityDays(date, 15)
                ytdMinPrice, ytdMaxPrice = self.stat.getMinMaxPriceDays(date, 1)
                sysMinPrice, sysMaxPrice = self.stat.getMinMaxPriceDays(date, 14)

                if ytdMaxPrice == sysMaxPrice:
                    if state.shareQty == 0:
                        state.buy(priceKit, volatility15)

                    elif state.shareQty > 0:
                        state.updateExitPrice(priceKit, volatility15)

                if state.shareQty > 0 and priceKit.get(Price.LOW) <= state.exitPrice:
                    state.sell(priceKit)

                self.info.append(date, priceKit, state, volatility15)

            date += timedelta(minutes=15)

        return self.info

