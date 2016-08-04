import os
import pymatbridge
import numpy as np
from skimage.transform import hough_circle
from skimage.feature import peak_local_max, canny
from tomokth.dataset.calibration import CalibrationData


_here = os.path.abspath(os.path.dirname(__file__))


class CalibrPy(object):
    '''Python interface to use Camera calibration toolbox for MATLAB/Octave'''

    @classmethod
    def centers_radii(cls, img):
        centers = []
        accums = []
        radii = []

        edges = canny(img, sigma=3.)
        # Detect two radii
        hough_radii = np.arange(15, 30, 2)
        hough_res = hough_circle(edges, hough_radii)
        for radius, h in zip(hough_radii, hough_res):
            # For each radius, extract two circles
            num_peaks = 2
            peaks = peak_local_max(h, num_peaks=num_peaks)
            centers.extend(peaks)
            accums.extend(h[peaks[:, 0], peaks[:, 1]])
            radii.extend([radius] * num_peaks)

        return centers, radii, edges

    def __init__(self, cdata, camera_nb=0, camera_type='tomokth'):
        """Initializes a MATLAB/Octave session and other parameters"""

        self.path = os.path.join(_here, '_calibr')
        try:
            self.pymat = pymatbridge.Matlab()
            self.pylab.start()
        except:
            self.pymat = pymatbridge.Octave()
            self.pymat.start()

        self.pymat.run_code('addpath({})'.format(self.path))

        if isinstance(cdata, CalibrationData):
            self.cdata = cdata
        else:
            raise ValueError('data must be an instance of CalibrationData')

        self.camera_nb = camera_nb
        self.camera_type = camera_type

    def prepare_input(self):
        """Prepares input for cacal.m function"""

        cam = self.camera_nb
        z = range(-6, 6, 3)
        img = [self.cdata.get_dset(cam, z_loc) for z_loc in z]

        data = [self.prepare_winxyz(z[i], img[i]) for i in range(5)]

        dico = {'name': self.camera_type}
        dico.update({'data' + str(i + 1): data[i] for i in range(5)})
        return dico

    def prepare_winxyz(self, z, img):
        """Returns world coordinates, image coordinates and normal vectors of a calibration image"""
        wxy, ixy = self.get_control_pts(img)
        wz = z * np.ones(wxy.shape)
        nx, ny, nz = (0, 0, 1)
        return wxy[0], wxy[2], wz, ixy[0], ixy[1], nx, ny, nz

    def get_control_pts(self, img):
        c, r = self.centers_radii(img)

    def calibrate(self):
        data_in = self.prepare_input()
        data_out = self.pymat.run_func('cacal.m', data_in)
        return data_out
