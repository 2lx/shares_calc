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
                                       AND IntervalMin == "D"
                                       AND DateTime == ?''', (self.marketId, self.shareId, date,))

        for row in rows:
            return row[price.value]

        return -1

    def getVolatility(self, date, days):
        dateprev = date - timedelta(days=days)

        rows = self.cur.execute('''SELECT date(DateTime), LowPrice, HighPrice
                                   FROM Quotation
                                   WHERE MarketId = ?
                                       AND ShareId = ?
                                       AND IntervalMin == "D"
                                       AND DateTime >= ? AND DateTime <= ?
                                   ORDER BY DateTime ASC''', (self.marketId, self.shareId, dateprev, date))

        avgVolatility = 0
        for row in rows:
            avgVolatility += abs(row[2] - row[1])

        return avgVolatility / days

