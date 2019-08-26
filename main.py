###############################################################################
# WaveArt
#   Playing around with the styling of the waveforms so that automation is
#   easier in the future.
###############################################################################
# https://matplotlib.org/users/text_props.html
# https://matplotlib.org/api/_as_gen/matplotlib.colors.LinearSegmentedColormap.html#matplotlib.colors.LinearSegmentedColormap.from_list
# https://stackoverflow.com/questions/9458480/read-mp3-in-python-3/45380892
# https://gist.github.com/kylemcdonald/bedcc053db0e7843ef95c531957cb90f
###############################################################################

# Required libraries
import os
import glob
import platform
import matplotlib.pyplot as plt
from pydub import AudioSegment
# Auxiliary files on the repository
import aux
import plot
import style


(SINGLE_SONG, RANDOM_ORDER, PRINT_NAME, DPI) = ('', True, True, 500)
(AUD_PATH, OUT_PATH, EXTS) = ('./audio/', './out/', ['*.mp3', '*.m4a'])
###############################################################################
# Define style
###############################################################################
fontName = style.fontFromOS(platform.system())
FONT = style.defineFont(fontName=fontName, size=75, alpha=.06)
COLORS = style.COLORS_POOL

###############################################################################
# Load Filenames (paths)
###############################################################################
filesList = aux.getSongsPaths(AUD_PATH, EXTS, SINGLE_SONG, RANDOM_ORDER)
print("Loaded: ")
aux.printFilesList(filesList)
print("Writing to: " + OUT_PATH + "\n\nProcessing...")

###############################################################################
# Process Files
###############################################################################
processStr = 'Processing {}/{} "{}"'
for (i, file) in enumerate(filesList):
    (fileName, songName) = aux.getFileAndSongNames(file)
    cm = plot.defineColorMap(COLORS)
    ###########################################################################
    # Get Signal
    ###########################################################################
    sound = AudioSegment.from_file(file=file)
    mix = aux.getMixedChannels(sound.normalize())
    print(processStr.format(i + 1, len(filesList), songName))
    ###########################################################################
    # Plot signal
    ###########################################################################
    plot.plotWave(
        mix, songName, PRINT_NAME,
        colorMap=cm, font=FONT, alpha=.075, s=.05, figSize=(30, 16.875/4)
    )
    plot.saveWave(OUT_PATH, fileName, DPI)
print("Finished")
