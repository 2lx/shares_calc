#!/usr/bin/python3
from AlgoInfo import AlgoInfo
from ShareStat import ShareStat, Price
from datetime import datetime, timedelta

class State:
    def __init__(self, cash):
        self.exitPrice   = 0
        self.sharesCount = 0
        self.boughtPrice = 0
        self.cash        = cash

    def buy(self, price, volat):
        self.boughtPrice = price
        self.exitPrice   = price - 2 * volat
        self.sharesCount = self.cash // price
        self.cash        = self.cash - price * self.sharesCount * 1.0005
        #  print("Buy : at {0} price {1:0>5.2f}$ X {2:0>4n}"
        #      .format(date, price, self.sharesCount))

    def updateExitPrice(self, highPrice, volat):
        self.exitPrice = max(highPrice - 2 * volat, self.exitPrice)

    def sell(self, highPrice):
        self.cash += min(self.exitPrice, highPrice) * self.sharesCount * 0.9995
        self.sharesCount  = 0
        self.exitPrice    = 0
        #  success = "+" if lowPrice > state.boughtPrice else ""
        #  print("Sell: at {0} price {1:0>5.2f}$, cash {3:0>8.2f} {4}"
        #          .format(date, openPrice cash, success))

class SimpleAlgo:
    def __init__(self, shareStat):
        self.stat = shareStat
        self.info = AlgoInfo()

    def process(self, startDate, endDate, cash):
        date  = startDate
        state = State(cash)

        while date < endDate:
            openPrice = self.stat.getPrice(date, Price.OPEN)

            if openPrice > 0:
                volatility15             = self.stat.getVolatilityDays(date, 15)
                ytdMinPrice, ytdMaxPrice = self.stat.getMinMaxPriceDays(date, 1)
                sysMinPrice, sysMaxPrice = self.stat.getMinMaxPriceDays(date, 14)
                lowPrice  = self.stat.getPrice(date, Price.LOW)
                highPrice = self.stat.getPrice(date, Price.HIGH)

                if ytdMaxPrice == sysMaxPrice:
                    if state.sharesCount == 0:
                        state.buy(openPrice, volatility15)

                    elif state.sharesCount > 0:
                        state.updateExitPrice(highPrice, volatility15)

                if state.sharesCount > 0 and lowPrice <= state.exitPrice:
                    state.sell(highPrice)

                self.info.append(date, openPrice, state.sharesCount, state.cash, volatility15, state.exitPrice)

            date += timedelta(minutes=15)

        return self.info

