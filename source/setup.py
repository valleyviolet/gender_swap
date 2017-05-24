"""
py2app/py2exe build script for the gender_swap program.

Will automatically ensure that all build prerequisites are available
via ez_setup

 Usage (Mac OS X):
     python setup.py py2app

 Usage (Windows):
     python setup.py py2exe


Copyright Eva Schiffer 2015

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

"""
Note: I've moved to packaging this using PyInstaller. The build command is:
    PyInstaller -w --onefile ./gender_swap.py
(run in the gender_swap source directory)

The -w option is the one that gets rid of the console, I'd rather not do that,
because my message passing isn't sufficiently set up yet. So for now let's use
this command to build instead:
    PyInstaller --onefile ./gender_swap.py
(run in the gender_swap source directory)
"""

import sys
import ez_setup
ez_setup.use_setuptools()

#import sys
from setuptools import setup, find_packages

mainscript = 'gender_swap.py'

if sys.platform == 'darwin':
    extra_options = dict(
                            setup_requires=['py2app'],
                            app=[mainscript],
                            # Cross-platform applications generally expect sys.argv to
                            # be used for opening files.
                            options=dict(py2app=dict(extension='.app',argv_emulation=True)),
                        )
elif sys.platform == 'win32':
    extra_options = dict(
                            setup_requires=['py2exe'],
                            app=[mainscript],
                        )
else:
     extra_options = dict(
                             # Normally unix-like platforms will use "setup.py install"
                             # and install the main script as such
                             scripts=[mainscript],
                         )

setup(
    name="Gender Swap Tool",
    version="0.6",
    zip_safe = True,
    entry_points = { 'console_scripts': [ 'gender_swap = gender_swap:main' ] },
    packages = find_packages('.'),
    install_requires = [ ], #'PyQt4', ],
    package_data = {'': ['*.txt', '*.png', ]},
    **extra_options
)
