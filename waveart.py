###############################################################################
# Waveforms
#   Playing around with the styling of the waveforms so that automation is
#   easier in the future.
###############################################################################
# https://matplotlib.org/users/text_props.html
# https://matplotlib.org/api/_as_gen/matplotlib.colors.LinearSegmentedColormap.html#matplotlib.colors.LinearSegmentedColormap.from_list
# https://stackoverflow.com/questions/9458480/read-mp3-in-python-3/45380892
# https://gist.github.com/kylemcdonald/bedcc053db0e7843ef95c531957cb90f
###############################################################################

import aux
import glob

import array
import random
import matplotlib.pyplot as plt
from pydub import AudioSegment
from pydub.utils import get_array_type
from matplotlib.colors import LinearSegmentedColormap

SINGLE_SONG = ''
###############################################################################
# Define style
###############################################################################
COLORS = [
    [155, 40, 125],     # Red
    [125, 40, 155],     # Purple
    [1, 25, 150],       # Dark Blue
    [150, 200, 255],    # Cyan
    [215, 5, 100],      # Pink
    [55, 5, 105],       # Dark Purple
    [255, 60, 125],     # Green
    [255, 0, 60],       # Magenta
    [150, 0, 255],      # Purple
    [80, 50, 225]       # Purple
]
font = {
    'fontname': 'Liberation Sans Narrow',#'Ubuntu Mono', #"Avenir",
    'color':  'black', 'weight': 'light',
    'size': 100, 'alpha': 0.06
}

###############################################################################
# Load Filenames
###############################################################################
(AUD_PATH, OUT_PATH, EXTS) = ('./audio/', '/home/chipdelmal/Google Drive/WaveArtNT/', ['*.mp3', '*.m4a'])
processStr = 'Processing {}/{} "{}" ({})'
if len(SINGLE_SONG) == 0:
    filesList = []
    for i in EXTS:
        filesList.extend(glob.glob(AUD_PATH + i))
    random.shuffle(filesList)
else:
    filesList = [AUD_PATH + SINGLE_SONG]
[print(str(i+1) + ': ' + path.split('/')[-1].split('.')[0]) for (i, path) in enumerate(filesList)]
print("Writing to: " + OUT_PATH)
print("\nProcessing...")

###############################################################################
# Process
###############################################################################
for (i, file) in enumerate(filesList):
    NAME = file.split('/')[-1].split('.')[0]
    colorRand = list(range(len(COLORS)))
    random.shuffle(colorRand)
    (colorB, colorT) = (
        aux.rescaleColor(COLORS[colorRand.pop()]),
        aux.rescaleColor(COLORS[colorRand.pop()])
    )
    colorMap = [colorB, (1, 1, 1), colorT]
    cm = LinearSegmentedColormap.from_list("red", colorMap, N=500)
    ###########################################################################
    sound = AudioSegment.from_file(file=file)
    soundNorm = sound.normalize()
    (left, right) = (
        soundNorm.split_to_mono()[0],
        soundNorm.split_to_mono()[1]
    )
    peak_amplitude = sound.max

    ###########################################################################
    # Process channels
    ###########################################################################
    bit_depth = left.sample_width * 8
    array_type = get_array_type(bit_depth)
    (signalL, signalR) = (
        array.array(array_type, left._data),
        array.array(array_type, right._data)
    )
    mix = [signalL[i] + signalR[i] for i in range(len(signalL))]
    print(processStr.format(i + 1, len(filesList), NAME, max(mix)))

    ###########################################################################
    # Plot signal
    ###########################################################################
    fig, ax = plt.subplots(figsize=(30, 6))
    ax.axis('off')
    plt.autoscale(tight=True)
    plt.scatter(
        range(len(mix)), mix,
        c=mix, alpha=.2, cmap=cm, s=.05
    )
    # plt.text(
    #     .5, .5-.01, NAME, fontdict=font,
    #     horizontalalignment='center', verticalalignment='center',
    #     transform=ax.transAxes
    # )
    plt.savefig(
        OUT_PATH + NAME + '.png',
        dpi=400, bbox_inches='tight',
        pad_inches=0
    )
    plt.close()
