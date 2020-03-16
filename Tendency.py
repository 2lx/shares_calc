from enum     import Enum

class Tendency(Enum):
    UNDEFINED = 0
    MINRISE   = 1
    MINFALL   = 2
    MAXRISE   = 3
    MAXFALL   = 4
    ALLRISE   = 5
    ALLFALL   = 6
    EXPAND    = 7
    SHRINK    = 8


class TendsSet:
    def __init__(self, maxCount):
        self.tends = {
            Tendency.UNDEFINED: 0,
            Tendency.MINRISE:   0,
            Tendency.MINFALL:   0,
            Tendency.MAXRISE:   0,
            Tendency.MAXFALL:   0,
            Tendency.ALLRISE:   0,
            Tendency.ALLFALL:   0,
            Tendency.EXPAND:    0,
            Tendency.SHRINK:    0,
        }
        self.count = 0
        self.maxCount = maxCount

    def incTends(self, incTends):
        updated = False

        for tend in incTends:
            if self.tends[tend] == self.count:
                self.tends[tend] += 1
                updated = True

        self.count += 1
        return updated and self.count < self.maxCount

    def proceedTend(self, curPriceMin, curPriceMax, prePriceMin, prePriceMax):
        if prePriceMax is None or curPriceMax is None:
            return True

        if prePriceMin < curPriceMin:
            if prePriceMax  < curPriceMax:
                return self.incTends([Tendency.ALLRISE, Tendency.MINRISE, Tendency.MAXRISE])
            if prePriceMax == curPriceMax:
                return self.incTends([Tendency.ALLRISE, Tendency.SHRINK, Tendency.MINRISE, Tendency.MAXRISE, Tendency.MAXFALL])
            if prePriceMax  > curPriceMax:
                return self.incTends([Tendency.MINRISE, Tendency.MAXFALL, Tendency.SHRINK])

        if prePriceMin == curPriceMin:
            if prePriceMax  < curPriceMax:
                return self.incTends([Tendency.ALLRISE, Tendency.EXPAND, Tendency.MINRISE, Tendency.MINFALL, Tendency.MAXRISE])
            if prePriceMax == curPriceMax:
                return self.incTends([Tendency.ALLRISE, Tendency.ALLFALL, Tendency.EXPAND, Tendency.SHRINK, \
                                Tendency.MINRISE, Tendency.MINFALL, Tendency.MAXRISE, Tendency.MAXFALL])
            if prePriceMax  > curPriceMax:
                return self.incTends([Tendency.ALLFALL, Tendency.SHRINK, Tendency.MINRISE, Tendency.MINFALL, Tendency.MAXFALL])

        if prePriceMin > curPriceMin:
            if prePriceMax  < curPriceMax:
                return self.incTends([Tendency.EXPAND, Tendency.MINFALL, Tendency.MAXRISE])
            if prePriceMax == curPriceMax:
                return self.incTends([Tendency.EXPAND, Tendency.ALLFALL, Tendency.MINFALL, Tendency.MAXRISE, Tendency.MAXFALL])
            if prePriceMax  > curPriceMax:
                return self.incTends([Tendency.ALLFALL, Tendency.MINFALL, Tendency.MAXFALL])

