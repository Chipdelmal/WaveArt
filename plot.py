###############################################################################
# Plot
#   Plot-related routines for the main.py
###############################################################################
# https://matplotlib.org/users/text_props.html
# https://matplotlib.org/api/_as_gen/matplotlib.colors.LinearSegmentedColormap.html#matplotlib.colors.LinearSegmentedColormap.from_list
###############################################################################

import random
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

def rescaleColor(colorEightBit):
    return [i / 255 for i in colorEightBit]


def sampleColorsRandomly(colorsPool):
    colorRand = list(range(len(colorsPool)))
    random.shuffle(colorRand)
    (colorB, colorT) = (
        rescaleColor(colorsPool[colorRand.pop()]),
        rescaleColor(colorsPool[colorRand.pop()])
    )
    return (colorB, colorT)


def defineColorMap(colorsPool):
    (colorB, colorT) = sampleColorsRandomly(colorsPool)
    colorMap = [colorB, (1, 1, 1), colorT]
    cm = LinearSegmentedColormap.from_list("red", colorMap, N=500)
    return cm


def plotWave(
            mix, songName, printName,
            colorMap, font,
            alpha=.075, s=.05, figSize=(30, 16.875/4)
        ):
    fig, ax = plt.subplots(figsize=figSize)
    ax.axis('off')
    plt.autoscale(tight=True)
    plt.scatter(
        range(len(mix)), mix,
        c=mix, alpha=alpha, cmap=colorMap, s=s
    )
    if printName:
        plt.text(
            .5, .5-.01, songName, fontdict=font,
            horizontalalignment='center', verticalalignment='center',
            transform=ax.transAxes
        )
    return (fig, ax)

def saveWave(outPath, fileName, DPI, fileType=".png"):
    plt.savefig(
        outPath + fileName + fileType,
        dpi=DPI, bbox_inches='tight',
        pad_inches=0
    )
    plt.close()
    return True
