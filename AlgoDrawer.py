from AlgoInfo import AlgoInfo

import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def drawAlgoInfo(info, market, share):
    minDay, maxDay = min(info.axisDT).date(), max(info.axisDT).date()

    fig, axes = plt.subplots(3, 1, sharex=True, gridspec_kw={ 'height_ratios': [5, 2, 2] })
    ax1, ax2, ax3 = axes
    fig.suptitle('{0} market'.format(market), fontsize=16)
    fig.tight_layout()
    plt.subplots_adjust(hspace=0.09, left=0.07, right=0.94, bottom=0.04, top=0.935)

    #  axis_major_ticks = []
    #  dt = info.axisDT[0].replace(hour=0,minute=0,second=0)
    #  while dt < info.axisDT[-1]:
    #      axis_major_ticks.append(dt)
    #      dt += timedelta(days=190)


    ax1.fill_between(info.axisDT, info.fnLowPrice, info.fnHighPrice,
        facecolor="#2980b9",
        edgecolor="#2980b9",
        joinstyle="bevel",
        capstyle="butt",
        step="mid",
        label="{0} shares price".format(share,))
    ax1.fill_between(info.axisDT, 0, info.fnSoldPrice,
        facecolor="#bdc3c7",
        edgecolor="#7f8c8d",
        joinstyle="bevel",
        capstyle="butt",
        step="mid",
        label="exit price")
    ax1.axis([minDay, maxDay, 0, max(info.fnHighPrice) + 5])
    ax1.plot(info.axisBuyPrice, info.fnBuyPrice, "bo",
        color="#2980b9",
        marker=6,
        markersize=12,
        markeredgecolor="#000000")
    ax1.plot(info.axisSellSucc, info.fnSellSucc, "bo",
        color="#2ecc71",
        marker=7,
        markersize=12,
        markeredgecolor="#000000")
    ax1.plot(info.axisSellFail, info.fnSellFail, "bo",
        color="#e74c3c",
        marker=7,
        markersize=12,
        markeredgecolor="#000000")
    ax1.set_ylabel("USD")
    ax1.legend()
    ax1.tick_params(top=True, right=True, left=True, bottom=True, labeltop=True, labelright=True)
    ax1.minorticks_on()
    ax1.grid(True, which="both", axis="x", linestyle="--", alpha=0.5)

    ax2.fill_between(info.axisDT, 0, info.fnCount,
        facecolor="#fda7df",
        edgecolor="#8e44ad",
        joinstyle="bevel",
        capstyle="butt",
        step="mid",
        label="acquired AMD shares")
    ax2.axis([minDay, maxDay, min(info.fnCount), max(info.fnCount) + 5])
    ax2.set_ylabel("Amount")
    ax2.legend()
    ax2.tick_params(top=True, right=True, left=True, bottom=True, labeltop=True, labelright=True)
    ax2.grid(True, which="major", axis="both", linestyle="--", alpha=0.5)

    ax3.plot(info.axisDT, info.fnCapital,
        color="#c0392b",
        label="capital")
    ax3.axis([minDay, maxDay, 0, max(info.fnCapital) + 100])
    ax3.set_ylabel("USD")
    ax3.legend()
    ax3.tick_params(top=True, right=True, left=True, bottom=True, labeltop=True, labelright=True)
    ax3.grid(True, which="major", axis="both", linestyle="--", alpha=0.5)

    fig.align_labels()

    plt.show()
