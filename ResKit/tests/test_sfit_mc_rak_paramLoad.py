import os
import sys
fileDir = os.path.dirname(os.path.realpath(__file__))
rkPath = fileDir+'/../..'
sys.path.insert(0,rkPath)

import ResKit as rk
rk.safeMode = False
import channelutil as cu
import TwoChanRadialWell as rw

import unittest
import shutil

TEST_ROOT = "test_sfit_mc_rak_config"
if os.path.isdir(TEST_ROOT):
    shutil.rmtree(TEST_ROOT)

class parentTest(unittest.TestCase):
    def findPoles(self):
        cal = rk.getAsymCalc(cu.HARTs, [0,0])
        cSmat = rw.getSmatFun(1.0,2.0,2.0,cal,1.0)
        dSmat = cSmat.discretise(1.,8.,100)

        sfit_mc_rak = rk.getTool(rk.SFIT_MC_RAK, dSmat, resultsRoot=TEST_ROOT,
                                 silent=True)
        cFins = sfit_mc_rak.getElasticFins(range(2,4,2))
        sfit_mc_rak.findPoles(cFins)

        # Import again with same config and check no exception
        rk.getTool(rk.SFIT_MC_RAK, dSmat, resultsRoot=TEST_ROOT, silent=True)

        testPath = fileDir+os.sep+"test_sfit_mc_rak_data1"+os.sep
        testPath += "changedRoots.yml"
        sfit_mc_rak = rk.getTool(rk.SFIT_MC_RAK, dSmat, resultsRoot=TEST_ROOT,
                                 paramFilePath=testPath, silent=True)
        cFins = sfit_mc_rak.getElasticFins(range(2,4,2))
        sfit_mc_rak.findRoots(cFins)
        self.assertTrue(sfit_mc_rak.allCoeffsLoaded)
        self.assertFalse(sfit_mc_rak.allRootsLoaded)

        testPath = fileDir+os.sep+"test_sfit_mc_rak_data2"+os.sep
        testPath += "changedPoles.yml"
        sfit_mc_rak = rk.getTool(rk.SFIT_MC_RAK, dSmat, resultsRoot=TEST_ROOT,
                                 paramFilePath=testPath, silent=True)
        cFins = sfit_mc_rak.getElasticFins(range(2,4,2))
        sfit_mc_rak.findRoots(cFins)
        self.assertTrue(sfit_mc_rak.allCoeffsLoaded)
        self.assertTrue(sfit_mc_rak.allRootsLoaded)

class test_numpy(parentTest):
    def runTest(self):
        rk.usePythonTypes()
        self.findPoles()

class test_mpmath(parentTest):
    def runTest(self):
        rk.useMpmathTypes()
        self.findPoles()

if __name__ == "__main__":
    #Just for debug
    b = test_numpy()
    b.runTest()
