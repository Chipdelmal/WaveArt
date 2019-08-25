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
import array
import platform
import matplotlib.pyplot as plt
from pydub import AudioSegment
from pydub.utils import get_array_type
# Custom files
import style
import aux


(SINGLE_SONG, RANDOM_ORDER, PRINT_NAME) = ('', True, True)
(AUD_PATH, OUT_PATH, EXTS) = ('./audio/', './out/', ['*.mp3', '*.m4a'])
###############################################################################
# Define style
###############################################################################
fontName = style.fontFromOS(platform.system())
FONT = style.defineFont(fontName=fontName, size=75, alpha=.06)
COLORS = style.COLORS_POOL

###############################################################################
# Load Filenames
###############################################################################
filesList = aux.getSongsPaths(AUD_PATH, EXTS, SINGLE_SONG, RANDOM_ORDER)
aux.printFilesList(filesList)
print("Writing to: " + OUT_PATH + "\n\nProcessing...")

###############################################################################
# Process
###############################################################################
processStr = 'Processing {}/{} "{}"'
for (i, file) in enumerate(filesList):
    (fileName, songName) = aux.getFileAndSongNames(file)
    cm = aux.defineColorMap(COLORS)
    ###########################################################################
    # Get Signal
    ###########################################################################
    sound = AudioSegment.from_file(file=file)
    mix = aux.getMixedChannels(sound.normalize())
    print(processStr.format(i + 1, len(filesList), songName))

    ###########################################################################
    # Plot signal
    ###########################################################################
    fig, ax = plt.subplots(figsize=(30, 16.875/4))#(30, 6))
    ax.axis('off')
    plt.autoscale(tight=True)
    plt.scatter(
        range(len(mix)), mix,
        c=mix, alpha=.15, cmap=cm, s=.05
    )
    if PRINT_NAME:
        plt.text(
            .5, .5-.01, songName, fontdict=FONT,
            horizontalalignment='center', verticalalignment='center',
            transform=ax.transAxes
        )
    plt.savefig(
        OUT_PATH + fileName + '.png',
        dpi=300, bbox_inches='tight',
        pad_inches=0
    )
    plt.close()
print("Finished")
