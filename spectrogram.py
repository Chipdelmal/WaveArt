import array
import matplotlib.pyplot as plt
from pydub import AudioSegment
from pydub.utils import get_array_type

PATH = "./audio/"
sound = AudioSegment.from_file(file=PATH + 'impossiblegermany.mp3')
left = sound.split_to_mono()[0]
right = sound.split_to_mono()[1]

bit_depth = left.sample_width * 8
array_type = get_array_type(bit_depth)
numeric_arrayL = array.array(array_type, left._data)
numeric_arrayR = array.array(array_type, right._data)


# Plot the signal read from wav file
fig, ax = plt.subplots()
plt.plot(numeric_arrayL, alpha=.2)
plt.plot(numeric_arrayR, color="r",alpha=.1, drawstyle="steps", fillstyle=None)
ax.axis('off')
plt.show()
