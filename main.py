###############################################################################
# WaveArt
#   This script takes an audio file (or multiple files), and generates an
#       attractive representation of its waveform.
###############################################################################

import platform
import aux
import plot
import style
from pydub import AudioSegment

(SINGLE_SONG, RANDOM_ORDER, PRINT_NAME, DPI) = ('', True, True, 500)
(AUD_PATH, OUT_PATH, EXTS) = ('./audio/', './out/', ['*.mp3', '*.m4a'])
###############################################################################
# Define style
###############################################################################
fontName = style.fontFromOS(platform.system())
(FONT, COLORS) = (
        style.defineFont(fontName=fontName, size=45, alpha=.04),
        style.COLORS_POOL
    )
###############################################################################
# Load Filenames (paths)
###############################################################################
filesList = aux.getSongsPaths(AUD_PATH, EXTS, SINGLE_SONG, RANDOM_ORDER)
print("Loaded [" + AUD_PATH + "]:")
aux.printFilesList(filesList)
print("\nWorking [" + OUT_PATH + "]:")
###############################################################################
# Process Files
###############################################################################
processStr = '\tProcessing ({}/{}): "{}"'
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
            colorMap=cm, font=FONT, alpha=.2, s=.01, figSize=(30, 16.875/4)
        )
    plot.saveWave(OUT_PATH, fileName, DPI, fileType=".png")
print("Finished")
