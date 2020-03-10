#!/usr/bin/python3
import sqlite3
import sys
from datetime import datetime, timedelta
from dateutil import parser
from enum import Enum

conn = sqlite3.connect(sys.argv[1])

class Price(Enum):
    OPEN  = 0
    HIGH  = 1
    LOW   = 2
    CLOSE = 3

class Stat:
    def __init__(self, market, share):
        self.market = market
        self.share  = share

    def getPrice(self, date, price):
        cur = conn.cursor()
        rows = cur.execute('''SELECT OpenPrice, HighPrice, LowPrice, ClosePrice
                            FROM Quotation
                                INNER JOIN Market ON Quotation.MarketId = Market.rowid
                                INNER JOIN Share ON Quotation.ShareId = Share.rowid
                            WHERE Market.Abbr = ?
                                AND Share.Abbr = ?
                                AND IntervalMin == "D"
                                AND DateTime == ?''', (self.market, self.share, date,))

        for row in rows:
            return row[price.value]

        return -1

    def getVolatility(self, date, days):
        cur = conn.cursor()
        dateprev = date - timedelta(days=days)

        rows = cur.execute('''SELECT date(DateTime), LowPrice, HighPrice
                            FROM Quotation
                                INNER JOIN Market ON Quotation.MarketId = Market.rowid
                                INNER JOIN Share ON Quotation.ShareId = Share.rowid
                            WHERE Market.Abbr = ?
                                AND Share.Abbr = ?
                                AND IntervalMin == "D"
                                AND DateTime >= ? AND DateTime <= ?
                            ORDER BY DateTime ASC''', (self.market, self.share, dateprev, date))

        avgVolatility = 0
        for row in rows:
            avgVolatility += abs(row[2] - row[1])

        return avgVolatility / days

curMarket = "SPBEX"
curShare  = "AMD"

date = parser.parse(sys.argv[2])
days = 15
if len(sys.argv) > 3:
    days = sys.argv[3]

stat = Stat(curMarket, curShare)
closePrice = stat.getPrice(date, Price.CLOSE)
volatility15 = stat.getVolatility(date, 15)

print("Price: {0:.4f}$, Volatility {1:.4f}$, {2:.2f}%".format(closePrice, volatility15, volatility15 * 100.0 / closePrice))

