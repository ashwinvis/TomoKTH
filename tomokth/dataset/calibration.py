""" Calibration data (:mod:`tomokth.dataset.calibration`)
=======================================================================

.. currentmodule:: tomokth.dataset.calibration

Provides
--------
.. autoclass:: CalibrationData
   :members:
      :private-members:

"""

from __future__ import print_function
import os
from glob import glob
from tomokth.operators.io import imread
from .base import DataBase


class CalibrationData(DataBase):
    """Contains the calibration data object and assosciated member functions."""

    def config(self, filename='calibration.h5'):
        """Configure defaults and initialize paths"""
        super(CalibrationData, self).config(filename)

    def _parse_image_path(self, path):
        filename = super(CalibrationData, self)._parse_image_path(path)
        zloc, camera = filename.split('mm_')
        dummy, camera_index = filename.split('mm_cam')
        return int(zloc), camera, int(camera_index)

    def create_h5(self):
        """Creates a HDF5 file with all calibration data in it"""
        list_of_images = glob(self.path + '/*.' + self.image_type)

        with self.open_h5('a') as f:
            for path in list_of_images:
                arr = imread(path)
                fname = os.path.basename(path)
                z_loc, camera, camera_index = self._parse_image_path(path)
                if camera not in f.keys():
                    grp = f.create_group(camera)
                    grp.attrs['cam'] = camera_index
                else:
                    grp = f[camera]

                try:
                    dset = grp.create_dataset(fname, data=arr)
                    dset.attrs['cam'] = camera_index
                    dset.attrs['z'] = z_loc
                except RuntimeError:
                    print('WARNING: Image dataset ' + fname + ' already exists in ' + self.h5file)
                    pass

        self.refresh_h5dict()

    def get_dset(self, camera, z_loc):
        """Returns a numpy array corresponding to a calibration image stored as a dataset in the HDF5 file.
        Array located by matching camera index and z-location.

        Parameters
        ----------
        camera : int
            Index of the camera

        z_loc : int
            z-location at with the calibration image was taken
        """
        return super(CalibrationData, self).get_dset(camera=camera,
                                                     z=z_loc)

    def save_camera_calibration(self, camera, calib_arr):
        with self.open_h5('a') as f:
            grp = self.get_camera_grp(camera, f)
            grp['calib'] = calib_arr

    def get_camera_calibration(self, camera):
        with self.open_h5() as f:
            grp = self.get_camera_grp(camera, f)
            return grp['calib'][...]
