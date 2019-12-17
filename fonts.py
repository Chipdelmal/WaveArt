###############################################################################
# Fonts
#   Dedicated script to show the font options available to matplotlib
###############################################################################
# Source:
#   http://jonathansoma.com/lede/data-studio/matplotlib/list-all-fonts-available-in-matplotlib-plus-samples/
#   https://stackoverflow.com/questions/8753835/how-to-get-a-list-of-all-the-fonts-currently-available-for-matplotlib
###############################################################################

import matplotlib.font_manager
from IPython.core.display import HTML


def make_html(fontname):
    # Auxiliary function to have a preview of a font.
    str = "<p>{font}: <span style='font-family:{font}; font-size: 24px;'>{font}</p>"
    return str.format(font=fontname)


matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext='ttf')
code = "\n".join([make_html(font) for font in sorted(
    set([f.name for f in matplotlib.font_manager.fontManager.ttflist]))])
HTML("<div style='column-count: 2;'>{}</div>".format(code))
