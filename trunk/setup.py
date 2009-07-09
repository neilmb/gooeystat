# Copyright (C) 2008, 2009  Spencer Herzberg <spencer.herzberg@gmail.com>

# This file is part of GooeyStat

# GooeyStat is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from setuptools import setup
setup(name = 'GooeyStat',
      version = '0.1',
      description = 'A python statistical gui application',
      long_description = """
GooeyStat is an application for basic statistical analysis.  It started as a
student project in a Statistical Methods course at `Wartburg College`_.  The
goal is to have a Open Source, cross-platform program for doing the
calculations of an introductory statistics class.

.. _`Wartburg College`: http://www.wartburg.edu
""",

      author = 'Spencer Herzberg',
      author_email = 'spencer.herzberg@gmail.com',
      url = 'http://code.google.com/p/mathapp',
      install_requires = ['scipy',
                          'setuptools',
                          #'PyQt4 >= 4.0',
                         ],
      scripts = ['GooeyStat'],
      packages = ['gooeylib',
                  'gooeylib.plugins',
                  'gooeylib.plugins.helpers',
                 ],
      package_data = {'gooeylib' : ['icons/*.png',
                                    'splash.png',
                                    'hline.png',
                                   ],
                     },
      data_files = [('share/GooeyStat/examples', ['examples/loader.gef'])],

      classifiers = ['Development Status :: 2 - Pre-Alpha',
                     'Intended Audience :: Education',
                     'License :: OSI Approved :: GNU General Public License (GPL)',
                     'Topic :: Scientific/Engineering :: Mathematics',
                    ],
      platforms = "Any",
      license = "GPLv3"
     )


