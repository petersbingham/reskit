import os
import sys
fileDir = os.path.dirname(os.path.realpath(__file__))
rkPath = fileDir+'/../..'
sys.path.insert(0,rkPath)

import ResKit as rk
import channelutil as cu
import TwoChanRadialWell as rw
import pynumwrap as nw

import unittest
import shutil

class parentTest(unittest.TestCase):
    def calculateQIs(self):
        cal = rk.getAsymCalc(cu.HARTs, [0,0])
        cSmat = rw.getSmatFun(1.0,2.0,2.0,cal,1.0)
        dSmat = cSmat.discretise(1.,8.,100)
        sfit_mc_elastic = rk.getTool(rk.TOOL_SFIT_MC_ELASTIC, resultsRoot="test")

        sfit_mc_elastic.getElasticSmat(dSmat, 6)
        shutil.rmtree("test"+os.sep+nw.getConfigString())
        cFins = sfit_mc_elastic.getElasticFins(dSmat, range(2,20,2))
        return sfit_mc_elastic.calculateQIs(cFins)


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
