# -*- coding: utf-8 -*-

from distutils.core import setup
import os

dir_setup = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(dir_setup, 'reskit', 'release.py')) as f:
    # Defines __version__
    exec(f.read())

setup(name='reskit',
      version=__version__,
      description='Python Package to assist with the identification and characterisation of quantum scattering resonances.',
      author="Peter Bingham",
      author_email="petersbingham@hotmail.co.uk",
      packages=['reskit'],
      package_data={'reskit': ['site-packages/get-utilities.sh',
                               'tools/toolhelper.py',
                               'tools/chart/__init__.py',
                               'tools/chart/default.yaml',
                               'tools/mcsmatfit/__init__.py',
                               'tools/mcsmatfit/default.yaml',
                               'tests/*.py',
                               'tests/test_mcsmatfit_data1/changedRoots.yaml',
                               'tests/test_mcsmatfit_data1/default.yaml',
                               'tests/test_mcsmatfit_data2/changedPoles.yaml',
                               'tests/test_mcsmatfit_data2/default.yaml',
                               'utilities/channelutil/*.py',
                               'utilities/matfuncutil/*.py',
                               'utilities/parsmat/*.py',
                               'utilities/pynumutil/*.py',
                               'utilities/pynumwrap/*.py',
                               'utilities/stelempy/*.py',
                               'utilities/tisutil/*.py',
                               'utilities/twochanradialwell/*.py',
                               'utilities/ukrmolmatreader/*.py']}
     )
