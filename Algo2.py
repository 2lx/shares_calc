from AlgoInfo  import AlgoInfo
from ShareStat import *
from State     import State

from datetime  import datetime, timedelta

class Algo2:
    def __init__(self, shareStat):
        self.stat      = shareStat
        self.tends1d   = {}
        self.tends2d   = {}
        self.tends7d   = {}
        self.tends15m  = {}
        self.tends60m  = {}

    def setParams(self, volatDays, volatCoef, p1, p2):
        self.volatDays = volatDays
        self.volatCoef = volatCoef
        self.info      = AlgoInfo()

    def buySignal1(self, date):
        wddate = date.replace(hour = 0, minute = 0, second = 0)
        whdate = date.replace(minute = 0, second = 0)

        if wddate not in self.tends1d:
            self.tends1d[wddate] = self.stat.tendsRow(date, deltaDays=1)

        if wddate not in self.tends2d:
            self.tends2d[wddate] = self.stat.tendsRow(date, deltaDays=2)

        #  if wddate not in self.tends7d:
        #      self.tends7d[wddate] = self.stat.tendsRow(date, deltaDays=7)
        #  #
        if date not in self.tends15m:
            self.tends15m[date] = self.stat.tendsRow(date, deltaMinutes=15)

        #  if whdate not in self.tends60m:
        #      self.tends60m[whdate] = self.stat.tendsRow(date, deltaMinutes=60)
        priceKit2h = self.stat.calcPriceKitMinutes(date - timedelta(minutes=60), date)
        minMaxDiff = 0 if (priceKit2h is None) else abs(priceKit2h.get(Price.HIGH) - priceKit2h.get(Price.LOW))
        minMax2hP = minMaxDiff / self.stat.getPrices(date).get(Price.OPEN)

        #  return date.hour >= 9 and self.tends15m[date][Tendency.MINRISE] >= 2 and minMax2hP < 0.08 and \
        #      (self.tends1d[wddate][Tendency.MAXRISE] >= 3 or self.tends2d[wddate][Tendency.MAXRISE] >= 2 or self.tends7d[wddate][Tendency.MAXRISE] >= 1)
        #  if self.tends1d[wddate][Tendency.MAXRISE] >= 3:
        #      print("tends1d")

        # best 1d 7500
        #  return self.tends1d[wddate][Tendency.MAXRISE] >= 2

        #  best 2d 6000
        #  return self.tends2d[wddate][Tendency.MAXRISE] >= 1

        # best 6d 6000
        #  return self.tends7d[wddate][Tendency.MAXRISE] >= 1


        # and minMax2hP < 0.08

        # BAD!
        # self.tends1d[wddate][Tendency.MINRISE] >= 2

        # not BAD
        #and not self.tends1d[wddate].get(Tendency.AVGFALL) >= 3

        return date.hour >= 10 and self.tends1d[wddate].get(Tendency.MAXRISE) >= 2

    def process(self, startDate, endDate, cash):
        date     = startDate
        state    = State(cash, self.volatCoef)
        lastSell = date - timedelta(days=1000)

        while date < endDate:
            priceKit = self.stat.getPrices(date)
            self.info.appendGlobal(date, priceKit is not None)

            if priceKit is not None:
                volatility15 = self.stat.getVolatilityDays(date, self.volatDays)

                if state.shareQty == 0 and self.buySignal1(date):
                    state.buy(date, priceKit, volatility15)
                elif priceKit.get(Price.LOW) <= state.exitPrice:
                    state.sell(date, priceKit)
                    lastSell = date

                if state.shareQty > 0:
                    state.updateExitPrice(priceKit, volatility15)

                priceKit2h = self.stat.calcPriceKitMinutes(date - timedelta(minutes=60), date)
                minMaxDiff = 0 if (priceKit2h is None) else abs(priceKit2h.get(Price.HIGH) - priceKit2h.get(Price.LOW))
                minMax2hP = minMaxDiff / self.stat.getPrices(date).get(Price.OPEN)

                self.info.append(date, priceKit, state, volatility15, minMax2hP)

            date += timedelta(minutes=15)

        return self.info

