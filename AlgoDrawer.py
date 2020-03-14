#!/usr/bin/python3
from AlgoInfo import AlgoInfo
import matplotlib.pyplot as plt

def drawAlgoInfo(info, market, share):
    minDay, maxDay = min(info.axisDT).date(), max(info.axisDT).date()

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True)
    fig.suptitle("{0}, {1}".format(market, share), fontsize=16)
    fig.tight_layout()
    plt.subplots_adjust(hspace=0.1, left=0.07)

    ax1.plot(info.axisDT, info.fnPrice, color="#2980b9")
    ax1.fill_between(info.axisDT, 0, info.fnSoldPrice, facecolor="#bdc3c7", edgecolor="#7f8c8d", interpolate=False)
    ax1.axis([minDay, maxDay, 0, max(info.fnPrice) + 5])
    ax1.set_ylabel("Prices")

    ax2.fill_between(info.axisDT, 0, info.fnCount, facecolor="#9b59b6", interpolate=False, joinstyle="round")
    ax2.axis([minDay, maxDay, min(info.fnCount), max(info.fnCount) + 5])
    ax2.set_ylabel("Share count")

    ax3.plot(info.axisDT, info.fnCapital, color="#c0392b")
    ax3.axis([minDay, maxDay, 0, max(info.fnCapital) + 10])
    ax3.set_ylabel("Capital")

    plt.show()
