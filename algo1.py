#!/usr/bin/python3
import sqlite3
import sys
from datetime import datetime, timedelta
from dateutil import parser
from ShareStat import ShareStat, Price

cash         = 2000.0
date         = datetime(2017, 10, 1)
stat         = ShareStat(sys.argv[1], "SPBEX", "AMD")
minSoldPrice = -1
sharesCount  = 0

while date < datetime(2020, 3, 1):
    #  volatility15             = stat.getVolatilityDays(date, 15)
    openPrice                = stat.getPrice(date, Price.OPEN)
    ytdMinPrice, ytdMaxPrice = stat.getMinMaxPriceDays(date, 1)
    sysMinPrice, sysMaxPrice = stat.getMinMaxPriceDays(date, 14)

    if openPrice > 0:
        if ytdMaxPrice == sysMaxPrice:
            if sharesCount == 0:
                minSoldPrice = openPrice - 2 * volatility15
                sharesCount = cash // openPrice
                cash = cash - openPrice * sharesCount * 1.0003
                print("Buy : at {0} price {1:0>5.2f}$ X {2:0>4n}, remain {3:0>8.2f}, minSold {4:.2f}"
                    .format(date, openPrice, sharesCount, cash, minSoldPrice))

            elif minSoldPrice > 0:
                minSoldPrice = max(openPrice - 2 * volatility15, minSoldPrice)

        if sharesCount > 0 and openPrice <= minSoldPrice:
            cash += openPrice * sharesCount * 0.9997
            print("Sell: at {0} price {1:0>5.2f}$ X {2:0>4n}, remain {3:0>8.2f}"
                    .format(date, openPrice, sharesCount, cash))
            sharesCount  = 0
            minSoldPrice = -1

    date += timedelta(minutes=15)

