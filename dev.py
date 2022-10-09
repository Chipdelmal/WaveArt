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
    '/home/chipdelmal/Documents/Sync/Waveart/', 
    ['*.mp3', '*.m4a']
)
ix = 2
files = [
    "/mnt/Luma/Music/Dinosaur Jr_/I Bet On Sky/1-01 Don't Pretend You Didn't Know.mp3",
    "/mnt/Luma/Music/Arcade Fire/Funeral/09 Rebellion (Lies).mp3",
    "/mnt/Luma/Music/Caamp/Boys (Side A)/05 26.mp3"
]
file = files[ix]
TRK_NUM = 10
step =int(10e3)
###############################################################################
# Process Files
###############################################################################
(MAX_BIT, scaleFactor) = ((0, 32767), (0, 2.5))
(fileName, songName, songArtist) = aux.getFileAndSongInfo(file)
sound = AudioSegment.from_file(file=file)
(left, right) = (sound.split_to_mono()[0], sound.split_to_mono()[1])
bit_depth = left.sample_width * 8
array_type = get_array_type(bit_depth)
(signalL, signalR) = [
    np.interp(
        np.abs(np.array(array.array(array_type, sig), dtype=np.int64)), 
        MAX_BIT, scaleFactor
    )
    for sig in (left._data, right._data)
]
(sigL, sigR) = [i[0::step] for i in (signalL, signalR)]
###############################################################################
# Plot Iris
###############################################################################
innerOffset = 1.25
(astart, aend) = (-.75*np.pi/2, 2.75*np.pi/2)
ANGLES = np.linspace(astart, aend, len(sigL), endpoint=False)
(fig, ax) = plt.subplots(figsize=(8, 8), subplot_kw={"projection": "polar"})
ax.set_theta_offset(np.pi/2)
ax.set_axis_off()
fig.add_axes(ax)
ax.set_rscale('linear')
ax.vlines(
    ANGLES, innerOffset, innerOffset+sigL, 
    lw=0.250, colors='#3a0ca3', alpha=1
)
ax.vlines(
    ANGLES, innerOffset, innerOffset+sigR, 
    lw=0.175, colors='#ffffff', alpha=.975
)
plt.text(
    .475, .5, f'"{songName}" by {songArtist}', 
    fontsize=30, color='#ffffffcc', font='Gotham Light',
    horizontalalignment='left', verticalalignment='center',
    transform=ax.transAxes
)
ax.set_ylim(0, scaleFactor[1]+1)
ax.set_facecolor("k")
fig.patch.set_facecolor("k")
plot.saveWave(OUT_PATH, fileName, DPI, fileType=".png", transparent=False)