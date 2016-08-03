"""Preprocess base (:mod:`tomokth.preprocess.base`)
====================================================
To preprocess series of images.

.. currentmodule:: tomokth.preprocess.base

Provides:

.. autoclass:: PreprocBase
   :members:
   :private-members:

"""
import os

from fluiddyn.util.paramcontainer import ParamContainer
from fluiddyn.util.serieofarrays import SerieOfArraysFromFiles
from .toolbox import PreprocTools
# TODO: Replace with `from fluidimage.pre_proc import PreprocTools` when PyPi is updated


class PreprocBase(object):
    """Preprocess series of images with various tools. """

    @classmethod
    def create_default_params(cls):
        """Class method returning the default parameters."""
        params = ParamContainer(tag='params')
        params._set_child('preproc')
        params.preproc._set_child('series', attribs={'path': ''})

        PreprocTools._complete_class_with_tools(params)

        return params

    def __init__(self, params=None):
        """Set path for results and loads images as SerieOfArraysFromFiles."""
        if params is None:
            params = self.__class__.create_default_params()

        self.params = params.preproc

        path = params.preproc.series.path
        if not os.path.exists(path):
            path = params.preproc.series.path = os.path.expandvars(path)

        self.serie_arrays = SerieOfArraysFromFiles(path)
        self.tools = PreprocTools(params)
        self.results = {}

    def __call__(self):
        """Apply all enabled preprocessing tools on the series of arrays
        and saves them in self.results.

        """
        name_files = self.serie_arrays.get_name_files()
        for i, img in enumerate(self.serie_arrays.iter_arrays()):
            name = name_files[i]
            self.results[name] = self.tools(img)
