import sqlite3
import sys
from datetime import datetime, timedelta
from dateutil import parser
from enum     import Enum
from Tendency import *

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

class PriceKit:
    def __init__(self, openP, highP, lowP, closeP):
        self.prices15 = [ openP, highP, lowP, closeP ]

    def get(self, price_type):
        return self.prices15[price_type.value]

class ShareStat:
    def __init__(self, database, market, share):
        self.delta = timedelta(hours=-3)
        self.conn  = sqlite3.connect(database)
        self.cur   = self.conn.cursor()

        rows = self.cur.execute('''SELECT rowid FROM Market WHERE Abbr = ?''', (market,))
        self.marketId = self.cur.fetchone()[0]

        rows = self.cur.execute('''SELECT rowid FROM Share WHERE Abbr = ?''', (share,))
        self.shareId = self.cur.fetchone()[0]

        # precalculate prices15
        self.prices15 = {}
        rows = self.cur.execute('''SELECT DATETIME(DateTime, '-3 hours') as DateTime, OpenPrice, HighPrice, LowPrice, ClosePrice
                                   FROM Quotation
                                   WHERE MarketId = ?
                                       AND ShareId = ?
                                       AND Interval = "15"
                                   ORDER BY DateTime ASC''', (self.marketId, self.shareId,))


        for row in rows:
            date = parser.parse(row[0])
            self.prices15[date] = PriceKit(row[1], row[2], row[3], row[4])

        # precalculate volatilities 15 days
        self.pricesDay = {}
        rows = self.cur.execute('''SELECT date(DATETIME(DateTime, '-3 hours')) AS DateTime,
                                        min(LowPrice) AS minPrice,
                                        max(HighPrice) AS maxPrice,
                                        min(DATETIME(DateTime, '-3 hours')) AS MinDateTime,
                                        max(DATETIME(DateTime, '-3 hours')) AS MaxDateTime
                                   FROM Quotation
                                   WHERE MarketId = ?
                                       AND ShareId = ?
                                       AND Interval = "15"
                                   GROUP BY date(DATETIME(DateTime, '-3 hours'))
                                   ORDER BY DateTime ASC''', (self.marketId, self.shareId,))

        for row in rows:
            date = parser.parse(row[0])
            dateMin, dateMax = parser.parse(row[3]), parser.parse(row[4])
            self.pricesDay[date] = PriceKit(self.prices15[dateMin].get(Price.OPEN), row[2], row[1], self.prices15[dateMax].get(Price.CLOSE))

    def timeDelta(self):
        return self.delta

    def getPrices(self, date):
        if date in self.prices15:
            return self.prices15[date]

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

    def getPrevMinMax(self, dt, deltaMinutes=None, deltaDays=None):
        def getPrices(dt):
            if deltaDays is not None:
                return self.getMinMaxPriceDays(dt, deltaDays)

            if deltaMinutes is not None:
                return self.getMinMaxPriceMinutes(dt - timedelta(minutes=deltaMinutes), dt)

        def prevDT(dt):
            if deltaDays is not None:
                return dt - timedelta(days=deltaDays)

            if deltaMinutes is not None:
                return dt - timedelta(minutes=deltaMinutes)

        priceMin, priceMax = getPrices(dt)
        dtStart = prevDT(dt)

        while (priceMin is None) or (priceMax is None):
            priceMin, priceMax = getPrices(dtStart)
            dtStart = prevDT(dtStart)

        return dtStart, priceMin, priceMax

    def tendsRow(self, dtEnd, deltaDays=None, deltaMinutes=None, maxCount=9):
        dt = dtEnd
        if deltaDays is not None:
            dt = dt.replace(hour = 0, minute = 0, second = 0)

        tends = TendsSet(maxCount)

        curDTStart, curPriceMin, curPriceMax = self.getPrevMinMax(dt, deltaDays=deltaDays, deltaMinutes=deltaMinutes)
        preDTStart, prePriceMin, prePriceMax = self.getPrevMinMax(curDTStart, deltaDays=deltaDays, deltaMinutes=deltaMinutes)

        while tends.proceedTend(curPriceMin, curPriceMax, prePriceMin, prePriceMax):
            curDTStart, curPriceMin, curPriceMax = preDTStart, prePriceMin, prePriceMax
            preDTStart, prePriceMin, prePriceMax = self.getPrevMinMax(preDTStart, deltaDays=deltaDays, deltaMinutes=deltaMinutes)

        return tends.tends

    def getVolatilityDays(self, date, days):
        rdate = date.replace(hour = 0, minute = 0, second = 0)
        rdateprev = rdate - timedelta(days=days)

        volSum = 0
        count = 0
        while rdateprev < rdate:
            if rdateprev in self.pricesDay:
                priceKit = self.pricesDay[rdateprev]
                minPrice, maxPrice = priceKit.get(Price.LOW), priceKit.get(Price.HIGH)
                volSum += abs(maxPrice - minPrice)
                count += 1

            rdateprev += timedelta(days=1)

        return 0 if count == 0 else round(volSum / count, 4)

    #  def getVolatilityDaysInterval(self, dtStart, dtEnd):
    #      rows = self.cur.execute('''SELECT date(DATETIME(DateTime, '-3 hours')) AS DateTime, min(LowPrice), max(HighPrice)
    #                                 FROM Quotation
    #                                 WHERE MarketId = ?
    #                                     AND ShareId = ?
    #                                     AND Interval = "15"
    #                                     AND DateTime >= ? AND DateTime < ?
    #                                 GROUP BY date(DATETIME(DateTime, '-3 hours'))
    #                                 ORDER BY DateTime ASC''', (self.marketId, self.shareId, dtStart, dtEnd))
    #      rows = self.cur.fetchall()
    #      if len(rows) < 1:
    #          return 0
    #
    #      avgVolatility = 0
    #      for row in rows:
    #          avgVolatility += abs(row[2] - row[1])
    #
    #      return round(avgVolatility / len(rows), 4)


    def getMinMaxPriceDays(self, dtEnd, days):
        dateEnd = dtEnd.replace(hour = 0, minute = 0, second = 0)
        date = dateEnd - timedelta(days=days)

        minResult, maxResult = 999999, 0
        updated = False

        while date < dateEnd:
            if date in self.pricesDay:
                priceKit = self.pricesDay[date]
                minPrice, maxPrice   = priceKit.get(Price.LOW), priceKit.get(Price.HIGH)
                minResult, maxResult = min(minResult, minPrice), max(maxResult, maxPrice)
                updated              = True

            date += timedelta(days=1)

        if not updated:
            return None, None

        return minResult, maxResult

    def getMinMaxPriceMinutes(self, dtStart, dtEnd):
        date = dtStart
        curMin, curMax = 999999, 0
        updated = False

        while date < dtEnd:
            if date in self.prices15:
                priceKit       = self.prices15[date]
                curMin, curMax = min(curMin, priceKit.get(Price.LOW)), max(curMax, priceKit.get(Price.HIGH))
                updated        = True

            date = date + timedelta(minutes=15)

        if not updated:
            return None, None

        return curMin, curMax

