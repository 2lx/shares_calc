from AlgoInfo  import AlgoInfo
from ShareStat import ShareStat, Price
from State     import State

from datetime  import datetime, timedelta

class Algo2:
    def __init__(self, shareStat):
        self.stat = shareStat
        self.info = AlgoInfo()

    def process(self, startDate, endDate, cash):
        date     = startDate
        state    = State(cash, 2.5)
        lastSell = date - timedelta(days=1000)

        while date < endDate:
            priceKit = self.stat.getPrices(date)

            if priceKit is not None:
                volatility15 = self.stat.getVolatilityDays(date, 15)

                if state.shareQty == 0: #and (date - lastSell).seconds >= 15 * 60:
                    minPrice1, maxPrice1   = self.stat.getMinMaxPriceDays(date, 1)
                    minPrice14, maxPrice14 = self.stat.getMinMaxPriceDays(date, 14)

                    if self.stat.priceRiseInRow(date, 1, 7) and minPrice1 != minPrice14:
                        state.buy(date, priceKit, volatility15)
                elif priceKit.get(Price.LOW) <= state.exitPrice:
                    state.sell(date, priceKit)
                    lastSell = date

                if state.shareQty > 0:
                    state.updateExitPrice(priceKit, volatility15)

                self.info.append(date, priceKit, state, volatility15)

            date += timedelta(minutes=15)

        return self.info

