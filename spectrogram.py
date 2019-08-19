###############################################################################
# Waveforms
#   Playing around with the styling of the waveforms so that automation is
#   easier in the future.
###############################################################################
# https://matplotlib.org/users/text_props.html
# https://matplotlib.org/api/_as_gen/matplotlib.colors.LinearSegmentedColormap.html#matplotlib.colors.LinearSegmentedColormap.from_list
# https://stackoverflow.com/questions/9458480/read-mp3-in-python-3/45380892
###############################################################################

import array
import matplotlib.pyplot as plt
from pydub import AudioSegment
from pydub.utils import get_array_type
from matplotlib.colors import LinearSegmentedColormap

###############################################################################
# Define style
###############################################################################
(colorT, colorB) = (
    [i / 255 for i in [155, 40, 125]],
    [i / 255 for i in [125, 40, 155]]
)
colors = [colorT, (1, 1, 1), colorB]
cm = LinearSegmentedColormap.from_list("red", colors, N=500)
#cm = plt.cm.get_cmap('bwr')#('seismic')
font = {
    'fontname': "Silom",#'DIN Condensed',
    'color':  'black',
    'weight': 'light',
    'size': 75,
    'alpha': .075
}

###############################################################################
# Load data
###############################################################################
(AUD_PATH, OUT_PATH, NAME, FILE) = (
    "./audio/", "./out/",
    "Tame", '02 Tame.mp3'
)
sound = AudioSegment.from_file(file=AUD_PATH + FILE)
left = sound.split_to_mono()[0]
right = sound.split_to_mono()[1]
peak_amplitude = sound.max
dir(sound)

###############################################################################
# Process channels
###############################################################################
bit_depth = left.sample_width * 8
array_type = get_array_type(bit_depth)
numeric_arrayL = array.array(array_type, left._data)
numeric_arrayR = array.array(array_type, right._data)
numeric_array = numeric_arrayL + numeric_arrayR
mix = [numeric_arrayL[i] + numeric_arrayR[i] for i in range(len(numeric_arrayR))]

###############################################################################
# Plot signal
###############################################################################
fig, ax = plt.subplots(figsize=(30, 6))
ax.axis('off')
plt.scatter(
    range(len(mix)),
    mix, c=mix,
    alpha=.1, cmap=cm, s=.05
    # vmin=0, vmax=20,
)
plt.text(
    .5, .5-.02, NAME, fontdict=font,
    horizontalalignment='center', verticalalignment='center',
    transform=ax.transAxes
)
plt.savefig(
    OUT_PATH + NAME + '.png',
    dpi=300, bbox_inches='tight',
    pad_inches=0
)
plt.close()
