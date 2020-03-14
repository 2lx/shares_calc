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
                                       AND IntervalMin = "15"
                                   ORDER BY DateTime ASC''', (self.marketId, self.shareId,))

        for row in rows:
            self.prices[parser.parse(row[0])] = PriceKit(row[1], row[2], row[3], row[4])

        # precalculate volatilities 15 days
        self.volatDay = {}
        rows = self.cur.execute('''SELECT date(DateTime), min(LowPrice), max(HighPrice)
                                   FROM Quotation
                                   WHERE MarketId = ?
                                       AND ShareId = ?
                                       AND IntervalMin = "15"
                                   GROUP BY date(DateTime)
                                   ORDER BY date(DateTime) ASC''', (self.marketId, self.shareId,))

        for row in rows:
            date = parser.parse(row[0])
            self.volatDay[date] = (row[1], row[2],)

    def getPrices(self, date):
        if date in self.prices:
            return self.prices[date]

        return None

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
                                       AND IntervalMin = "15"
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
                minPrice, maxPrice = self.volatDay[rdateprev]
                minResult, maxResult = min(minResult, minPrice), max(maxResult, maxPrice)

            rdateprev += timedelta(days=1)

        return minResult, maxResult

    def getMinMaxPriceInterval(self, dtStart, dtEnd):
        rows = self.cur.execute('''SELECT min(LowPrice), max(HighPrice)
                                   FROM Quotation
                                   WHERE MarketId = ?
                                       AND ShareId = ?
                                       AND IntervalMin == "15"
                                       AND DateTime >= ? AND DateTime < ?
                                   GROUP BY MarketId''', (self.marketId, self.shareId, dtStart, dtEnd))
        rows = self.cur.fetchall()
        if len(rows) != 1:
            return -1, -1

        return rows[0][0], rows[0][1]
