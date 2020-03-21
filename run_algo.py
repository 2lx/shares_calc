#!/usr/bin/python3
import sqlite3
import sys
from datetime  import datetime
from dateutil  import parser
from ShareStat import ShareStat

from Algo2      import Algo2 as Algo
from AlgoDrawer import drawAlgoInfo

cash      = 2000.0
startDate = datetime(2017, 10, 1)
endDate   = datetime(2020,  3, 1)
#  endDate   = datetime(2020,  3, 20)
market    = "SPBEX"
share     = "BBBY"

stat = ShareStat(sys.argv[1], market, share)

class AlgoResult:
    def __init__(self, capital, volDays, volCoef):
        self.capital = capital
        self.volDays = volDays
        self.volCoef = volCoef

    def __lt__(self, other):
        return self.capital > other.capital

    def __repr__(self):
        return "Days = {0}, Coef = {1}, Capital = {2}".format(self.volDays, self.volCoef, round(self.capital, 4))

def bestAlgo():
    results = []
    algo = Algo(stat)

    for volDays in [1, 2, 4, 6, 7, 8, 10, 14, 15, 21, 28, 30, 35, 45]:
        print("Days: ", volDays)
        for volCoef in [15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]:
            algo.setParams(volDays, volCoef / 10)
            algoInfo = algo.process(startDate, endDate, cash)

            result = algoInfo.fnCapital[-1]
            results.append(AlgoResult(result, volDays, volCoef / 10))

    results.sort()
    count = 0
    for res in results:
        print(res)
        count += 1
        if count > 40:
            break

bestAlgo()

#  algo = Algo(stat)
#  algo.setParams(15, 2.0)
#  algoInfo = algo.process(startDate, endDate, cash)
#  drawAlgoInfo(algoInfo, market, share)

