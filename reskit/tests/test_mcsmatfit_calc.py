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

TEST_ROOT = "test_mcsmatfit_calc"
if os.path.isdir(TEST_ROOT):
    shutil.rmtree(TEST_ROOT)

class parentTest(unittest.TestCase):
    def find_stable_Smat_poles(self):
        cal = rk.get_asym_calc(cu.HARTs, [0,0])
        csmat = rw.get_Smat_fun(1.0,2.0,2.0,cal,1.0)
        dsmat = csmat.discretise(1.,8.,100)
        mcsmatfit = rk.get_tool(rk.mcsmatfit, dsmat, archive_root=TEST_ROOT,
                               silent=True)

        mcsmatfit.get_elastic_Smat(6)

        cfins = mcsmatfit.get_elastic_Fins(range(2,10,2))
        mcsmatfit.find_stable_Smat_poles(cfins)
        self.assertFalse(mcsmatfit.allCoeffsLoaded)
        self.assertFalse(mcsmatfit.allRootsLoaded)

        cfins = mcsmatfit.get_elastic_Fins(range(2,10,2))
        self.assertTrue(mcsmatfit.allCoeffsLoaded)
        # False because we haven't called find_stable_Smat_poles yet
        self.assertFalse(mcsmatfit.allRootsLoaded)

        roots = mcsmatfit.find_Fin_roots(cfins)
        mcsmatfit.find_stable_Smat_poles(roots)
        self.assertTrue(mcsmatfit.allRootsLoaded)

class test_numpy(parentTest):
    def runTest(self):
        rk.use_python_types()
        self.find_stable_Smat_poles()

class test_mpmath(parentTest):
    def runTest(self):
        rk.use_mpmath_types()
        self.find_stable_Smat_poles()

if __name__ == "__main__":
    #Just for debug
    b = test_mpmath()
    b.runTest()
