
import aux
import array
from os import path
import numpy as np
from numpy import pi
from sys import argv, exit
from termcolor import cprint
from os.path import expanduser
import matplotlib.pyplot as plt
from mutagen import File
from mutagen.id3 import ID3
from mutagen.mp4 import MP4, MP4Cover
from PIL import Image, ImageFilter
import eyed3
from matplotlib.patches import Rectangle
from io import BytesIO
from pydub import (AudioSegment, effects)
from matplotlib.offsetbox import (OffsetImage, AnnotationBbox)
from pydub.utils import get_array_type
import matplotlib
matplotlib.use('agg')


if aux.isNotebook():
    (AUD_PATH, OUT_PATH, OVW) = (
        '/Users/chipdelmal/Pictures/Waveart/02 Song 2.mp3', 
        expanduser('/Users/chipdelmal/Pictures/Waveart/'),
        True
    )
else:
    (AUD_PATH, OUT_PATH, OVW) = (argv[1], argv[2], int(argv[3]))
DPI = 250
FRAMES = 1500
ALBUM = True
###############################################################################
# Aesthetics constants
###############################################################################
(STEP_SCALE, IN_OFF) = (25, 3)
(BITS, SCALE, CLIP, MEAN_SIG) = ((0, 32767), (0, 5), (0, 10), 5e3)
(DIFF_AMP, ROLL_PAD) = (1.1, 10)
(ANGLE_START, ANGLE_DIR, ANGLE_RANGE) = ('W', 1, (2*pi-0.1*pi, 0.1*pi))
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
    sound = effects.normalize(AudioSegment.from_file(file=AUD_PATH))
    channels = sound.split_to_mono()
    if len(channels) < 2:
        cprint(f"Error: {AUD_PATH}", "red")
        exit()
    bitDepth = channels[0].sample_width*8
    arrayType = get_array_type(bitDepth)
    ###########################################################################
    # Load album cover
    ###########################################################################
    extension = path.splitext(AUD_PATH)[-1]
    if ALBUM:
        if (extension=='.mp3'):
            # tags = ID3(AUD_PATH)    
            # pict = tags.get("APIC:").data
            # img = Image.open(BytesIO(pict))
            audio_file = eyed3.load(AUD_PATH)
            img = Image.open(BytesIO(audio_file.tag.images[0].image_data))
            COVER = True
        elif (extension=='.m4a'):
            tags = MP4(AUD_PATH)
            img = Image.open(BytesIO(tags['covr'][0]))
            COVER = True
        else:
            COVER = False
    ###########################################################################
    # Process signals 
    ###########################################################################
    sigRaw = [array.array(arrayType, sig) for sig in [i._data for i in channels]]
    sigAbs = [np.abs(np.array(sig), dtype=np.int64) for sig in sigRaw]
    sigSrt = sigAbs if (np.median(sigAbs[1]) < np.median(sigAbs[0])) else sigAbs[::-1]
    # sigSrt = np.max(np.array(sigSrt).T, axis=1)
    STEP = int(sigSrt[0].shape[0]/(STEP_SCALE*FRAMES))
    # Scale signal for plot ---------------------------------------------------
    M_POWER = np.mean(sigAbs[0]+sigAbs[1])/2
    sigSca = [np.interp(sig, BITS, (SCALE[0], SCALE[1]*MEAN_SIG/M_POWER)) for sig in sigSrt]
    sigClp = [np.clip(sig, CLIP[0], CLIP[1]) for sig in sigSca]
    KERNEL = np.ones(STEP)/STEP
    sigSmt = [np.convolve(i, KERNEL, mode='full') for i in sigClp]
    sigPad = (np.pad(sigSmt[0], (ROLL_PAD, 0), mode='constant')[:-ROLL_PAD], sigSmt[1])
    sigSmp = [i[0::STEP] for i in sigPad]
    # Get soundframes ---------------------------------------------------------
    sndArray = np.max(np.array(sigSmp).T, axis=1)# sigSmp[0]
    idx = np.round(np.linspace(0, len(sndArray)-1, FRAMES)).astype(int)
    m = sndArray[idx]
    m = np.where(m!=0, abs(np.sqrt(m)), 0)
    # m = np.where(m!=0, abs(m)), 0)
    # Get colors --------------------------------------------------------------
    sca = [np.interp(i, [0, np.max(m)], [0, 1]) for i in m]
    cmap = aux.colorPaletteFromHexList([
        '#9979AC', '#A2A2E0', '#839CE2', '#4B49CF', '#AAC4F2',
        '#8672E7', '#f9f7f3', '#f9f7f3'
    ])
    hexClr = [cmap(i) for i in sca]
    ###########################################################################
    # Plot eclipse
    ###########################################################################
    maxStr = max(len(songArtist), len(songName))
    FONT_SIZE = np.interp(maxStr, (5, 60, 75), (25, 7.5, 4))
    ANGLES = np.linspace(ANGLE_RANGE[0], ANGLE_RANGE[1], len(m), endpoint=False)
    # Figure ------------------------------------------------------------------
    (fig, ax) = plt.subplots(figsize=(10, 10), subplot_kw={"projection": "polar"})
    ax.set_axis_off()
    # Add cover ---------------------------------------------------------------
    if ALBUM and img:
        ax0 = fig.add_subplot(111)
        ax0.imshow(
            img.filter(ImageFilter.SMOOTH_MORE()), 
            zorder=-2
        )
        ax0.axis("off")
        square = Rectangle(
            (0, 0), 10, 10, 
            linewidth=0, facecolor='#000000CC',
            transform=ax0.transAxes, zorder=10
        )
        ax0.add_patch(square)
    # Add waveform ------------------------------------------------------------
    ax = fig.add_subplot(111, polar=True, label="polar")
    ax.vlines(
        ANGLES, IN_OFF, IN_OFF+m*DIFF_AMP, 
        lw=0.425, colors=hexClr, zorder=-1,
        capstyle='round'
    )
    plt.text(
        .5, .5, f'"{songName}"\n{songArtist}', 
        fontsize=FONT_SIZE, color=TX_COL, font='Avenir Next Condensed',
        horizontalalignment='center', verticalalignment='center',
        rotation=0, transform=ax.transAxes
    )
    # Set limits and axes -----------------------------------------------------
    ax.set_axis_off()
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
        pad_inches=0,
        dpi=DPI, bbox_inches='tight',
        transparent=False
    )
    plt.close("all")