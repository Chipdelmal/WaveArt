###############################################################################
# Aux
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
from colour import Color
from pydub.utils import mediainfo
from pydub.utils import get_array_type
from matplotlib.colors import LinearSegmentedColormap, ColorConverter


def getMixedChannels(sound):
    # Combines two channels of a loaded song into a single array
    (left, right) = (sound.split_to_mono()[0], sound.split_to_mono()[1])
    bit_depth = left.sample_width * 8
    array_type = get_array_type(bit_depth)
    (signalL, signalR) = (
            array.array(array_type, left._data),
            array.array(array_type, right._data)
        )
    mix = [signalL[i] + signalR[i] for i in range(len(signalL))]
    return mix


def getNameFromPath(path):
    # Return the name of the file in a path (not safe for names with '.')
    return path.split('/')[-1].split('.')[0]


def printFilesList(filesList):
    # Auxiliary function for terminal printing
    [print('\t' + str(i + 1) + ': ' + getNameFromPath(path)) for (i, path) in enumerate(filesList)]
    return True


def getFileAndSongNames(filePath):
    # Returns the paths and names of the songs contained in a given folder
    #   with the name being loaded from the files' metadata.
    fileName = os.path.splitext(filePath.split('/')[-1])[0]
    songName = mediainfo(filePath).get('TAG', None)['title']
    return (fileName, songName)


def getFileAndSongInfo(filePath):
    # Returns the paths and names of the songs contained in a given folder
    #   with the name being loaded from the files' metadata.
    fileName = os.path.splitext(filePath.split('/')[-1])[0]
    songName = mediainfo(filePath).get('TAG', None)['title']
    songArtist = mediainfo(filePath).get('TAG', None)['artist']
    return (fileName, songName, songArtist)


def getSongsPaths(AUD_PATH, EXTS, SINGLE_SONG, RANDOM_ORDER):
    # Auxiliary function for batch processing of songs
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


def isNotebook():
    try:
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True   # Jupyter notebook or qtconsole
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False      # Probably standard Python interpreter
    
    
def generateAlphaColorMapFromColor(color, minAlpha=0, maxAlpha=1):
    if (type(color) is str):
        color = list(Color(color).rgb)
    alphaMap = LinearSegmentedColormap.from_list(
        'alphaMap', 
        [
            (0, 0, 0, minAlpha), 
            (color[0], color[1], color[2], maxAlpha)
        ]
    )
    return alphaMap


def colorPaletteFromHexList(clist):
    c = ColorConverter().to_rgb
    clrs = [c(i) for i in clist]
    rvb = LinearSegmentedColormap.from_list("hexMap", clrs)
    return rvb