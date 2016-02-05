
from setuptools import setup, find_packages
import os
here = os.path.abspath(os.path.dirname(__file__))

import sys
if sys.version_info[:2] < (2, 6) or (3, 0) <= sys.version_info[0:2] < (3, 2):
    raise RuntimeError("Python version 2.6, 2.7 or >= 3.2 required.")

# Get the long description from the relevant file
with open(os.path.join(here, 'README.md')) as f:
    long_description = f.read()
lines = long_description.splitlines(True)
long_description = ''.join(lines[8:])

# Get the version from the relevant file
# execfile(here + '/tomokth/_version.py')
# Get the development status from the version string
'''
from pkg_resources import parse_version
parsed_version = parse_version(__version__)
try:
    if parsed_version.is_prerelease:
        if 'a' in __version__:
            devstatus = 'Development Status :: 3 - Alpha'
        else:
            devstatus = 'Development Status :: 4 - Beta'
    else:
        devstatus = 'Development Status :: 5 - Production/Stable'
except AttributeError:
    if 'a' in __version__:
        devstatus = 'Development Status :: 3 - Alpha'
    elif 'b' in __version__:
        devstatus = 'Development Status :: 4 - Beta'
    else:
        devstatus = 'Development Status :: 5 - Production/Stable'
'''
setup(name='tomokth',
#      version=__version__,
      description=('PIV code'),
      long_description=long_description,
      keywords='PIV',
      author='Ashwin Krishna Mubashir',
      author_email='avmo@kth.se',
      license='GPL',
      install_requires=['numpy', 'matplotlib']
      )
