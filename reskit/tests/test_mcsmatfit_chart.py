import os
import sys
from base64 import test
fileDir = os.path.dirname(os.path.realpath(__file__))
rkPath = fileDir+'/../..'
sys.path.insert(0,rkPath)

import reskit as rk
rk.safeMode = False
import channelutil as cu
import twochanradialwell as rw
import pynumwrap as nw

import unittest
import shutil

TEST_ROOT = "test_mcsmatfit_chart"
if os.path.isdir(TEST_ROOT):
    shutil.rmtree(TEST_ROOT)

class parent_test(unittest.TestCase):
    def charts(self):
        cal = rk.get_asym_calc(cu.hartrees, [0,0])
        csmat = rw.get_Smat_fun(1.0,2.0,2.0,cal,1.0)
        dsmat = csmat.discretise(1.,8.,100)
        mcsmatfit = rk.get_tool(rk.mcsmatfit, dsmat, archive_root=TEST_ROOT,
                               silent=True)

        cfin = mcsmatfit.get_elastic_Fin(6)
        csmat = mcsmatfit.get_elastic_Smat(6)
        
        chart = rk.get_tool(rk.chart, cfin, archive_root=TEST_ROOT, silent=True)
        chart.plot_raw(show=False)
        chart = rk.get_tool(rk.chart, csmat, archive_root=TEST_ROOT, silent=True)
        chart.plot_Smatrix(show=False)

class test_numpy(parent_test):
    def runTest(self):
        rk.use_python_types()
        self.charts()

class test_mpmath(parent_test):
    def runTest(self):
        rk.use_mpmath_types()
        self.charts()

if __name__ == "__main__":
    #Just for debug
    b = test_mpmath()
    b.runTest()
