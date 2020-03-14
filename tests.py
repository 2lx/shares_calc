#!/usr/bin/python3
from ShareStat import ShareStat, Price

from datetime import datetime, timedelta
import unittest

class TestShareStat(unittest.TestCase):
    def setUp(self):
        self.stat = ShareStat("shares.db", "SPBEX", "AMD")

    def test_getPrice(self):
        date1 = datetime(2017, 10, 3) + timedelta(hours=22)
        self.assertEqual(self.stat.getPrices(date1).get(Price.OPEN),  13.34)
        self.assertEqual(self.stat.getPrices(date1).get(Price.HIGH),  13.35)
        self.assertEqual(self.stat.getPrices(date1).get(Price.LOW),   13.31)
        self.assertEqual(self.stat.getPrices(date1).get(Price.CLOSE), 13.33)

        date2 = datetime(2018, 5, 3) + timedelta(hours=18)
        self.assertEqual(self.stat.getPrices(date2).get(Price.OPEN),  10.87)
        self.assertEqual(self.stat.getPrices(date2).get(Price.HIGH),  10.94)
        self.assertEqual(self.stat.getPrices(date2).get(Price.LOW),   10.85)
        self.assertEqual(self.stat.getPrices(date2).get(Price.CLOSE), 10.92)

        date3 = datetime(2019, 12, 16) + timedelta(hours=18)
        self.assertEqual(self.stat.getPrices(date3).get(Price.OPEN),  42.61)
        self.assertEqual(self.stat.getPrices(date3).get(Price.HIGH),  42.69)
        self.assertEqual(self.stat.getPrices(date3).get(Price.LOW),   42.50)
        self.assertEqual(self.stat.getPrices(date3).get(Price.CLOSE), 42.65)

    def test_getMinMaxPriceInterval(self):
        date1s = datetime(2017, 10, 1) + timedelta(hours=22)
        date1e = datetime(2017, 10, 3) + timedelta(hours=18)
        self.assertEqual(self.stat.getMinMaxPriceInterval(date1s, date1e), (12.62, 13.48))

        date2s = datetime(2017, 10, 3) + timedelta(hours=18)
        date2e = datetime(2017, 10, 5) + timedelta(hours=22)
        self.assertEqual(self.stat.getMinMaxPriceInterval(date2s, date2e), (13.16, 13.53))

        date3s = datetime(2017, 10, 3) + timedelta(hours=14)
        date3e = datetime(2018, 10, 5) + timedelta(hours=22)
        self.assertEqual(self.stat.getMinMaxPriceInterval(date3s, date3e), ( 9.04, 34.14))

        date4s = datetime(2019,  2, 3)
        date4e = datetime(2019,  9, 5)
        self.assertEqual(self.stat.getMinMaxPriceInterval(date4s, date4e), (21.04, 35.55))
        delta4 = date4e.date() - date4s.date()
        self.assertEqual(self.stat.getMinMaxPriceDays(date4e, delta4.days), (21.04, 35.55))

        date5s = datetime(2017, 10, 1)
        date5e = datetime(2017, 10, 3)
        self.assertEqual(self.stat.getMinMaxPriceInterval(date5s, date5e), (12.62, 12.85))
        delta5 = date5e.date() - date5s.date()
        self.assertEqual(self.stat.getMinMaxPriceDays(date5e, delta5.days), (12.62, 12.85))
        date5e1 = datetime(2017, 10, 3) + timedelta(hours=22)
        self.assertEqual(self.stat.getMinMaxPriceDays(date5e1, delta5.days), (12.62, 12.85))


    def test_getVolatilityInterval(self):
        date1s = datetime(2017, 10, 2) + timedelta(hours=22)
        date1e = datetime(2017, 10, 4) + timedelta(hours=18)
        self.assertEqual(self.stat.getVolatilityDaysInterval(date1s, date1e), 0.4167)

        date2s = datetime(2017, 10, 3) + timedelta(hours=18)
        date2e = datetime(2017, 10, 5) + timedelta(hours=22)
        self.assertEqual(self.stat.getVolatilityDaysInterval(date2s, date2e), 0.2633)

        date3s = datetime(2017, 10, 3) + timedelta(hours=14)
        date3e = datetime(2018, 10, 5) + timedelta(hours=22)
        self.assertEqual(self.stat.getVolatilityDaysInterval(date3s, date3e), 0.7056)

        date4s = datetime(2019,  2, 3)
        date4e = datetime(2019,  9, 5)
        self.assertEqual(self.stat.getVolatilityDaysInterval(date4s, date4e), 1.1099)
        delta4 = date4e.date() - date4s.date()
        self.assertEqual(self.stat.getVolatilityDays(date4e, delta4.days), 1.1099)
        date4e1 = datetime(2019,  9, 5) + timedelta(hours=14)
        self.assertEqual(self.stat.getVolatilityDays(date4e1, delta4.days), 1.1099)

if __name__ == '__main__':
    unittest.main()
