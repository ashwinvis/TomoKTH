# TomoKTH
Tomographic PIV code done as a part of a KTH course

### Resources
Images available as a [zip archive](http://www.mech.kth.se/~ramis/PIV2016/Assignment%20material.zip)
Do not upload the images or any binary files! They can increase the size of the repositories.
Save the files under the following path & it will be ignored by git. (Maybe an unnecessary detail, but for the sake of consistency)
- examples/assignment/calibration_images/
- examples/assignment/particle_images/

### Tasks to do / Assignee
- [ ] Image loading / jadelord
- [ ] Dewarping
- [ ] Calibration
- [ ] Statistics: Image density calculation, PDF of intensities
- [ ] Preprocessing: Threshold, sliding minima, Gaussian smoothing
- [ ] MLOS
- [ ] Outlier or bad vector removal

### Resources
* OpenPIV: for [python](https://github.com/OpenPIV/openpiv-python) and [MATLAB](https://github.com/OpenPIV/openpiv-matlab)
* LEGI UVmat: [matlab code](http://servforge.legi.grenoble-inp.fr/projects/soft-uvmat) and [tutorial](http://servforge.legi.grenoble-inp.fr/projects/soft-uvmat/wiki/Tutorial)
* Image handling: [pillow](https://pypi.python.org/pypi/Pillow/3.1.0), [scikit-image](https://pypi.python.org/pypi/scikit-image/0.11.3), [opencv](http://docs.opencv.org/3.1.0/)
* Plotting: [matplotlib](http://matplotlib.org/gallery.html), [MayaVi](http://docs.enthought.com/mayavi/mayavi/auto/examples.html#example-gallery)
