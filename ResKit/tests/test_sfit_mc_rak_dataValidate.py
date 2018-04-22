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

TEST_ROOT = "test_sfit_mc_rak_dataValidate"
if os.path.isdir(TEST_ROOT):
    shutil.rmtree(TEST_ROOT)

class parentTest(unittest.TestCase):
    def findPoles(self):
        cal = rk.getAsymCalc(cu.HARTs, [0,0])
        cSmat = rw.getSmatFun(1.0,2.0,2.0,cal,1.0)
        dSmat = cSmat.discretise(1.,8.,100)

        rk.getTool(rk.SFIT_MC_RAK, dSmat, archiveRoot=TEST_ROOT, silent=True)
        rk.getTool(rk.SFIT_MC_RAK, dSmat, archiveRoot=TEST_ROOT, silent=True)
        
        dSmat.asymCal.units = cu.RYDs
        self.assertRaises(Exception, rk.getTool, rk.SFIT_MC_RAK, dSmat, 
                          archiveRoot=TEST_ROOT, silent=True)

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
