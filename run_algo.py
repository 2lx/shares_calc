#!/usr/bin/python3
import sqlite3
import sys
from datetime  import datetime
from dateutil  import parser
from ShareStat import ShareStat

from Algo3      import Algo3 as Algo
from AlgoDrawer import drawAlgoInfo

cash      = 2000.0
startDate = datetime(2017, 10, 1)
endDate   = datetime(2020,  3, 1)
#  endDate   = datetime(2020,  3, 20)
market    = "SPBEX"
share     = "AMD"

stat = ShareStat(sys.argv[1], market, share)

class AlgoResult:
    def __init__(self, capital, volDays, volCoef, cntPercentOffset, cntPercentMult):
        self.capital          = capital
        self.volDays          = volDays
        self.volCoef          = volCoef
        self.cntPercentOffset = cntPercentOffset
        self.cntPercentMult   = cntPercentMult

    def __lt__(self, other):
        return self.capital > other.capital

    def __repr__(self):
        return "Days = {0}, Coef = {1}, cntPrOffset = {2}, cntPrMult = {3}, Capital = {4}"\
            .format(self.volDays, self.volCoef, self.cntPercentOffset, self.cntPercentMult, round(self.capital, 4))

def bestAlgo():
    results = []
    algo = Algo(stat)

    #  for volDays in [1, 2, 4, 6, 7, 8, 10, 14, 15, 21, 28, 30, 35, 45]:
    for volDays in [15]:
        #  print("Days: ", volDays)
        #  for volCoef in [1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.0, 3.1]:
        #  for volCoef in [1.85, 1.9, 1.95, 2, 2.05, 2.1, 2.15]:
        for volCoef in [2]:
            for cntPercentOffset in [0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.10]:
            #  for cntPercentOffset in [0.05, 0.06, 0.07, 0.08, 0.09]:
            #  for cntPercentOffset in [0]:
                print("cntPercOff: ", cntPercentOffset)
                #  for cntPercentMult in [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8,5, 9]:
                for cntPercentMult in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
                #  for cntPercentMult in [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]:
                    algo.setParams(volDays, volCoef, cntPercentOffset, cntPercentMult)
                    algoInfo = algo.process(startDate, endDate, cash)

                    result = algoInfo.fnCapital[-1]
                    results.append(AlgoResult(result, volDays, volCoef, cntPercentOffset, cntPercentMult))

    results.sort()
    count = 0
    for res in results:
        print(res)
        count += 1
        if count > 40:
            break

#  bestAlgo()

algo = Algo(stat)
algo.setParams(15, 2.0, 0.07, 5)
algoInfo = algo.process(startDate, endDate, cash)

result    = algoInfo.fnCapital[-1]
minCap    = round(min(algoInfo.fnCapital), 4)
maxCap    = round(max(algoInfo.fnCapital), 4)
goodDeals = len(algoInfo.fnSellSucc)
badDeals  = len(algoInfo.fnSellFail)
print("Result: {0}, min: {1}, max: {2}, good: {3}, bad: {4}".format(round(result, 2), minCap, maxCap, goodDeals, badDeals))

drawAlgoInfo(algoInfo, market, share)

