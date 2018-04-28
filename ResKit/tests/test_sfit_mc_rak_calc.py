import os
import sys
from base64 import test
fileDir = os.path.dirname(os.path.realpath(__file__))
rkPath = fileDir+'/../..'
sys.path.insert(0,rkPath)

import ResKit as rk
rk.safeMode = False
import channelutil as cu
import TwoChanRadialWell as rw
import pynumwrap as nw

import unittest
import shutil

TEST_ROOT = "test_sfit_mc_rak_calc"
if os.path.isdir(TEST_ROOT):
    shutil.rmtree(TEST_ROOT)

class parentTest(unittest.TestCase):
    def findStableSmatPoles(self):
        cal = rk.getAsymCalc(cu.HARTs, [0,0])
        csmat = rw.getSmatFun(1.0,2.0,2.0,cal,1.0)
        dsmat = csmat.discretise(1.,8.,100)
        sfit_mc_rak = rk.getTool(rk.SFIT_MC_RAK, dsmat, archiveRoot=TEST_ROOT,
                                 silent=True)

        sfit_mc_rak.getElasticSmat(6)

        cfins = sfit_mc_rak.getElasticFins(range(2,10,2))
        sfit_mc_rak.findStableSmatPoles(cfins)
        self.assertFalse(sfit_mc_rak.allCoeffsLoaded)
        self.assertFalse(sfit_mc_rak.allRootsLoaded)

        cfins = sfit_mc_rak.getElasticFins(range(2,10,2))
        self.assertTrue(sfit_mc_rak.allCoeffsLoaded)
        # False because we haven't called findStableSmatPoles yet
        self.assertFalse(sfit_mc_rak.allRootsLoaded)

        roots = sfit_mc_rak.findFinRoots(cfins)
        sfit_mc_rak.findStableSmatPoles(roots)
        self.assertTrue(sfit_mc_rak.allRootsLoaded)

class test_numpy(parentTest):
    def runTest(self):
        rk.usePythonTypes()
        self.findStableSmatPoles()

class test_mpmath(parentTest):
    def runTest(self):
        rk.useMpmathTypes()
        self.findStableSmatPoles()

if __name__ == "__main__":
    #Just for debug
    b = test_mpmath()
    b.runTest()
