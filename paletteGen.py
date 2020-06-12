import numpy as np
import PIL.Image, PIL.ImageDraw
from colorthief import ColorThief
import sys

def palette(img):
    """
    Return palette in descending order of frequency
    """
    arr = np.asarray(img)
    palette, index = np.unique(asvoid(arr).ravel(), return_inverse=True)
    palette = palette.view(arr.dtype).reshape(-1, arr.shape[-1])
    count = np.bincount(index)
    order = np.argsort(count)
    return palette[order[::-1]]

def asvoid(arr):
    """View the array as dtype np.void (bytes)
    This collapses ND-arrays to 1D-arrays, so you can perform 1D operations on them.
    http://stackoverflow.com/a/16216866/190597 (Jaime)
    http://stackoverflow.com/a/16840350/190597 (Jaime)
    Warning:
    >>> asvoid([-0.]) == asvoid([0.])
    array([False], dtype=bool)
    """
    arr = np.ascontiguousarray(arr)
    return arr.view(np.dtype((np.void, arr.dtype.itemsize * arr.shape[-1])))

# PARAMETERS:
# 1: input image filepath
# 2: output image filepath (png)
if len(sys.argv) < 2:
    print("Image file path as parameter!")
else:
    #img = PIL.Image.open(sys.argv[1], 'r').convert('RGB')
    color_thief = ColorThief(sys.argv[1])
    # get palette
    palette = color_thief.get_palette(color_count=6)

    width = 400
    height = 100

    # SAVE COLOR THIEF INTO BARS
    # array = np.zeros([height, width, 3], dtype=np.uint8)
    # array[:,:100] = palette[0] #palette(img)[0]
    # array[:,101:200] = palette[1] #palette(img)[1]
    # array[:,201:300] = palette[2] #palette(img)[2]
    # array[:,301:400] = palette[3] #palette(img)[3]
    # array[:,401:500] = palette[4] #palette(img)[3]
    # array[:,501:600] = palette[5] #palette(img)[3]
    #imgFinal = PIL.Image.fromarray(array)
    #imgFinal.save(sys.argv[2]);

    # SAVE COLOR THIEF INTO CIRCLES
    im = PIL.Image.new('RGBA', (width, height), (255,255,255,0))
    draw = PIL.ImageDraw.Draw(im)
    draw.ellipse((0,0,100,100), fill=palette[0])
    draw.ellipse((100,0,200,100), fill=palette[1])
    draw.ellipse((200,0,300,100), fill=palette[2])
    draw.ellipse((300,0,400,100), fill=palette[3])
    im.save(sys.argv[2], 'PNG',quality=100, optimize=True)
    #im.resize((300,100), resample=PIL.Image.ANTIALIAS)
