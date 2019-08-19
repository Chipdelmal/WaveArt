import array
import matplotlib.pyplot as plt
from pydub import AudioSegment
from pydub.utils import get_array_type
from matplotlib.colors import LinearSegmentedColormap

color = [i / 255 for i in [155, 40, 125]]
colors = [color, (1, 1, 1), color]
cm = LinearSegmentedColormap.from_list("red", colors, N=500)
#cm = plt.cm.get_cmap('bwr')#('seismic')
font = {
    'family': 'sans-serif',
    'color':  'darkblue',
    'weight': 'light',
    'size': 75,
    'alpha': .35
}

(AUD_PATH, OUT_PATH) = ("./audio/", "./out/")
sound = AudioSegment.from_file(file=AUD_PATH + 'impossiblegermany.mp3')
left = sound.split_to_mono()[0]
right = sound.split_to_mono()[1]

bit_depth = left.sample_width * 8
array_type = get_array_type(bit_depth)
numeric_arrayL = array.array(array_type, left._data)
numeric_arrayR = array.array(array_type, right._data)
numeric_array = numeric_arrayL + numeric_arrayR

# Plot the signal read from wav file
fig, ax = plt.subplots(figsize=(30, 6))
plt.scatter(
    range(len(numeric_arrayL)),
    numeric_arrayL,  # vmin=0, vmax=20,
    alpha=.1, c=numeric_arrayL, cmap=cm, s=.05
)
ax.axis('off')
plt.text(
    .5, .5, 'Impossible Germany', fontdict=font,
    horizontalalignment='center', verticalalignment='center',
    transform=ax.transAxes
)
plt.savefig(
    OUT_PATH + 'out.png',
    dpi=100, bbox_inches='tight'
)
