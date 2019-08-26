###############################################################################
# Aux
#   Functions needed by the wavearts script
###############################################################################
# https://stackoverflow.com/questions/9458480/read-mp3-in-python-3/45380892
# https://gist.github.com/kylemcdonald/bedcc053db0e7843ef95c531957cb90f
###############################################################################

import os
import glob
import array
import style
import random
from pydub.utils import mediainfo
from pydub.utils import get_array_type


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


def getNameFromPath(path):
    return path.split('/')[-1].split('.')[0]


def printFilesList(filesList):
    [
        print("\t" + str(i+1) + ': ' +
        getNameFromPath(path)) for (i, path) in enumerate(filesList)
    ]
    return True


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
