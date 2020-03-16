#!/usr/bin/python3
from ShareStat import *

from datetime import datetime, timedelta
import unittest

class TestShareStat(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.stat = ShareStat("shares.db", "SPBEX", "AMD")

    def test_getPrice(self):
        date1 = datetime(2017, 10, 3) + timedelta(hours=22) + self.stat.timeDelta()
        self.assertEqual(self.stat.getPrices(date1).get(Price.OPEN),  13.34)
        self.assertEqual(self.stat.getPrices(date1).get(Price.HIGH),  13.35)
        self.assertEqual(self.stat.getPrices(date1).get(Price.LOW),   13.31)
        self.assertEqual(self.stat.getPrices(date1).get(Price.CLOSE), 13.33)

        date2 = datetime(2018, 5, 3) + timedelta(hours=18) + self.stat.timeDelta()
        self.assertEqual(self.stat.getPrices(date2).get(Price.OPEN),  10.87)
        self.assertEqual(self.stat.getPrices(date2).get(Price.HIGH),  10.94)
        self.assertEqual(self.stat.getPrices(date2).get(Price.LOW),   10.85)
        self.assertEqual(self.stat.getPrices(date2).get(Price.CLOSE), 10.92)

        date3 = datetime(2019, 12, 16) + timedelta(hours=18) + self.stat.timeDelta()
        self.assertEqual(self.stat.getPrices(date3).get(Price.OPEN),  42.61)
        self.assertEqual(self.stat.getPrices(date3).get(Price.HIGH),  42.69)
        self.assertEqual(self.stat.getPrices(date3).get(Price.LOW),   42.50)
        self.assertEqual(self.stat.getPrices(date3).get(Price.CLOSE), 42.65)

    def test_getMinMaxPriceInterval(self):
        date1s = datetime(2017, 10, 1) + timedelta(hours=22) + self.stat.timeDelta()
        date1e = datetime(2017, 10, 3) + timedelta(hours=18) + self.stat.timeDelta()
        self.assertEqual(self.stat.getMinMaxPriceMinutes(date1s, date1e), (12.62, 13.48))

        date2s = datetime(2017, 10, 3) + timedelta(hours=18) + self.stat.timeDelta()
        date2e = datetime(2017, 10, 5) + timedelta(hours=22) + self.stat.timeDelta()
        self.assertEqual(self.stat.getMinMaxPriceMinutes(date2s, date2e), (13.16, 13.53))

        date3s = datetime(2017, 10, 3) + timedelta(hours=14) + self.stat.timeDelta()
        date3e = datetime(2018, 10, 5) + timedelta(hours=22) + self.stat.timeDelta()
        self.assertEqual(self.stat.getMinMaxPriceMinutes(date3s, date3e), ( 9.04, 34.14))

        date4s = datetime(2019,  2, 3)
        date4e = datetime(2019,  9, 5)
        self.assertEqual(self.stat.getMinMaxPriceMinutes(date4s, date4e), (21.04, 35.55))
        delta4 = date4e.date() - date4s.date()
        self.assertEqual(self.stat.getMinMaxPriceDays(date4e, delta4.days), (21.04, 35.55))

        date5s = datetime(2017, 10, 1)
        date5e = datetime(2017, 10, 3)
        self.assertEqual(self.stat.getMinMaxPriceMinutes(date5s, date5e), (12.62, 12.85))
        delta5 = date5e.date() - date5s.date()
        self.assertEqual(self.stat.getMinMaxPriceDays(date5e, delta5.days), (12.62, 12.85))
        date5e1 = datetime(2017, 10, 3) + timedelta(hours=22)
        self.assertEqual(self.stat.getMinMaxPriceDays(date5e1, delta5.days), (12.62, 12.85))

    def test_getVolatilityInterval(self):
        date1e = datetime(2019,  2, 8)
        self.assertEqual(self.stat.getVolatilityDays(date1e, 1), 0.93)
        self.assertEqual(self.stat.getVolatilityDays(date1e, 2), 0.945)
        self.assertEqual(self.stat.getVolatilityDays(date1e, 3), 1.2567)
        self.assertEqual(self.stat.getVolatilityDays(date1e, 4), 1.0975)
        self.assertEqual(self.stat.getVolatilityDays(date1e, 5), 1.0975)

        date4s = datetime(2019,  2, 3)
        date4e = datetime(2019,  9, 5)
        delta4 = date4e.date() - date4s.date()
        self.assertEqual(self.stat.getVolatilityDays(date4e, delta4.days), 1.3109)
        date4e1 = datetime(2019,  9, 5) + timedelta(hours=14) + self.stat.timeDelta()
        self.assertEqual(self.stat.getVolatilityDays(date4e1, delta4.days), 1.3109)

    def test_tendenciesInRow(self):
        date = datetime(2017, 9, 30) + timedelta(hours=15, minutes=30) + self.stat.timeDelta()
        tends = self.stat.tendsRow(date, deltaMinutes=15)

        def checkTends(tendsVals):
            index = 0
            for val in tendsVals:
                self.assertEqual(tends[Tendency(index)], val)
                index += 1

        checkTends([0, 1, 0, 2, 0, 1, 0, 0, 0])

        date = datetime(2018, 2, 3) + timedelta(hours=2, minutes=15) + self.stat.timeDelta()
        tends = self.stat.tendsRow(date, deltaMinutes=15)
        checkTends([0, 4, 2, 0, 2, 0, 2, 0, 2])

        date = datetime(2018, 2, 5) + timedelta(hours=20, minutes=0) + self.stat.timeDelta()
        tends = self.stat.tendsRow(date, deltaMinutes=15)
        checkTends([0, 0, 6, 0, 6, 0, 6, 0, 0])

        date = datetime(2018, 2, 5) + timedelta(hours=23, minutes=45) + self.stat.timeDelta()
        tends = self.stat.tendsRow(date, deltaMinutes=15)
        checkTends([0, 2, 0, 2, 1, 2, 0, 0, 1])

        date = datetime(2018, 2, 6) + timedelta(hours=22, minutes=15) + self.stat.timeDelta()
        tends = self.stat.tendsRow(date, deltaMinutes=15)
        checkTends([0, 1, 6, 2, 0, 1, 0, 2, 0])

        date = datetime(2018, 2, 6) + timedelta(hours=22, minutes=15) + self.stat.timeDelta()
        tends = self.stat.tendsRow(date, deltaMinutes=30)
        checkTends([0, 0, 3, 0, 3, 0, 3, 0, 0])

        date = datetime(2018, 2, 6) + timedelta(hours=22, minutes=15) + self.stat.timeDelta()
        tends = self.stat.tendsRow(date, deltaMinutes=45)
        checkTends([0, 0, 3, 0, 2, 0, 2, 0, 0])

        date = datetime(2019, 2, 8)
        tends = self.stat.tendsRow(date, deltaMinutes=1 * 24 * 60)
        checkTends([0, 0, 1, 0, 1, 0, 1, 0, 0])
        tends = self.stat.tendsRow(date, deltaDays=1)
        checkTends([0, 0, 1, 0, 1, 0, 1, 0, 0])

        date = datetime(2019, 2, 4)
        tends = self.stat.tendsRow(date, deltaMinutes=1 * 24 * 60)
        checkTends([0, 3, 0, 0, 1, 0, 0, 0, 1])
        tends = self.stat.tendsRow(date, deltaDays=1)
        checkTends([0, 3, 0, 0, 1, 0, 0, 0, 1])

        date = datetime(2019, 2, 3)
        tends = self.stat.tendsRow(date, deltaMinutes=2 * 24 * 60)
        checkTends([0, 2, 0, 0, 1, 0, 0, 0, 1])
        tends = self.stat.tendsRow(date, deltaDays=2)
        checkTends([0, 2, 0, 0, 1, 0, 0, 0, 1])

if __name__ == '__main__':
    unittest.main()
