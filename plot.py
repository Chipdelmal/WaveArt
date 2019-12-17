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
    # Rescales the color from 8bit to 0-1 float
    return [i / 255 for i in colorEightBit]


def sampleColorsRandomly(colorsPool):
    # Samples two colors randomly from the pool without replacement
    colorRand = list(range(len(colorsPool)))
    random.shuffle(colorRand)
    (colorB, colorT) = (
        rescaleColor(colorsPool[colorRand.pop()]),
        rescaleColor(colorsPool[colorRand.pop()])
        )
    return (colorB, colorT)


def defineColorMap(colorsPool):
    # Creates a duotone linear cm of two randomly selected colors defined in
    #   the pool, with a white buffer in-between
    (colorB, colorT) = sampleColorsRandomly(colorsPool)
    colorMap = [colorB, (1, 1, 1), colorT]
    cm = LinearSegmentedColormap.from_list("dummy", colorMap, N=256)
    return cm


def plotWave(
            mix, songName, printName,
            colorMap, font,
            alpha=.075, s=.05, figSize=(30, 16.875/4)
        ):
    # Creates a stylish scatterplot of a waveform
    fig, ax = plt.subplots(figsize=figSize)
    ax.axis('off')
    plt.autoscale(tight=True)
    plt.scatter(
            range(len(mix)), mix,
            c=mix, alpha=alpha, cmap=colorMap, s=s
        )
    # For the song-name overlay
    if printName:
        plt.text(
                .5, .5-.01, songName, fontdict=font,
                horizontalalignment='center', verticalalignment='center',
                transform=ax.transAxes
            )
    return (fig, ax)


def saveWave(outPath, fileName, DPI, fileType=".png"):
    # Saves the plot
    plt.savefig(
            outPath + fileName + fileType,
            dpi=DPI, bbox_inches='tight', pad_inches=0
        )
    plt.close()
    return True
