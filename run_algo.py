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
market    = "SPBEX"
share     = "AMD"

stat = ShareStat(sys.argv[1], market, share)
algo = Algo(stat)
algoInfo = algo.process(startDate, endDate, cash)
drawAlgoInfo(algoInfo, market, share)

