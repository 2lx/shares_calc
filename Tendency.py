from enum     import Enum

class Tendency(Enum):
    MINRISE   = 0
    MINFALL   = 1
    MAXRISE   = 2
    MAXFALL   = 3
    ALLRISE   = 4
    ALLFALL   = 5
    EXPAND    = 6
    SHRINK    = 7

class TendKit:
    def __init__(self):
        self.tends = {
            Tendency.MINRISE:   0,
            Tendency.MINFALL:   0,
            Tendency.MAXRISE:   0,
            Tendency.MAXFALL:   0,
        }

    def get(self, tend):
        if tend in [Tendency.MINRISE, Tendency.MAXRISE, Tendency.MINFALL, Tendency.MAXFALL]:
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
        if tend in [Tendency.MINRISE, Tendency.MAXRISE, Tendency.MINFALL, Tendency.MAXFALL]:
            self.tends[tend] += 1


class TendsSet:
    def __init__(self, maxCount):
        self.tends    = TendKit()
        self.count    = 0
        self.maxCount = maxCount

    def incTends(self, incTends):
        updated = False

        for tend in incTends:
            if self.tends.get(tend) == self.count:
                self.tends.inc(tend)
                updated = True

        self.count += 1
        return updated and self.count < self.maxCount

    def proceedTend(self, curPriceMin, curPriceMax, prePriceMin, prePriceMax):
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

        return self.incTends(forInc)
