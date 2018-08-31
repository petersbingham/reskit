import os
import sys
from base64 import test
fileDir = os.path.dirname(os.path.realpath(__file__))
rkPath = fileDir+'/../../..'
sys.path.insert(0,rkPath)

import reskit as rk
rk.safeMode = False
import channelutil as cu
import twochanradialwell as rw
import pynumwrap as nw

import unittest
import shutil

TEST_ROOT = "test_mcsmatfit_calc"
if os.path.isdir(TEST_ROOT):
    shutil.rmtree(TEST_ROOT)

class parent_test(unittest.TestCase):
    def find_stable_Smat_poles(self):
        # Test that the (previously determined) correct number poles returned
        # for the different modes.
        cal = rk.get_asym_calc(cu.hartrees, [0,0])
        csmat = rw.get_Smat_fun(1.0,2.0,2.0,cal,1.0)
        dsmat = csmat.discretise(1.,8.,100)
        mcsmatfit = rk.get_tool(rk.mcsmatfit, dsmat, archive_root=TEST_ROOT,
                               silent=True)

class test_numpy(parent_test):
    def runTest(self):
        rk.use_python_types()
        self.find_stable_Smat_poles()

class test_mpmath(parent_test):
    def runTest(self):
        rk.use_mpmath_types()
        self.find_stable_Smat_poles()

if __name__ == "__main__":
    #Just for debug
    b = test_mpmath()
    b.runTest()
