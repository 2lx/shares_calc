from AlgoInfo  import AlgoInfo
from ShareStat import *
from State     import State

from datetime  import datetime, timedelta

class Algo2:
    def __init__(self, shareStat):
        self.stat = shareStat
        self.info = AlgoInfo()
        self.cache2d = {}
        self.cache7d = {}
        self.cache15m = {}

    def signal1(self, date):
        whdate = date.replace(hour = 0, minute = 0, second = 0)
        if whdate not in self.cache2d:
            self.cache2d[whdate] = self.stat.tendsRow(date, deltaDays=2)

        if whdate not in self.cache7d:
            self.cache7d[whdate] = self.stat.tendsRow(date, deltaDays=7)

        #  if date not in self.cache15m:
        #      self.cache15m[date] = self.stat.tendsRow(date, deltaMinutes=15)

        #  return self.cache15m[date][Tendency.MAXRISE] >= 1 and \
        #      (self.cache2d[whdate][Tendency.MAXRISE] >= 3 or self.cache7d[whdate][Tendency.MAXRISE] >= 2)
        return (self.cache2d[whdate][Tendency.MAXRISE] >= 3 or self.cache7d[whdate][Tendency.MAXRISE] >= 2)

    def process(self, startDate, endDate, cash):
        date     = startDate
        state    = State(cash, 2.5)
        lastSell = date - timedelta(days=1000)

        while date < endDate:
            priceKit = self.stat.getPrices(date)

            if priceKit is not None:
                volatility15 = self.stat.getVolatilityDays(date, 15)

                if state.shareQty == 0 and self.signal1(date):
                    state.buy(date, priceKit, volatility15)
                elif priceKit.get(Price.LOW) <= state.exitPrice:
                    state.sell(date, priceKit)
                    lastSell = date

                if state.shareQty > 0:
                    state.updateExitPrice(priceKit, volatility15)

                self.info.append(date, priceKit, state, volatility15)

            date += timedelta(minutes=15)

        return self.info

