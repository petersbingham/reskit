import os
import sys
fileDir = os.path.dirname(os.path.realpath(__file__))
rkPath = fileDir+'/../..'
sys.path.insert(0,rkPath)

import ResKit as rk
import channelutil as cu
import TwoChanRadialWell as rw

import unittest


class parentTest(unittest.TestCase):
    def calculateQIs(self):
        cal = cu.asymCal([0.,0.], units=cu.HARTs)
        cSmat = rw.getSmatFun(1.0,2.0,2.0,cal,1.0)
        dSmat = cSmat.discretise(1.,8.,100)
        sfit_mc_elastic = rk.getModule(rk.MOD_SFIT_MC_ELASTIC)
        
        sfit_mc_elastic.getElasticSmats(dSmat, range(2,6,2), cal)
        
        cFins = sfit_mc_elastic.getElasticFins(dSmat, range(2,20,2), cal)
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
    b = test_mpmath()
    b.runTest()
