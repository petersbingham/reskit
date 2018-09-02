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

class test(unittest.TestCase):
    def get_dsmat(self):
        cal = rk.get_asym_calc(cu.hartrees, [0,0])
        csmat = rw.get_Smat_fun(1.0,2.0,2.0,cal,1.0)
        return csmat.discretise(1.,8.,100)

    def get_roots(self, mcsmatfit):
        cFin = mcsmatfit.get_elastic_Fin(4)
        return mcsmatfit.find_Fin_roots([cFin])

    def runTest(self):
        # Test that the three modes (mpmath, python with and without sympy 
        # nroots) all return different results.
        dsmat = self.get_dsmat()
        rk.use_python_types()
        mcsmatfit = rk.get_tool(rk.mcsmatfit, dsmat, silent=True)
        roots1 = self.get_roots(mcsmatfit)
        mcsmatfit = rk.get_tool(rk.mcsmatfit, dsmat, silent=True,
                                param_file_path="test_mcsmatfit_calc_modes.yaml")
        roots2 = self.get_roots(mcsmatfit)
        rk.use_mpmath_types(dps=100)
        dsmat = self.get_dsmat()
        mcsmatfit = rk.get_tool(rk.mcsmatfit, dsmat, silent=True)
        roots3 = self.get_roots(mcsmatfit)

        self.assertNotEqual(str(roots1), str(roots2))
        self.assertNotEqual(str(roots1), str(roots3))
        self.assertNotEqual(str(roots2), str(roots3))

if __name__ == "__main__":
    #Just for debug
    b = test()
    b.runTest()
