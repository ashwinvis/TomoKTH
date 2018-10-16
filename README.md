# TomoKTH
![](http://unmaintained.tech/badge.svg)

**See [FluidImage](fluidimage.readthedocs.io) for a working implementation of [camera calibration](https://fluidimage.readthedocs.io/en/latest/ipynb/tuto_opencv_calibration.html) and [reconstruction](https://fluidimage.readthedocs.io/en/latest/ipynb/tuto_opencv_tomo_reconstruct.html).**

Tomographic PIV code done as a part of a KTH course


### Installation
To install in development mode.
```bash
$ python setup.py develop
```

It may be a good idea to setup a virtual environment (virtualenv command for Linux and Anaconda for Windows), so that you don't clutter the root of your system. A quick tutorial can be found on that [here](http://docs.python-guide.org/en/latest/dev/virtualenvs/).

To install dependencies (for eg: numpy, matplotlib, etc.) in Linux
```bash
$ pip search <package>
$ pip install <package>
```
Anaconda users can find similar instructions [here](http://conda.pydata.org/docs/using/pkgs.html#install-a-package).


### Resources
Images available as a [zip archive from KTH](http://www.mech.kth.se/~ramis/PIV2016/Assignment%20material.zip).
Do not upload the images or any binary files! They can increase the size of the repositories.
Save the files under the following path & it will be ignored by git. (Maybe an unnecessary detail, but for the sake of consistency)
- examples/assignment/calibration_images/
- examples/assignment/particle_images/

### Tasks to do / Assignee
- [x] Image loading / jadelord
- [x] Classes for storing calibration and particle datasets / jadelord
- [ ] Calibration / mubasharkhan
- [x] Preprocessing: Threshold, sliding minima, Gaussian smoothing / jadelord
- [ ] Class for storing voxel and velocity vector datasets / jadelord
- [ ] Operators for tomo reconstruction: MLOS/MART/SMART
- [ ] Operators for 3D PIV: single pass cross-correlation

#### Future
- [ ] Outlier or bad vector removal
- [ ] Statistics: Image density calculation, PDF of intensities ()

### External Resources
* Learn Python: [Codecademy](https://www.codecademy.com/en/) or [tutorial in official Python documentation](https://docs.python.org/2/tutorial/index.html).
* OpenPIV: for [Python](https://github.com/OpenPIV/openpiv-python) and [MATLAB](https://github.com/OpenPIV/openpiv-matlab)
* LEGI UVmat: [MATLAB code](http://servforge.legi.grenoble-inp.fr/projects/soft-uvmat) and [tutorial](http://servforge.legi.grenoble-inp.fr/projects/soft-uvmat/wiki/Tutorial)
* Image handling: [pillow](https://pypi.python.org/pypi/Pillow/3.1.0), [scikit-image](https://pypi.python.org/pypi/scikit-image/0.11.3), [opencv](http://docs.opencv.org/3.1.0/)
* Plotting: [matplotlib](http://matplotlib.org/gallery.html), [MayaVi](http://docs.enthought.com/mayavi/mayavi/auto/examples.html#example-gallery)
* Data structures: [h5py](http://docs.h5py.org/en/latest/quick.html)
* Ships-project: [TomoRecon, TomoSim etc. in Google Code](http://ships-project.googlecode.com/svn/trunk/tomo/)
* Cernlib: Cylinder-Sphere intersection [docs](http://dollywood.itp.tuwien.ac.at/cernlib/shortwrupsdir/v700/top.html), [code](http://cernlib.web.cern.ch/cernlib/download/2006_source/src/mathlib/gen/v/)
