from enum     import Enum

class Price(Enum):
    OPEN  = 0
    HIGH  = 1
    LOW   = 2
    CLOSE = 3

class Tendency(Enum):
    MINRISE = 0
    MINFALL = 1
    MAXRISE = 2
    MAXFALL = 3
    AVGRISE = 4
    AVGFALL = 5
    ALLRISE = 6
    ALLFALL = 7
    EXPAND  = 8
    SHRINK  = 9

class TendKit:
    def __init__(self):
        self.tends = {
            Tendency.MINRISE:   0,
            Tendency.MINFALL:   0,
            Tendency.MAXRISE:   0,
            Tendency.MAXFALL:   0,
            Tendency.AVGRISE:   0,
            Tendency.AVGFALL:   0,
        }

    def get(self, tend):
        if tend in [Tendency.MINRISE, Tendency.MAXRISE, Tendency.MINFALL, Tendency.MAXFALL, Tendency.AVGRISE, Tendency.AVGFALL]:
            return self.tends[tend]
        elif tend == Tendency.ALLRISE:
            return min(self.tends[Tendency.MINRISE], self.tends[Tendency.MAXRISE])
        elif tend == Tendency.ALLFALL:
            return min(self.tends[Tendency.MINFALL], self.tends[Tendency.MAXFALL])
        elif tend == Tendency.EXPAND:
            return min(self.tends[Tendency.MINFALL], self.tends[Tendency.MAXRISE])
        elif tend == Tendency.SHRINK:
            return min(self.tends[Tendency.MINRISE], self.tends[Tendency.MAXFALL])

    def inc(self, tend):
        if tend in [Tendency.MINRISE, Tendency.MINFALL, Tendency.MAXRISE, Tendency.MAXFALL, Tendency.AVGRISE, Tendency.AVGFALL]:
            self.tends[tend] += 1


class TendsSet:
    def __init__(self, maxCount):
        self.tends    = TendKit()
        self.count    = 0
        self.maxCount = maxCount

    def __repr__(self):
        ts = []
        for k in Tendency:
            ts.append(self.tends.get(k))

        return repr(ts)

    def incTends(self, incTends):
        updated = False

        for tend in incTends:
            if self.tends.get(tend) == self.count:
                self.tends.inc(tend)
                updated = True

        self.count += 1
        return updated and self.count < self.maxCount

    def proceedTend(self, prePriceKit, curPriceKit):
        if prePriceKit is None or curPriceKit is None:
            return False

        prePriceMin, prePriceMax = prePriceKit.get(Price.LOW), prePriceKit.get(Price.HIGH)
        curPriceMin, curPriceMax = curPriceKit.get(Price.LOW), curPriceKit.get(Price.HIGH)
        prePriceAvg = (prePriceKit.get(Price.OPEN) + prePriceKit.get(Price.CLOSE)) / 2.0
        curPriceAvg = (curPriceKit.get(Price.OPEN) + curPriceKit.get(Price.CLOSE)) / 2.0

        if prePriceMax is None or curPriceMax is None:
            return True

        forInc = []
        if prePriceMin <= curPriceMin:
            forInc.append(Tendency.MINRISE)
        if prePriceMin >= curPriceMin:
            forInc.append(Tendency.MINFALL)
        if prePriceMax <= curPriceMax:
            forInc.append(Tendency.MAXRISE)
        if prePriceMax >= curPriceMax:
            forInc.append(Tendency.MAXFALL)
        if prePriceAvg <= curPriceAvg:
            forInc.append(Tendency.AVGRISE)
        if prePriceAvg >= curPriceAvg:
            forInc.append(Tendency.AVGFALL)

        return self.incTends(forInc)
