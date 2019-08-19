###############################################################################
# https://matplotlib.org/users/text_props.html
# https://matplotlib.org/api/_as_gen/matplotlib.colors.LinearSegmentedColormap.html#matplotlib.colors.LinearSegmentedColormap.from_list
#
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
    'weight': 'ultralight',
    'size': 75,
    'alpha': .075
}

###############################################################################
# Load data
###############################################################################
(AUD_PATH, OUT_PATH, NAME) = ("./audio/", "./out/", "Golden Days")
sound = AudioSegment.from_file(file=AUD_PATH + 'goldenDays.m4a')
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

###############################################################################
# Plot signal
###############################################################################
fig, ax = plt.subplots(figsize=(30, 6))
plt.scatter(
    range(len(numeric_arrayL)),
    numeric_arrayL, c=numeric_arrayL,
    alpha=.1, cmap=cm, s=.05
    # vmin=0, vmax=20,
)
ax.axis('off')
plt.text(
    .5, .5, NAME, fontdict=font,
    horizontalalignment='center', verticalalignment='center',
    transform=ax.transAxes
)
plt.savefig(
    OUT_PATH + NAME + '.png',
    dpi=300, bbox_inches='tight'
)
plt.close()
