from AlgoInfo  import AlgoInfo
from ShareStat import *
from State     import State

from datetime  import datetime, timedelta
import math

class Algo3:
    def __init__(self, shareStat):
        self.stat = shareStat

    def setParams(self, volatDays, volatCoef, cntPercentOffset, cntPercentMult):
        self.volatDays        = volatDays
        self.volatCoef        = volatCoef
        self.cntPercentOffset = cntPercentOffset
        self.cntPercentMult   = cntPercentMult
        self.info             = AlgoInfo()

    def buySignal1(self, date):
        wddate = date.replace(hour = 0, minute = 0, second = 0)
        whdate = date.replace(minute = 0, second = 0)
        self.stat.updateTends(date)

        dlt = date - date.replace(hour=0, minute=0)
        dltMinTime = timedelta(hours=10, minutes=15)
        dltMaxTime = timedelta(hours=21, minutes=30)

        dlt1Min = timedelta(hours=13, minutes=0)
        dlt1Max = timedelta(hours=15, minutes=0)

        dlt2Min = timedelta(hours=17, minutes=0)
        dlt2Max = timedelta(hours=21, minutes=0)

        return   dlt >= dltMinTime and dlt < dltMaxTime and \
            not (dlt >= dlt1Min    and dlt < dlt1Max)   and \
            not (dlt >= dlt2Min    and dlt < dlt2Max)   and \
            self.stat.tends1d[wddate].get(Tendency.MAXRISE) >= 2

    def process(self, startDate, endDate, cash):
        date     = startDate
        state    = State(cash, self.volatCoef)
        lastSell = date - timedelta(days=1000)

        while date < endDate:
            priceKit = self.stat.getPrices(date)
            self.info.appendGlobal(date, priceKit is not None)

            if priceKit is not None:
                volat = self.stat.getVolatilityDays(date, self.volatDays)

                #  if (state.shareQty == 0 or (state.buyPrice <= state.exitPrice - volat)) and self.buySignal1(date):
                #  if (state.shareQty == 0 or (state.buyDate - date).days > 2) and self.buySignal1(date):
                if state.shareQty == 0 and self.buySignal1(date):
                    volatPercent = volat / priceKit.get(Price.OPEN)
                    countPercent = 1 - math.sqrt(max(0, volatPercent - self.cntPercentOffset)) * self.cntPercentMult
                    #  countPercent = 1 - max(0, volatPercent - self.cntPercentOffset) * self.cntPercentMult
                    countPercent = max(0.3, min(1, countPercent))

                    wddate = date.replace(hour = 0, minute = 0, second = 0)
                    if self.stat.tends7d[wddate].get(Tendency.AVGRISE) >= 1:
                        countPercent = 1
                    if self.stat.tends2d[wddate].get(Tendency.AVGFALL) >= 2:
                        countPercent = 0.3
                    #  countPercent = 1
                    #  print(round(volatPercent, 4), round(countPercent, 4))
                    state.buy(date, priceKit, countPercent)
                elif priceKit.get(Price.LOW) <= state.exitPrice:
                    state.sell(date, priceKit)
                    lastSell = date

                if state.shareQty > 0:
                    state.updateExitPrice(priceKit, volat)

                priceKit2h = self.stat.calcPriceKitMinutes(date - timedelta(minutes=60), date)
                minMaxDiff = 0 if (priceKit2h is None) else abs(priceKit2h.get(Price.HIGH) - priceKit2h.get(Price.LOW))
                minMax2hP = minMaxDiff / self.stat.getPrices(date).get(Price.OPEN)

                self.info.append(date, priceKit, state, volat, minMax2hP)

            date += timedelta(minutes=15)

        return self.info

