#!/usr/bin/python3

class AlgoInfo:
    def __init__(self):
        self.axisDT       = []
        self.fnPrice      = []
        self.fnCount      = []
        self.fnCash       = []
        self.fnVolatility = []
        self.fnSoldPrice  = []
        self.fnCapital    = []

    def append(self, date, price, count, cash, volatility, soldPrice):
        self.axisDT.append(date)
        self.fnPrice.append(price)
        self.fnCount.append(count)
        self.fnCash.append(count)
        self.fnVolatility.append(volatility)
        self.fnSoldPrice.append(soldPrice)
        self.fnCapital.append(cash + price * count)
