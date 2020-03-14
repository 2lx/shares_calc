#!/usr/bin/python3
import sqlite3
import sys
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from dateutil import parser
from ShareStat import ShareStat, Price

cash         = 2000.0
startDate    = datetime(2017, 10, 1)
endDate      = datetime(2020,  3, 1)
date         = startDate
market       = "SPBEX"
share        = "AMD"
stat         = ShareStat(sys.argv[1], market, share)
minSoldPrice = -1
sharesCount  = 0
boughtPrice  = -1

scaleDT       = []
funPrices     = []
funCounts     = []
funSoldPrices = []
funCapital    = []

while date < endDate:
    volatility15             = stat.getVolatilityDays(date, 15)
    openPrice                = stat.getPrice(date, Price.OPEN)
    ytdMinPrice, ytdMaxPrice = stat.getMinMaxPriceDays(date, 1)
    sysMinPrice, sysMaxPrice = stat.getMinMaxPriceDays(date, 14)

    if openPrice > 0:
        scaleDT.append(date)
        funPrices.append(openPrice)

        if ytdMaxPrice == sysMaxPrice:
            if sharesCount == 0:
                boughtPrice = openPrice
                minSoldPrice = openPrice - 2 * volatility15
                sharesCount = cash // openPrice
                cash = cash - openPrice * sharesCount * 1.0003
                print("Buy : at {0} price {1:0>5.2f}$ X {2:0>4n}"
                    .format(date, openPrice, sharesCount))

            elif minSoldPrice > 0:
                minSoldPrice = max(openPrice - 2 * volatility15, minSoldPrice)

        if sharesCount > 0 and openPrice <= minSoldPrice:
            cash += openPrice * sharesCount * 0.9997
            success = "+" if openPrice > boughtPrice else ""
            print("Sell: at {0} price {1:0>5.2f}$ X {2:0>4n}, remain {3:0>8.2f} {4}"
                    .format(date, openPrice, sharesCount, cash, success))
            sharesCount  = 0
            minSoldPrice = -1

        funCounts.append(sharesCount)
        funSoldPrices.append(minSoldPrice)
        funCapital.append(cash + sharesCount * openPrice)

    date += timedelta(minutes=15)

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True)
fig.suptitle("{0}, {1}".format(market, share), fontsize=16)
fig.tight_layout()
plt.subplots_adjust(hspace=0.1)

ax1.plot(scaleDT, funPrices, color="#2980b9")
ax1.fill_between(scaleDT, 0, funSoldPrices, facecolor="#bdc3c7", edgecolor="#7f8c8d", interpolate=False)
ax1.axis([startDate.date(), endDate.date(), 0, max(funPrices) + 5])
ax1.set_ylabel("Prices")

ax2.fill_between(scaleDT, 0, funCounts, facecolor="#9b59b6", interpolate=False, joinstyle="round")
ax2.axis([startDate.date(), endDate.date(), min(funCounts), max(funCounts) + 5])
ax2.set_ylabel("Share count")

ax3.plot(scaleDT, funCapital, color="#c0392b")
ax3.axis([startDate.date(), endDate.date(), 0, max(funCapital) + 10])
ax3.set_ylabel("Capital")

plt.show()
