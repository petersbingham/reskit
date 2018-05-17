# -*- coding: utf-8 -*-

from distutils.core import setup

setup(name='reskit',
      version='0.34',
      description='Python Package to assist with the identification and characterisation of quantum scattering resonances.',
      author="Peter Bingham",
      author_email="petersbingham@hotmail.co.uk",
      packages=['reskit'],
      package_data={'reskit': ['utilities/get.sh',
                               'tools/toolhelper.py',
                               'tools/chart/__init__.py',
                               'tools/chart/default.yml',
                               'tools/mcsmatfit/__init__.py',
                               'tools/mcsmatfit/default.yml',
                               'tests/*.py',
                               'tests/test_mcsmatfit_data1/changedRoots.yml',
                               'tests/test_mcsmatfit_data1/default.yml',
                               'tests/test_mcsmatfit_data2/changedPoles.yml',
                               'tests/test_mcsmatfit_data2/default.yml']}
     )
