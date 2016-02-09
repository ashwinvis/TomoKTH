"""Essential operators for input and output (:mod:`tomokth.operators.io`)
==========================================================================

.. currentmodule:: tomokth.operators.io

Provides
--------
imread, imshow, imsave, implot

"""

import numpy as np
import matplotlib.pyplot as plt
try:
    from skimage import io as _io_
    from skimage.io import imshow
    from skimage.exposure import rescale_intensity
except ImportError:
    from matplotlib import image as _io_
    from matplotlib.pyplot import imshow


def imread(filename):
    """Read an image file into a numpy array

    Parameters
    ----------
    filename :  string
        the absolute path of the image file that is to be read.

    Returns
    -------
    arr : ndarray
    A 2D numpy array with grey levels
    """
    try:
        arr = _io_.imread(filename, as_grey=True)
    except TypeError:
        arr = _io_.imread(filename)

    return arr


def imsave(filename, arr):
    """Saves a numpy array into a text/image file

    Parameters
    ----------
    filename :  string
            the absolute path of the image file that is to be read.
    """
    if filename[-3:] is 'txt':
        with open(filename, 'w') as f:
            f.write(np.array2string(arr))
    else:
        _io_.imsave(filename, arr)


def implot(filename, cmap='plasma', rescale=False):
    """Display an image in a window.

    Parameters
    ----------
    filename :  string
           the absolute path of the image file that is to be read.
    cmap : string
           specifies matplotlib colormap
    rescale : bool
           rescales intensities when set `True`
    """

    arr = imread(filename)
    if rescale:
        arr = rescale_intensity(arr, in_range=(0, arr.max()))

    fig, ax = plt.subplots()
    ax = imshow(arr, cmap=cmap)
    fig.show()
