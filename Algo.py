#!/usr/bin/python3
from AlgoInfo import AlgoInfo
from ShareStat import ShareStat, Price
from datetime import datetime, timedelta

class Algo:
    def __init__(self, shareStat):
        self.stat = shareStat
        self.info = AlgoInfo()

    def process(self, startDate, endDate, cash):
        minSoldPrice = 0
        sharesCount  = 0
        boughtPrice  = 0
        date = startDate

        while date < endDate:
            volatility15             = self.stat.getVolatilityDays(date, 15)
            openPrice                = self.stat.getPrice(date, Price.OPEN)
            ytdMinPrice, ytdMaxPrice = self.stat.getMinMaxPriceDays(date, 1)
            sysMinPrice, sysMaxPrice = self.stat.getMinMaxPriceDays(date, 14)

            if openPrice > 0:
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
                    minSoldPrice = 0

                self.info.axisDT.append(date)
                self.info.fnPrices.append(openPrice)
                self.info.fnCounts.append(sharesCount)
                self.info.fnSoldPrices.append(minSoldPrice)
                self.info.fnCapital.append(cash + sharesCount * openPrice)

            date += timedelta(minutes=15)

        return self.info

