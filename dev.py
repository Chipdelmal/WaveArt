
import aux
import array
import numpy as np
from os import path
from tqdm import tqdm
from glob import glob
import matplotlib.pyplot as plt
from pydub import AudioSegment
from pydub.utils import mediainfo
from pydub.utils import get_array_type

(SINGLE_SONG, RANDOM_ORDER, PRINT_NAME, DPI) = ('', False, True, 300)
(AUD_PATH, OUT_PATH, EXTS) = (
    './Schemes/', 
    '/home/chipdelmal/Documents/Sync/Waveart/', 
    ['*.mp3', '*.m4a']
)
ix = -6
playlists = glob(AUD_PATH+'*m3u')
for playlist in playlists:
    # Get filenames from playlist ---------------------------------------------
    my_file = open(playlist, "r")
    data = my_file.read()
    files = data.split("\n")[::2][1:]
    # Constants ---------------------------------------------------------------
    step =int(.25e3)
    innerOffset = 4
    (MAX_BIT, scaleFactor, clip) = (
        (0, 32767), (0, 5), (0, 10)
    )
    (diffAmp, rollPad) = (1.25, 10)
    file = files[ix]
    for file in tqdm(files[::]):
        print(file)
        ###########################################################################
        # Process Files
        ###########################################################################
        (fileName, songName, songArtist) = aux.getFileAndSongInfo(file)
        if not path.isfile(file):
            continue
        sound = AudioSegment.from_file(file=file)
        (left, right) = (sound.split_to_mono()[0], sound.split_to_mono()[1])
        bit_depth = left.sample_width*8
        array_type = get_array_type(bit_depth)
        (rawL, rawR) = [
            np.abs(np.array(array.array(array_type, sig), dtype=np.int64))
            for sig in (left._data, right._data)
        ]
        (rawL, rawR) = (rawL, rawR) if (np.median(rawR)<np.median(rawL)) else (rawR, rawL)
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
        ###########################################################################
        # Plot Iris
        ###########################################################################
        (astart, aend) = (2*np.pi-.25*np.pi/2, 0+.25*np.pi/2)
        maxStr = max(len(songArtist), len(songName))
        fontSize = np.interp(maxStr, (5, 60), (25, 10))
        ANGLES = np.linspace(astart, aend, len(sigL), endpoint=False)
        (fig, ax) = plt.subplots(figsize=(16, 9), subplot_kw={"projection": "polar"})
        ax.set_theta_offset(np.pi/2)
        ax.set_axis_off()
        fig.add_axes(ax)
        ax.set_theta_zero_location('E')
        ax.set_theta_direction(-1)
        ax.set_rscale('linear')
        ax.vlines(
            ANGLES, innerOffset, innerOffset+sigL, 
            lw=0.025, colors='#4A14AA', alpha=.90, 
            zorder=-1
        )
        ax.vlines(
            ANGLES, innerOffset, innerOffset+sigR, 
            lw=0.065, colors='#ffffff', alpha=.70, 
            zorder=0
        )
        plt.text(
            .5, .5, f'"{songName}"\n{songArtist}', 
            fontsize=fontSize, color='#ffffffcc', font='Gotham Light',
            horizontalalignment='center', verticalalignment='center',
            transform=ax.transAxes
        )
        ax.set_ylim(0, scaleFactor[1]+1)
        ax.set_facecolor("k")
        fig.patch.set_facecolor("k")
        plt.savefig(
            OUT_PATH+fileName+'.png',
            pad_inches=.5,
            dpi=DPI, bbox_inches='tight',
            transparent=False
        )
        plt.close("all")
