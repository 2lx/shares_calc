import sqlite3
import sys
from datetime import datetime, timedelta
from dateutil import parser
from enum     import Enum
from Tendency import *

#  class Extremum(Enum):
#      NOT     = 0
#      MINIMUM = 1
#      MAXIMUM = 2
#      BOTH    = 3

class PriceKit:
    def __init__(self, openP, highP, lowP, closeP):
        self.prices = [ openP, highP, lowP, closeP ]

    def __eq__(self, other):
        return self.prices == other.prices

    def __repr__(self):
        return repr(self.prices)

    def get(self, price_type):
        return self.prices[price_type.value]

class ShareStat:
    def __init__(self, database, market, share):
        self.delta    = timedelta(hours = -3)
        self.conn     = sqlite3.connect(database)
        self.cur      = self.conn.cursor()
        self.tends1d  = {}
        self.tends2d  = {}
        self.tends7d  = {}
        self.tends15m = {}
        self.tends60m = {}

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
            priceOpen, priceClose = self.prices15[dateMin].get(Price.OPEN), self.prices15[dateMax].get(Price.CLOSE)
            assert(priceOpen is not None and priceClose is not None)
            self.pricesDay[date] = PriceKit(priceOpen, row[2], row[1], priceClose)

    def timeDelta(self):
        return self.delta

    def updateTends(self, date):
        wddate = date.replace(hour = 0, minute = 0, second = 0)
        whdate = date.replace(minute = 0, second = 0)

        if wddate not in self.tends1d:
            self.tends1d[wddate] = self.tendsRow(date, deltaDays=1)

        if wddate not in self.tends2d:
            self.tends2d[wddate] = self.tendsRow(date, deltaDays=2)

        if wddate not in self.tends7d:
            self.tends7d[wddate] = self.tendsRow(date, deltaDays=7)

        #  if date not in self.tends15m:
            #  self.tends15m[date] = self.stat.tendsRow(date, deltaMinutes=15)


    def getPrices(self, date):
        if date in self.prices15:
            return self.prices15[date]

        return None

    #  def getPeriodExtremum(self, dt, periodMinutes):
    #      prevdt   = dt - timedelta(minutes=periodMinutes)
    #      priceKit = self.getPrices(dt)
    #
    #      curMin, curMax       = priceKit.get(Price.LOW), priceKit.get(Price.HIGH)
    #      periodMin, periodMax = self.getMinMaxPriceInterval(prevdt, dt)
    #
    #      if curMin <= periodMin and curMax >= periodMax:
    #          return Extremum.BOTH
    #
    #      if curMin <= periodMin:
    #          return Extremum.MINIMUM
    #
    #      if curMax >= periodMax:
    #          return Extremum.MAXIMUM
    #
    #      return Extremum.NOT

    def getPrevDatePriceKit(self, dt, deltaMinutes=None, deltaDays=None):
        def getPrices(dt):
            if deltaDays is not None:
                return self.calcPriceKitDays(dt, deltaDays)

            if deltaMinutes is not None:
                return self.calcPriceKitMinutes(dt - timedelta(minutes=deltaMinutes), dt)

        def prevDT(dt):
            if deltaDays is not None:
                return dt - timedelta(days=deltaDays)

            if deltaMinutes is not None:
                return dt - timedelta(minutes=deltaMinutes)

        priceKit = getPrices(dt)
        dtStart = prevDT(dt)

        while priceKit is None and dtStart > datetime(2017, 9, 1):
            priceKit = getPrices(dtStart)
            dtStart = prevDT(dtStart)

        return dtStart, priceKit

    def tendsRow(self, dtEnd, deltaDays=None, deltaMinutes=None, maxCount=9):
        dt = dtEnd
        if deltaDays is not None:
            dt = dt.replace(hour = 0, minute = 0, second = 0)

        tends = TendsSet(maxCount)

        curDTStart, curPriceKit = self.getPrevDatePriceKit(dt,         deltaDays=deltaDays, deltaMinutes=deltaMinutes)
        preDTStart, prePriceKit = self.getPrevDatePriceKit(curDTStart, deltaDays=deltaDays, deltaMinutes=deltaMinutes)
        #  print(curDTStart, curPriceKit)
        #  print(preDTStart, prePriceKit)

        while tends.proceedTend(prePriceKit, curPriceKit):
            curDTStart, curPriceKit = preDTStart, prePriceKit
            preDTStart, prePriceKit = self.getPrevDatePriceKit(curDTStart, deltaDays=deltaDays, deltaMinutes=deltaMinutes)
        #      print(preDTStart, prePriceKit)
        #
        #  print(tends)

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

    #  def getVolatilityMinutes(self, dtStart, dtEnd):
    #      rows = self.cur.execute('''SELECT min(LowPrice), max(HighPrice)
    #                                 FROM Quotation
    #                                 WHERE MarketId = ?
    #                                     AND ShareId = ?
    #                                     AND Interval = "15"
    #                                     AND DateTime >= ? AND DateTime < ?
    #                                 GROUP BY MarketId''', (self.marketId, self.shareId, dtStart - self.timeDelta(), dtEnd - self.timeDelta()))
    #      rows = self.cur.fetchall()
    #      if len(rows) != 1:
    #          return 0
    #
    #      if rows[0][0] is None and rows[0][1] is None:
    #          return 0
    #
    #      return abs(rows[0][1] - rows[0][0])

    def calcPriceKitDays(self, dateEnd, days):
        dtEnd = dateEnd.replace(hour = 0, minute = 0, second = 0)
        dt = dtEnd - timedelta(days=days)

        openResult, closeResult = None, None
        lowResult,  highResult  = 999999, 0
        updated                 = False

        while dt < dtEnd:
            if dt in self.pricesDay:
                priceKit              = self.pricesDay[dt]
                lowPrice,  highPrice  = priceKit.get(Price.LOW), priceKit.get(Price.HIGH)
                lowResult, highResult = min(lowResult, lowPrice), max(highResult, highPrice)

                if openResult is None:
                    openResult = priceKit.get(Price.OPEN)
                closeResult = priceKit.get(Price.CLOSE)

                updated = True

            dt += timedelta(days=1)

        if not updated:
            return None

        return PriceKit(openResult, highResult, lowResult, closeResult)

    def calcPriceKitMinutes(self, dtStart, dtEnd):
        dt = dtStart

        openResult, closeResult = None, None
        lowResult,  highResult  = 999999, 0
        updated                 = False

        while dt < dtEnd:
            if dt in self.prices15:
                priceKit              = self.prices15[dt]
                lowPrice,  highPrice  = priceKit.get(Price.LOW), priceKit.get(Price.HIGH)
                lowResult, highResult = min(lowResult, lowPrice), max(highResult, highPrice)

                if openResult is None:
                    openResult = priceKit.get(Price.OPEN)
                closeResult = priceKit.get(Price.CLOSE)

                updated = True

            dt += timedelta(minutes=15)

        if not updated:
            return None

        return PriceKit(openResult, highResult, lowResult, closeResult)

