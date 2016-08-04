import os
import h5py


class DataBase(object):
    def __init__(self, path=None):
        """Initialize attributes"""

        self.path = path
        self.f = None
        self.h5file = None
        self.h5dict = dict()
        self.image_type = None

    def config(self, filename):
        """Configure defaults and initialize paths"""

        if self.path is None:
            self.path = os.getcwd()
        else:
            self.path = os.path.abspath(self.path)

        if self.h5file is None:
            self.h5file = filename

        self.h5file = os.path.join(self.path, self.h5file)
        if self.image_type is None:
            self.image_type = 'tif'

    def _parse_image_path(self, path):
        filename = os.path.basename(path)
        filename, ext = os.path.splitext(filename)
        return filename

    def open_h5(self, mode='r'):
        """Returns a h5py.File object"""
        if self.f is not None:
            self.f.close()

        self.f = h5py.File(self.h5file, mode)
        return self.f

    def create_h5(self):
        """Creates a HDF5 file with all data in it"""
        pass

    def refresh_h5dict(self):
        with self.open_h5() as f:
            for key in f['/'].keys():
                self.h5dict[key] = f[key].keys()

    def get_grp(self, **kwargs):
        """Returns a HDF5 group containing datasets of a particular camera.

        Parameters
        ----------
        kwargs : dict
            All attributes to be matched.

        """

        f = self.open_h5()

        for grp in f.values():
            match = True
            for attr_key, attr_value in kwargs.items():
                if grp.attrs[attr_key] != attr_value:
                    match = False

            if match:
                return grp

        if not match:
            raise ValueError('Cannot locate camera group in ' + self.h5file)

    def get_dset(self, camera, **kwargs):
        """Returns a numpy array corresponding to a calibration image stored as a dataset in the HDF5 file.
        Array located by matching all attribute keys and values.

        Parameters
        ----------
        camera : int
            Index of the camera

        kwargs : dict
            Key & value of attributes to match the dataset
        """

        grp = self.get_camera_grp(camera)
        for dset in grp.values():
            match = True
            for attr_key, attr_value in kwargs.items():
                if dset.attrs[attr_key] != attr_value:
                    match = False

            if match:
                return dset[...]

        raise ValueError('Cannot locate dataset in ' + self.h5file)
