###############################################################################
# Aux
#   Functions definitions and auxiliary routines needed by the wavearts script
###############################################################################


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
