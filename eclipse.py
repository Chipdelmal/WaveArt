
import aux
import array
from os import path
import numpy as np
from numpy import pi
from sys import argv, exit
from termcolor import cprint
from os.path import expanduser
import matplotlib.pyplot as plt
from pydub import AudioSegment
from pydub.utils import get_array_type
import matplotlib
matplotlib.use('agg')


if aux.isNotebook():
    (AUD_PATH, OUT_PATH, OVW) = (
        './Schemes/OKComputer/05 Let Down.mp3', 
        expanduser('~/Documents/Sync/Waveart/'),
        True
    )
else:
    (AUD_PATH, OUT_PATH, OVW) = (argv[1], argv[2], int(argv[3]))
DPI = 250
###############################################################################
# Aesthetics constants
###############################################################################
(STEP, IN_OFF) = (int(.25e3), 4)
(BITS, SCALE, CLIP, MEAN_SIG) = ((0, 32767), (0, 5), (0, 10), 5e3)
(DIFF_AMP, ROLL_PAD) = (1.35, 10)
(ANGLE_START, ANGLE_DIR, ANGLE_RANGE) = ('E', -1, (2*pi-.125*pi, .125*pi))
(SB_COL, SF_COL) = ('#4A14AACC', '#ffffffAA')
(BG_COL, TX_COL) = ('#000000FF', '#ffffffcc')
###############################################################################
# Load song info
###############################################################################
try:
    (fileName, songName, songArtist) = aux.getFileAndSongInfo(AUD_PATH)
except:
    cprint(f"Error: {AUD_PATH}", "red")
    exit()
# Check if plot exists --------------------------------------------------------
fName = path.join(OUT_PATH, fileName+'.png')
exists = (path.isfile(fName) and not OVW)
if not exists:
    ###########################################################################
    # Load song data
    ###########################################################################
    sound = AudioSegment.from_file(file=AUD_PATH)
    channels = sound.split_to_mono()
    if len(channels) < 2:
        cprint(f"Error: {AUD_PATH}", "red")
        exit()
    bitDepth = channels[0].sample_width*8
    arrayType = get_array_type(bitDepth)
    ###########################################################################
    # Process signals 
    ###########################################################################
    sigRaw = [array.array(arrayType, sig) for sig in [i._data for i in channels]]
    sigAbs = [np.abs(np.array(sig), dtype=np.int64) for sig in sigRaw]
    sigSrt = sigAbs if (np.median(sigAbs[1]) < np.median(sigAbs[0])) else sigAbs[::-1]
    # Scale signal for plot ---------------------------------------------------
    M_POWER = np.mean(sigAbs[0]+sigAbs[1])/2
    sigSca = [np.interp(sig, BITS, (SCALE[0], SCALE[1]*MEAN_SIG/M_POWER)) for sig in sigSrt]
    sigClp = [np.clip(sig, CLIP[0], CLIP[1]) for sig in sigSca]
    KERNEL = np.ones(STEP)/STEP
    sigSmt = [np.convolve(i, KERNEL, mode='full') for i in sigClp]
    sigPad = (np.pad(sigSmt[0], (ROLL_PAD, 0), mode='constant')[:-ROLL_PAD], sigSmt[1])
    sigSmp = [i[0::STEP] for i in sigPad]
    ###########################################################################
    # Plot eclipse
    ###########################################################################
    maxStr = max(len(songArtist), len(songName))
    FONT_SIZE = np.interp(maxStr, (5, 60, 75), (25, 10, 6))
    ANGLES = np.linspace(ANGLE_RANGE[0], ANGLE_RANGE[1], len(sigSmp[0]), endpoint=False)
    # Figure ----------------------------------------------------------------------
    (fig, ax) = plt.subplots(figsize=(16, 9), subplot_kw={"projection": "polar"})
    fig.add_axes(ax)
    ax.set_axis_off()
    ax.vlines(
        ANGLES, IN_OFF, IN_OFF+sigSmp[0]*DIFF_AMP, 
        lw=0.025, colors=SB_COL, zorder=-1
    )
    ax.vlines(
        ANGLES, IN_OFF, IN_OFF+sigSmp[1], 
        lw=0.065, colors=SF_COL, zorder=0
    )
    plt.text(
        .5, .5, f'"{songName}"\n{songArtist}', 
        fontsize=FONT_SIZE, color=TX_COL, font='Gotham Light',
        horizontalalignment='center', verticalalignment='center',
        transform=ax.transAxes
    )
    ax.set_ylim(0, SCALE[1]+1)
    ax.set_facecolor(BG_COL)
    fig.patch.set_facecolor(BG_COL)
    # ax.set_theta_offset(np.pi/2)
    ax.set_theta_zero_location(ANGLE_START)
    ax.set_theta_direction(ANGLE_DIR)
    ax.set_rscale('linear')
    # Save --------------------------------------------------------------------
    plt.savefig(
        fName,
        pad_inches=.5,
        dpi=DPI, bbox_inches='tight',
        transparent=False
    )
    plt.close("all")