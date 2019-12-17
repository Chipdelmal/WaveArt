###############################################################################
# Style
#   Definitions of fonts and colors pool
###############################################################################

COLORS_POOL = [
    [155, 40, 125], [125, 40, 155], [1, 25, 150],
    [150, 200, 255], [215, 5, 100], [55, 5, 105],
    [255, 60, 125],  [255, 0, 60],  [150, 0, 255],
    [80, 50, 225]
]


def fontFromOS(systemName):
    # Select font according to OS
    if systemName == 'Darwin':
        FONT = 'Avenir'
    elif systemName == 'Linux':
        FONT = 'Liberation Sans Narrow'
    else:
        FONT = 'Arial'
    return FONT


def defineFont(fontName, color='black', size=50, alpha=.06):
    fontDict = {
        'fontname': fontName,
        'color': color, 'weight': 'light',
        'size': size, 'alpha': alpha
        }
    return fontDict
