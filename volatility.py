#!/usr/bin/python3
import sqlite3
import sys
from datetime import datetime, timedelta
from dateutil import parser

def getVolatility(date, days):
    conn = sqlite3.connect(sys.argv[1])
    cur = conn.cursor()
    dateprev = date - timedelta(days=days)

    rows = cur.execute('''SELECT date(DateTime), min(LowPrice), max(HighPrice), sum(Volume)
                        FROM Quotation
                            INNER JOIN Market ON Quotation.MarketId = Market.rowid
                        WHERE Market.Abbr = "SPBEX"
                            AND DateTime >= ? AND DateTime <= ?
                        GROUP BY date(DateTime)
                        ORDER BY DateTime ASC''',
            (dateprev, date))

    avgVolatility = 0
    for row in rows:
        avgVolatility += abs(row[2] - row[1])

    return avgVolatility / days


date = parser.parse(sys.argv[2])
days = 15
if len(sys.argv) > 3:
    days = sys.argv[3]

print("Volatility {0:f}".format(getVolatility(date, 15)))

