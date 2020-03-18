from AlgoInfo import AlgoInfo

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def drawAlgoInfo(info, market, share):
    minDay, maxDay = min(info.axisDT).date(), max(info.axisDT).date()

    fig, axes = plt.subplots(5, 1, sharex=True, gridspec_kw={ 'height_ratios': [5, 1, 1, 1, 1] })
    ax1, ax2, ax3, ax4, ax5 = axes
    fig.suptitle('{0} market'.format(market), fontsize=16)
    fig.tight_layout()
    plt.subplots_adjust(hspace=0.09, left=0.07, right=0.94, bottom=0.04, top=0.935)

    for nn, ax in enumerate(axes):
        locator   = mdates.AutoDateLocator(minticks=15, maxticks=45)
        formatter = mdates.ConciseDateFormatter(locator)
        ax.xaxis.set_major_locator(locator)
        ax.xaxis.set_major_formatter(formatter)

    ax1ymin, ax1ymax = 0, max(info.fnHighPrice) + 2
    ax1.fill_between(info.axisGlobal, ax1ymin, ax1ymax, where=info.fnMarketClose,
        facecolor="#e74c3c",
        joinstyle="bevel",
        capstyle="butt",
        step="mid",
        alpha=0.2,
        label="market close")
    ax1.fill_between(info.axisDT, info.fnLowPrice, info.fnHighPrice,
        facecolor="#2980b9",
        edgecolor="#2980b9",
        joinstyle="bevel",
        capstyle="butt",
        step="mid",
        label="{0} shares price".format(share,))
    ax1.fill_between(info.axisDT, ax1ymin, info.fnSoldPrice,
        facecolor="#bdc3c7",
        edgecolor="#7f8c8d",
        joinstyle="bevel",
        capstyle="butt",
        step="mid",
        label="exit price")
    ax1.axis([minDay, maxDay, ax1ymin, ax1ymax])
    ax1.plot(info.axisBuyPrice, info.fnBuyPrice, "bo",
        color="#2980b9",
        marker=6,
        markersize=12,
        markeredgecolor="#000000",
        label="moment of purchase")
    ax1.plot(info.axisSellSucc, info.fnSellSucc, "bo",
        color="#2ecc71",
        marker=7,
        markersize=12,
        markeredgecolor="#000000",
        label="moment of successful sell")
    ax1.plot(info.axisSellFail, info.fnSellFail, "bo",
        color="#e74c3c",
        marker=7,
        markersize=12,
        markeredgecolor="#000000",
        label="moment of failed sell")
    ax1.set_ylabel("USD")
    ax1.legend()
    ax1.minorticks_on()
    ax1.grid(True, which="major", axis="both", linestyle="--", alpha=0.6)
    ax1.grid(True, which="minor", axis="x", linestyle=":", alpha=0.7)
    ax1.tick_params(top=True, right=True, left=True, bottom=True, labeltop=True, labelright=True)

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
    ax2.grid(True, which="major", axis="both", linestyle="--", alpha=0.6)
    ax2.tick_params(top=True, right=True, left=True, bottom=True, labelright=True)

    ax3.plot(info.axisDT, info.fnCapital,
        color="#c0392b",
        label="capital")
    ax3.axis([minDay, maxDay, 0, max(info.fnCapital) + 100])
    ax3.set_ylabel("USD")
    ax3.legend()
    ax3.grid(True, which="major", axis="both", linestyle="--", alpha=0.6)
    ax3.tick_params(top=True, right=True, left=True, bottom=True, labelright=True)

    ax4.plot(info.axisDT, info.fnVol15Days,
        color="#e67e22",
        label="volatility 15 days")
    ax4.axis([minDay, maxDay, 0, max(info.fnVol15Days) + 0.2])
    ax4.set_ylabel("USD")
    ax4.legend()
    ax4.grid(True, which="major", axis="both", linestyle="--", alpha=0.6)
    ax4.tick_params(top=True, right=True, left=True, bottom=True, labelright=True)

    ax5.plot(info.axisDT, info.fnMinMax2hP,
        color="#1abc9c",
        label="min-max difference 120 minutes")
    ax5.axis([minDay, maxDay, 0, max(info.fnMinMax2hP) + 0.1])
    ax5.set_ylabel("percents")
    ax5.legend()
    ax5.grid(True, which="major", axis="both", linestyle="--", alpha=0.6)
    ax5.tick_params(top=True, right=True, left=True, bottom=True, labelright=True)

    fig.align_labels()
    plt.show()
