
import subprocess
from tqdm import tqdm
from glob import glob
from termcolor import cprint
from os.path import expanduser, join


(AUD_PATH, OUT_PATH) = (
    '/Users/chipdelmal/Pictures/Waveart/', 
    expanduser('/Users/chipdelmal/Pictures/Waveart/out')
)
# Read playlists --------------------------------------------------------------
playlists = glob(join(AUD_PATH, '*m3u'))
# Process playlists -----------------------------------------------------------
for playlist in playlists[:]:
    cprint(playlist, 'white')
    # Get filenames from playlist ---------------------------------------------
    myFile = open(playlist, "r")
    data = myFile.read()
    files = data.split("\n")[::2][1:]
    # Process files -----------------------------------------------------------
    for file in tqdm(files):
        # cmd = ['python', 'eclipse.py', file, OUT_PATH, '1']
        cmd = ['python', 'eclipseSimple.py', file, OUT_PATH, '1']
        subprocess.Popen(cmd).wait()