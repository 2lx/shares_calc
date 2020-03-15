from AlgoInfo  import AlgoInfo
from ShareStat import *
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
                    #  minPrice1,  maxPrice1  = self.stat.getMinMaxPriceDays(date, 1)
                    #  minPrice14, maxPrice14 = self.stat.getMinMaxPriceDays(date, 14)
                    #  if self.stat.getPeriodExtremum(date, 7 * 24 * 60) == Extremum.MAXIMUM and \
                    #  if self.stat.priceRiseInRow(date, 2, 7) and minPrice1 != minPrice14:
                    #  tends14days = self.stat.tendenciesInRow(date, 14 * 24 * 60)
                    tends7days = self.stat.tendenciesInRow(date, 7 * 24 * 60)
                    tends2days = self.stat.tendenciesInRow(date, 2 * 24 * 60)

                    #  if tends7days[Tendency.MINFALL] == 0 and \
                    if (tends2days[Tendency.MAXRISE] >= 3 or tends7days[Tendency.MAXRISE] >= 2):
                        state.buy(date, priceKit, volatility15)
                elif priceKit.get(Price.LOW) <= state.exitPrice:
                    state.sell(date, priceKit)
                    lastSell = date

                if state.shareQty > 0:
                    state.updateExitPrice(priceKit, volatility15)

                self.info.append(date, priceKit, state, volatility15)

            date += timedelta(minutes=15)

        return self.info

