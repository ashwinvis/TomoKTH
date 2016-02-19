""" Particle data (:mod:`tomokth.dataset.particle`)
=======================================================================

.. currentmodule:: tomokth.dataset.particle

Provides
--------
.. autoclass:: ParticleData
   :members:
      :private-members:

"""

from __future__ import print_function
import os
from glob import glob
from tomokth.operators.io import imread
from .base import DataBase


class ParticleData(DataBase):
    """Contains the particle data object and assosciated member functions."""

    def config(self, filename='particle.h5'):
        """Configure defaults and initialize paths"""
        super(ParticleData, self).config(filename)

    def _parse_image_path(self, path):
        filename = super(ParticleData, self)._parse_image_path(path)
        dummy, camera, snapshot = filename.split('_')
        camera_index = int(camera[-1:])
        ab = snapshot[0]
        time = int(snapshot[1:])
        time_str = 't=' + snapshot[1:]
        return camera, camera_index, ab, time, time_str

    def create_h5(self):
        """Creates a HDF5 file with all particle data in it"""
        list_of_images = glob(self.path + '/*.' + self.image_type)

        with self.open_h5('a') as f:
            for path in list_of_images:
                arr = imread(path)
                fname = os.path.basename(path)
                camera, camera_index, ab, time, time_str = self._parse_image_path(path)
                if time_str not in f.keys():
                    grp = f.create_group(time_str)
                    grp.attrs['t'] = time
                else:
                    grp = f[time_str]

                if camera not in grp.keys():
                    subgrp = grp.create_group(camera)
                    subgrp.attrs['t'] = time
                    subgrp.attrs['cam'] = camera_index
                else:
                    subgrp = grp[camera]

                try:
                    dset = subgrp.create_dataset(fname, data=arr)
                    dset.attrs['t'] = time
                    dset.attrs['cam'] = camera_index
                    dset.attrs['ab'] = ab
                except RuntimeError:
                    print('WARNING: Image dataset ' + fname + ' already exists in ' + self.h5file)
                    pass

        self.refresh_h5dict()

    def get_dset(self, camera, ab, time):
        """Returns a numpy array corresponding to a particle image stored as a dataset
        in the HDF5 file. Array located by matching the following parameters.

        Parameters
        ----------
        camera : int
            Index of the camera

        ab : str
            Acceptable values 'a' or 'b' denoting first or second snapshot

        time : int
            Time at which the snapshot was taken
        """
        return super(ParticleData, self).get_dset(camera=camera,
                                                  ab=ab,
                                                  t=time)

    def replace_dset(self, camera, ab, time, arr):
        pass
