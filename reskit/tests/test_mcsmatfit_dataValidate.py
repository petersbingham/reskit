import os
import sys
fileDir = os.path.dirname(os.path.realpath(__file__))
rkPath = fileDir+'/../..'
sys.path.insert(0,rkPath)

import reskit as rk
rk.safeMode = False
import channelutil as cu
import twochanradialwell as rw

import unittest
import shutil

TEST_ROOT = "test_mcsmatfit_dataValidate"
if os.path.isdir(TEST_ROOT):
    shutil.rmtree(TEST_ROOT)

class parentTest(unittest.TestCase):
    def findStableSmatPoles(self):
        cal = rk.getAsymCalc(cu.HARTs, [0,0])
        csmat = rw.getSmatFun(1.0,2.0,2.0,cal,1.0)
        dsmat = csmat.discretise(1.,8.,100)

        rk.getTool(rk.SFIT_MC_RAK, dsmat, archiveRoot=TEST_ROOT, silent=True)
        rk.getTool(rk.SFIT_MC_RAK, dsmat, archiveRoot=TEST_ROOT, silent=True)
        
        dsmat.asymcalc.units = cu.RYDs
        self.assertRaises(Exception, rk.getTool, rk.SFIT_MC_RAK, dsmat, 
                          archiveRoot=TEST_ROOT, silent=True)

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
    b = test_numpy()
    b.runTest()
