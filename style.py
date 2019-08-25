
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


COLORS_POOL = [
    [155, 40, 125],     # Red
    [125, 40, 155],     # Purple
    [1, 25, 150],       # Dark Blue
    [150, 200, 255],    # Cyan
    [215, 5, 100],      # Pink
    [55, 5, 105],       # Dark Purple
    [255, 60, 125],     # Green
    [255, 0, 60],       # Magenta
    [150, 0, 255],      # Purple
    [80, 50, 225]       # Purple
]
