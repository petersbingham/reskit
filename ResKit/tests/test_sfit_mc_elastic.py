import os
import sys
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

if os.path.isdir("test"):
    shutil.rmtree("test")

class parentTest(unittest.TestCase):
    def calculateQIs(self):
        cal = rk.getAsymCalc(cu.HARTs, [0,0])
        cSmat = rw.getSmatFun(1.0,2.0,2.0,cal,1.0)
        dSmat = cSmat.discretise(1.,8.,100)
        sfit_mc_elastic = rk.getTool(rk.SFIT_MC_ELASTIC, dSmat,
                                     resultsRoot="test")

        sfit_mc_elastic.getElasticSmat(6)
        cFins = sfit_mc_elastic.getElasticFins(range(2,10,2))
        sfit_mc_elastic.calculateQIs(cFins)

        self.assertFalse(sfit_mc_elastic.allCoeffsLoaded)
        self.assertFalse(sfit_mc_elastic.allRootsLoaded)
        cFins = sfit_mc_elastic.getElasticFins(range(2,10,2))
        self.assertTrue(sfit_mc_elastic.allCoeffsLoaded)
        self.assertFalse(sfit_mc_elastic.allRootsLoaded)
        sfit_mc_elastic.calculateQIs(cFins)
        self.assertTrue(sfit_mc_elastic.allRootsLoaded)

class test_numpy(parentTest):
    def runTest(self):
        rk.usePythonTypes()
        self.calculateQIs()

class test_mpmath(parentTest):
    def runTest(self):
        rk.useMpmathTypes()
        self.calculateQIs()

if __name__ == "__main__":
    #Just for debug
    b = test_numpy()
    b.runTest()
