from AlgoInfo  import AlgoInfo
from ShareStat import *
from State     import State

from datetime  import datetime, timedelta

class Algo1:
    def __init__(self, shareStat):
        self.stat = shareStat
        self.info = AlgoInfo()

    def setParams(self, p1, p2, p3, p4):
        return

    def process(self, startDate, endDate, cash):
        date  = startDate
        state = State(cash, 2.0)

        while date < endDate:
            priceKit = self.stat.getPrices(date)

            if priceKit is not None:
                volatility15 = self.stat.getVolatilityDays(date, 15)

                if state.shareQty == 0:
                    ytdPriceKit = self.stat.calcPriceKitDays(date, 1)
                    sysPriceKit = self.stat.calcPriceKitDays(date, 14)
                    ytdMinPrice, ytdMaxPrice = ytdPriceKit.get(Price.LOW), ytdPriceKit.get(Price.HIGH)
                    sysMinPrice, sysMaxPrice = sysPriceKit.get(Price.LOW), sysPriceKit.get(Price.HIGH)

                    if ytdMaxPrice == sysMaxPrice:
                        state.buy(priceKit, volatility15)
                elif priceKit.get(Price.LOW) <= state.exitPrice:
                    state.sell(priceKit)

                if state.shareQty > 0:
                    state.updateExitPrice(priceKit, volatility15)

                self.info.append(date, priceKit, state, volatility15)

            date += timedelta(minutes=15)

        return self.info

