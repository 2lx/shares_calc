#!/usr/bin/python3
import sqlite3
import sys
from datetime import datetime, timedelta
from enum import Enum

class Price(Enum):
    OPEN  = 0
    HIGH  = 1
    LOW   = 2
    CLOSE = 3

class ShareStat:
    def __init__(self, database, market, share):
        self.conn   = sqlite3.connect(database)
        self.cur    = self.conn.cursor()

        rows = self.cur.execute('''SELECT rowid FROM Market WHERE Abbr = ?''', (market,))
        self.marketId = self.cur.fetchone()[0]

        rows = self.cur.execute('''SELECT rowid FROM Share WHERE Abbr = ?''', (share,))
        self.shareId = self.cur.fetchone()[0]

    def getPrice(self, date, price):
        rows = self.cur.execute('''SELECT OpenPrice, HighPrice, LowPrice, ClosePrice
                                   FROM Quotation
                                   WHERE MarketId = ?
                                       AND ShareId = ?
                                       AND IntervalMin = "15"
                                       AND DateTime == ?''', (self.marketId, self.shareId, date,))

        for row in rows:
            return row[price.value]

        return -1

    def getVolatilityDays(self, date, days):
        rdate = date.replace(hour = 0, minute = 0, second = 0)
        rdateprev = rdate - timedelta(days=days)

        return self.getVolatilityDaysInterval(rdateprev, rdate)

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

        return self.getMinMaxPriceInterval(rdateprev, rdate)


    def getMinMaxPriceInterval(self, dtStart, dtEnd):
        rows = self.cur.execute('''SELECT min(LowPrice), max(HighPrice)
                                   FROM Quotation
                                   WHERE MarketId = ?
                                       AND ShareId = ?
                                       AND IntervalMin == "15"
                                       AND DateTime >= ? AND DateTime <= ?
                                   GROUP BY MarketId''', (self.marketId, self.shareId, dtStart, dtEnd))
        rows = self.cur.fetchall()
        if len(rows) != 1:
            return -1, -1

        return rows[0][0], rows[0][1]
