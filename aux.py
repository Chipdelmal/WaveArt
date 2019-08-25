###############################################################################
# Aux
#   Functions definitions and auxiliary routines needed by the wavearts script
###############################################################################

# Required libraries
import os
import glob
import array
import random
from pydub.utils import mediainfo
from pydub.utils import get_array_type
from matplotlib.colors import LinearSegmentedColormap

def rescaleColor(colorEightBit):
    return [i / 255 for i in colorEightBit]


def getNameFromPath(path):
    return path.split('/')[-1].split('.')[0]


def printFilesList(filesList):
    [
        print(str(i+1) + ': ' +
        getNameFromPath(path)) for (i, path) in enumerate(filesList)
    ]
    return True


def getMixedChannels(sound):
    (left, right) = (
            sound.split_to_mono()[0],
            sound.split_to_mono()[1]
        )
    bit_depth = left.sample_width * 8
    array_type = get_array_type(bit_depth)
    (signalL, signalR) = (
        array.array(array_type, left._data),
        array.array(array_type, right._data)
    )
    mix = [signalL[i] + signalR[i] for i in range(len(signalL))]
    return mix


def sampleColorsRandomly(colorsPool):
    colorRand = list(range(len(colorsPool)))
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


def getFileAndSongNames(filePath):
    fileName = os.path.splitext(filePath.split('/')[-1])[0]
    songName = mediainfo(filePath).get('TAG',None)['title']
    return (fileName, songName)


def getSongsPaths(AUD_PATH, EXTS, SINGLE_SONG, RANDOM_ORDER):
    if len(SINGLE_SONG) == 0:
        filesList = []
        for i in EXTS:
            filesList.extend(glob.glob(AUD_PATH + i))
        if (RANDOM_ORDER):
            random.shuffle(filesList)
        else:
            filesList = sorted(filesList)
    else:
        filesList = [AUD_PATH + SINGLE_SONG]
    return filesList
