
import aux
import plot
import array
import numpy as np
import matplotlib.pyplot as plt
from pydub import AudioSegment
from pydub.utils import mediainfo
from pydub.utils import get_array_type

(SINGLE_SONG, RANDOM_ORDER, PRINT_NAME, DPI) = ('', False, True, 300)
(AUD_PATH, OUT_PATH, EXTS) = (
    './Schemes/OKComputer/', 
    '/home/chipdelmal/Documents/Sync/Waveart/', 
    ['*.mp3', '*.m4a']
)
ix = 9
files = [
    "/mnt/Luma/Music/Dinosaur Jr_/I Bet On Sky/1-01 Don't Pretend You Didn't Know.mp3",
    "/mnt/Luma/Music/Arcade Fire/Funeral/09 Rebellion (Lies).mp3",
    "/mnt/Luma/Music/Caamp/Boys (Side A)/05 26.mp3",
    "/mnt/Luma/Music/Two Door Cinema Club/Changing of the Seasons/01 Changing of the Seasons.mp3",
    "/mnt/Luma/Music/Pixies/Death to the Pixies/03 Tame.mp3",
    "/mnt/Luma/Music/Kashmir/Zitilites/05 Melpomene.mp3",
    "/mnt/Luma/Music/Radiohead/OK Computer/02 Paranoid Android.mp3",
    "/mnt/Luma/Music/Radiohead/OK Computer/05 Let Down.mp3",
    "/mnt/Luma/Music/Radiohead/OK Computer/10 No Surprises.mp3",
    "/mnt/Luma/Music/Radiohead/In Rainbows/1-02 Bodysnatchers.mp3",
    "/mnt/Luma/Music/R.E.M_/Out of Time/02 Losing My Religion.mp3",
    "/mnt/Luma/Music/Blind Pilot/3 Rounds and a Sound/11 3 Rounds and a Sound.mp3",
    "/mnt/Luma/Music/Caamp/By and By/11 By and By.mp3",
    "/mnt/Luma/Music/Caamp/Singles/Lavender Girl.mp3",
    "/mnt/Luma/Music/Houndmouth/Little Neon Limelight/01 - Sedona.mp3",
    "/mnt/Luma/Music/Pixies/Doolittle/03 Wave of Mutilation.mp3",
    "/mnt/Luma/Music/Snow Patrol/Final Straw/07 Run.mp3",
    "/mnt/Luma/Music/Courteeners/Falcon/1-01 The Opener.mp3"
]
file = files[ix]
step =int(.5e3)
innerOffset = 4
(MAX_BIT, scaleFactor, clip) = (
    (0, 32767), (0, 5), (0, 4.75)
)
(diffAmp, rollPad) = (1.25, 10)
###############################################################################
# Process Files
###############################################################################
(fileName, songName, songArtist) = aux.getFileAndSongInfo(file)
sound = AudioSegment.from_file(file=file)
(left, right) = (sound.split_to_mono()[0], sound.split_to_mono()[1])
bit_depth = left.sample_width*8
array_type = get_array_type(bit_depth)
(rawL, rawR) = [
    np.abs(np.array(array.array(array_type, sig), dtype=np.int64))
    for sig in (left._data, right._data)
]
mPower = np.mean(rawL+rawR)/2
(signalL, signalR) = [
    np.clip(
        np.interp(sig, MAX_BIT, (scaleFactor[0], scaleFactor[1]*5e3/mPower)), 
        clip[0], clip[1]
    )
    for sig in (rawL*diffAmp, rawR)
]
kernel = np.ones(step)/step
(l, r) = [
    np.convolve(i, kernel, mode='full') 
    for i in ( 
        np.pad(signalL, (rollPad, 0), mode='constant')[:-rollPad],
        signalR
    )
]
(sigL, sigR) = [i[0::step] for i in (l, r)]
###############################################################################
# Plot Iris
###############################################################################
(astart, aend) = (-.75*np.pi/2, 2.75*np.pi/2)
ANGLES = np.linspace(astart, aend, len(sigL), endpoint=False)
(fig, ax) = plt.subplots(figsize=(16, 9), subplot_kw={"projection": "polar"})
ax.set_theta_offset(np.pi/2)
ax.set_axis_off()
fig.add_axes(ax)
ax.set_rscale('linear')
ax.vlines(
    ANGLES, innerOffset, innerOffset+sigL, 
    lw=0.025, colors='#4A14AA', alpha=.75, 
    zorder=-1
)
ax.vlines(
    ANGLES, innerOffset, innerOffset+sigR, 
    lw=0.050, colors='#ffffff', alpha=1, 
    zorder=0
)
plt.text(
    .5, .5, f'"{songName}"\nby {songArtist}', 
    fontsize=30, color='#ffffffcc', font='Gotham Light',
    horizontalalignment='center', verticalalignment='center',
    transform=ax.transAxes
)
ax.set_ylim(0, scaleFactor[1]+1)
ax.set_facecolor("k")
fig.patch.set_facecolor("k")
plt.savefig(
    OUT_PATH+fileName+'.png',
    pad_inches=1,
    dpi=DPI, bbox_inches='tight',
    transparent=False
)
