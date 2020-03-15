import sqlite3
import sys
from datetime import datetime, timedelta
from dateutil import parser
from enum     import Enum

class Price(Enum):
    OPEN  = 0
    HIGH  = 1
    LOW   = 2
    CLOSE = 3

class Extremum(Enum):
    NOT     = 0
    MINIMUM = 1
    MAXIMUM = 2
    BOTH    = 3

class Tendency(Enum):
    UNDEFINED = 0
    MINRISE   = 1
    MINFALL   = 2
    MAXRISE   = 3
    MAXFALL   = 4
    ALLRISE   = 5
    ALLFALL   = 6
    EXPAND    = 7
    SHRINK    = 8

class PriceKit:
    def __init__(self, openP, highP, lowP, closeP):
        self.prices = [ openP, highP, lowP, closeP ]

    def get(self, price_type):
        return self.prices[price_type.value]

class ShareStat:
    def __init__(self, database, market, share):
        self.conn   = sqlite3.connect(database)
        self.cur    = self.conn.cursor()

        rows = self.cur.execute('''SELECT rowid FROM Market WHERE Abbr = ?''', (market,))
        self.marketId = self.cur.fetchone()[0]

        rows = self.cur.execute('''SELECT rowid FROM Share WHERE Abbr = ?''', (share,))
        self.shareId = self.cur.fetchone()[0]

        # precalculate prices
        self.prices = {}
        rows = self.cur.execute('''SELECT DateTime, OpenPrice, HighPrice, LowPrice, ClosePrice
                                   FROM Quotation
                                   WHERE MarketId = ?
                                       AND ShareId = ?
                                       AND Interval = "15"
                                   ORDER BY DateTime ASC''', (self.marketId, self.shareId,))

        for row in rows:
            self.prices[parser.parse(row[0])] = PriceKit(row[1], row[2], row[3], row[4])

        # precalculate volatilities 15 days
        self.volatDay = {}
        rows = self.cur.execute('''SELECT date(DateTime), min(LowPrice), max(HighPrice)
                                   FROM Quotation
                                   WHERE MarketId = ?
                                       AND ShareId = ?
                                       AND Interval = "15"
                                   GROUP BY date(DateTime)
                                   ORDER BY date(DateTime) ASC''', (self.marketId, self.shareId,))

        for row in rows:
            date = parser.parse(row[0])
            self.volatDay[date] = (row[1], row[2],)

    def getPrices(self, date):
        if date in self.prices:
            return self.prices[date]

        return None

    def getPeriodExtremum(self, dt, periodMinutes):
        prevdt   = dt - timedelta(minutes=periodMinutes)
        priceKit = self.getPrices(dt)

        curMin, curMax       = priceKit.get(Price.LOW), priceKit.get(Price.HIGH)
        periodMin, periodMax = self.getMinMaxPriceInterval(prevdt, dt)

        if curMin <= periodMin and curMax >= periodMax:
            return Extremum.BOTH

        if curMin <= periodMin:
            return Extremum.MINIMUM

        if curMax >= periodMax:
            return Extremum.MAXIMUM

        return Extremum.NOT

    def tendenciesInRow(self, dt, periodMinutes, maxCount=9):
        delta = timedelta(minutes=periodMinutes)
        curDTStart,  curDTEnd    = dt - delta, dt
        preDTStart,  preDTEnd    = curDTStart - delta, curDTStart
        curPriceMin, curPriceMax = self.getMinMaxPriceInterval(curDTStart, curDTEnd)
        prePriceMin, prePriceMax = self.getMinMaxPriceInterval(preDTStart, preDTEnd)

        tendencies = {
            Tendency.UNDEFINED: 0,
            Tendency.MINRISE:   0,
            Tendency.MINFALL:   0,
            Tendency.MAXRISE:   0,
            Tendency.MAXFALL:   0,
            Tendency.ALLRISE:   0,
            Tendency.ALLFALL:   0,
            Tendency.EXPAND:    0,
            Tendency.SHRINK:    0,
        }
        count = 0

        def incTends(tends):
            updated = False
            nonlocal count

            for tend in tends:
                if tendencies[tend] == count:
                    tendencies[tend] += 1
                    updated = True

            count += 1
            return updated

        def checkTendency():
            if prePriceMax is None or curPriceMax is None:
                return True

            if prePriceMin < curPriceMin:
                if prePriceMax  < curPriceMax:
                    return incTends([Tendency.ALLRISE, Tendency.MINRISE, Tendency.MAXRISE])
                if prePriceMax == curPriceMax:
                    return incTends([Tendency.ALLRISE, Tendency.SHRINK, Tendency.MINRISE, Tendency.MAXRISE, Tendency.MAXFALL])
                if prePriceMax  > curPriceMax:
                    return incTends([Tendency.MINRISE, Tendency.MAXFALL, Tendency.SHRINK])

            if prePriceMin == curPriceMin:
                if prePriceMax  < curPriceMax:
                    return incTends([Tendency.ALLRISE, Tendency.EXPAND, Tendency.MINRISE, Tendency.MINFALL, Tendency.MAXRISE])
                if prePriceMax == curPriceMax:
                    return incTends([Tendency.ALLRISE, Tendency.ALLFALL, Tendency.EXPAND, Tendency.SHRINK, Tendency.MINRISE, Tendency.MINFALL, Tendency.MAXRISE, Tendency.MAXFALL])
                if prePriceMax  > curPriceMax:
                    return incTends([Tendency.ALLFALL, Tendency.SHRINK, Tendency.MINRISE, Tendency.MINFALL, Tendency.MAXFALL])

            if prePriceMin > curPriceMin:
                if prePriceMax  < curPriceMax:
                    return incTends([Tendency.EXPAND, Tendency.MINFALL, Tendency.MAXRISE])
                if prePriceMax == curPriceMax:
                    return incTends([Tendency.EXPAND, Tendency.ALLFALL, Tendency.MINFALL, Tendency.MAXRISE, Tendency.MAXFALL])
                if prePriceMax  > curPriceMax:
                    return incTends([Tendency.ALLFALL, Tendency.MINFALL, Tendency.MAXFALL])


        while count < maxCount and checkTendency():
            curDTStart, curDTEnd = preDTStart, preDTEnd
            preDTStart, preDTEnd = preDTStart - delta, preDTStart
            curPriceMin, curPriceMax = self.getMinMaxPriceInterval(curDTStart, curDTEnd)
            prePriceMin, prePriceMax = self.getMinMaxPriceInterval(preDTStart, preDTEnd)

        return tendencies


    def getVolatilityDays(self, date, days):
        rdate = date.replace(hour = 0, minute = 0, second = 0)
        rdateprev = rdate - timedelta(days=days)

        volSum = 0
        count = 0
        while rdateprev < rdate:
            if rdateprev in self.volatDay:
                minPrice, maxPrice = self.volatDay[rdateprev]
                volSum += abs(maxPrice - minPrice)
                count += 1

            rdateprev += timedelta(days=1)

        return round(volSum / count, 4)

    def getVolatilityDaysInterval(self, dtStart, dtEnd):
        rows = self.cur.execute('''SELECT date(DateTime), min(LowPrice), max(HighPrice)
                                   FROM Quotation
                                   WHERE MarketId = ?
                                       AND ShareId = ?
                                       AND Interval = "15"
                                       AND DateTime >= ? AND DateTime < ?
                                   GROUP BY date(DateTime)
                                   ORDER BY date(DateTime) ASC''', (self.marketId, self.shareId, dtStart, dtEnd))
        rows = self.cur.fetchall()
        if len(rows) < 1:
            return 0

        avgVolatility = 0
        for row in rows:
            avgVolatility += abs(row[2] - row[1])

        return round(avgVolatility / len(rows), 4)


    def getMinMaxPriceDays(self, date, days):
        rdate = date.replace(hour = 0, minute = 0, second = 0)
        rdateprev = rdate - timedelta(days=days)

        minResult, maxResult = 999999, 0
        while rdateprev < rdate:
            if rdateprev in self.volatDay:
                minPrice, maxPrice   = self.volatDay[rdateprev]
                minResult, maxResult = min(minResult, minPrice), max(maxResult, maxPrice)

            rdateprev += timedelta(days=1)

        return minResult, maxResult

    def getMinMaxPriceInterval(self, dtStart, dtEnd):
        date = dtStart
        curMin, curMax = 999999, 0
        updated = False
        while date < dtEnd:
            if date in self.prices:
                priceKit       = self.prices[date]
                curMin, curMax = min(curMin, priceKit.get(Price.LOW)), max(curMax, priceKit.get(Price.HIGH))
                updated        = True

            date = date + timedelta(minutes=15)

        if not updated:
            return None, None

        return curMin, curMax

