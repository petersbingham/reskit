# -*- coding: utf-8 -*-

from distutils.core import setup

setup(name='ResKit',
      version='0.23',
      description='Python Package to assist with the identification and characterisation of quantum scattering resonances.',
      author="Peter Bingham",
      author_email="petersbingham@hotmail.co.uk",
      packages=['ResKit'],
      package_data={'ResKit': ['utilities/get.sh',
                               'tools/toolhelper.py',
                               'tools/chart/__init__.py',
                               'tools/chart/default.yml',
                               'tools/sfit_mc_rak/__init__.py',
                               'tools/sfit_mc_rak/default.yml',
                               'tests/*.py',
                               'tests/test_sfit_mc_rak_data1/changedRoots.yml',
                               'tests/test_sfit_mc_rak_data1/default.yml',
                               'tests/test_sfit_mc_rak_data2/changedPoles.yml',
                               'tests/test_sfit_mc_rak_data2/default.yml']}
     )
