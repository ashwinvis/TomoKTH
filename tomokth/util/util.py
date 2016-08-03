"""
Miscellaneous utilities
=======================

"""
from __future__ import print_function

import sys
import six
from logging import getLogger
from fluiddyn.util import config_logging as _cl_fluiddyn


logger = getLogger('tomokth')


def config_logging(level='info', name='tomokth', file=None):
    _cl_fluiddyn(level=level, name=name, file=file)


def raise_exception(exc, msg=''):
    '''Raise an exception with a custom message
    cf. http://python-future.org/compatible_idioms.html

    '''
    traceback = sys.exc_info()[2]
    six.reraise(type(exc), msg, traceback)
