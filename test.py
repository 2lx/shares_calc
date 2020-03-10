#!/usr/bin/python3
import sqlite3
import sys
from dateutil import parser
from ShareStat import ShareStat, Price

date = parser.parse(sys.argv[2])
days = 15
if len(sys.argv) > 3:
    days = sys.argv[3]

stat = ShareStat(sys.argv[1], "SPBEX", "AMD")
closePrice = stat.getPrice(date, Price.CLOSE)
volatility15 = stat.getVolatility(date, days)

print("Price: {0:.4f}$, Volatility {1:.4f}$, {2:.2f}%".format(closePrice, volatility15, volatility15 * 100.0 / closePrice))

