import platform
import aux
import plot
import style
import array
import numpy as np
import matplotlib.pyplot as plt
from pydub import AudioSegment
from pydub.utils import mediainfo
from pydub.utils import get_array_type

(SINGLE_SONG, RANDOM_ORDER, PRINT_NAME, DPI) = ('', False, True, 500)
(AUD_PATH, OUT_PATH, EXTS) = (
    './Schemes/OKComputer/', 
    './Schemes/OKComputer/', 
    ['*.mp3', '*.m4a']
)
TRK_NUM = 11
step =int(10e3)
###############################################################################
# Define style
###############################################################################
fontName = style.fontFromOS(platform.system())
(FONT, COLORS) = (
    style.defineFont(fontName=fontName, size=35, alpha=.3),
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
(i, file) = (0, filesList[TRK_NUM-1])
(fileName, songName, songArtist) = aux.getFileAndSongInfo(file)
cm = plot.defineColorMap(COLORS)
sound = AudioSegment.from_file(file=file)
(left, right) = (sound.split_to_mono()[0], sound.split_to_mono()[1])
bit_depth = left.sample_width * 8
array_type = get_array_type(bit_depth)
(signalL, signalR) = [
    np.interp(
        np.abs(np.array(array.array(array_type, sig), dtype=np.int64)), 
        (0, 32767), (0, 3)
    )
    for sig in (left._data, right._data)
]
(sigL, sigR) = [i[0::step] for i in (signalL, signalR)]
###############################################################################
# Plot Iris
###############################################################################
innerOffset = 1.25 # 10e3

(astart, aend) = (-.75*np.pi/2, 2.75*np.pi/2)
ANGLES = np.linspace(astart, aend, len(sigL), endpoint=False)

(fig, ax) = plt.subplots(figsize=(8, 8), subplot_kw={"projection": "polar"})
# ax.axis('off')
ax.set_theta_offset(np.pi/2)
ax.set_axis_off()
fig.add_axes(ax)
ax.set_rscale('linear')
# plt.autoscale(tight=True)
ax.vlines(
    ANGLES, innerOffset, innerOffset+sigL, 
    lw=0.250, colors='#3a0ca3', alpha=.9
)
ax.vlines(
    ANGLES, innerOffset, innerOffset+sigR, 
    lw=0.175, colors='#ffffff', alpha=.9
)
plt.text(
    .5, .5, f'"{songName}" by {songArtist}', 
    fontsize=30, color='#ffffffbb', font='Gotham Light',
    horizontalalignment='left', verticalalignment='center',
    transform=ax.transAxes
)
ax.set_ylim(0, 4) # 25e3+innerOffset)
ax.set_facecolor("k")
fig.patch.set_facecolor("k")
plot.saveWave(OUT_PATH, fileName, DPI, fileType=".png", transparent=False)