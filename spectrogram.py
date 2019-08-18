import array
import numpy as np
import matplotlib.pyplot as plt
from pydub import AudioSegment
from pydub.utils import get_array_type

(AUD_PATH, OUT_PATH) = ("./audio/", "./out/")
sound = AudioSegment.from_file(file=AUD_PATH + 'impossiblegermany.mp3')
left = sound.split_to_mono()[0]
right = sound.split_to_mono()[1]

bit_depth = left.sample_width * 8
array_type = get_array_type(bit_depth)
numeric_arrayL = array.array(array_type, left._data)
numeric_arrayR = array.array(array_type, right._data)


# Plot the signal read from wav file
cm = plt.cm.get_cmap('bwr')#('seismic')
fig, ax = plt.subplots()
plt.scatter(
    range(len(numeric_arrayL)),
    numeric_arrayL, #vmin=0, vmax=20,
    alpha=.1, c=numeric_arrayL, cmap=cm, s=.5
)
# plt.plot(numeric_arrayR, color="r",alpha=.1, drawstyle="steps", fillstyle=None)
ax.axis('off')
plt.savefig(
    OUT_PATH + 'out.png',
    dpi=500, bbox_inches='tight'
)
