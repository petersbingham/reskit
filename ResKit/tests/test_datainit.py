import os
import sys
fileDir = os.path.dirname(os.path.realpath(__file__))
rkPath = fileDir+'/../..'
sys.path.insert(0,rkPath)

import pynumwrap as nw
import ResKit as rk
import numpy as np
import mpmath

import unittest

class test_numpyDiscreteInit(unittest.TestCase):
    def runTest(self):
        data = {}
        data[1.] = np.matrix([[1.,1.],[1.,1.]], dtype=np.complex128)
        data[2.] = np.matrix([[2.,2.],[2.,2.]], dtype=np.complex128)
        rk.usePythonTypes()
        dmat = rk.initFromDiscreteData(rk.mat_type_S, data, rk.RYDs)
        self.assertEqual(nw.mode, nw.mode_python)
        self.assertEqual(nw.dps, nw.dps_default_python)
        for mat in dmat.values():
            nw.shape(mat) # Will get an exception if types are wrong.

class test_mpmathDiscreteInit(unittest.TestCase):
    def runTest(self):
        data = {}
        data[1.] = mpmath.matrix([[1.,1.],[1.,1.]])
        data[2.] = mpmath.matrix([[2.,2.],[2.,2.]])
        rk.useMpmathTypes()
        dmat = rk.initFromDiscreteData(rk.mat_type_S, data, rk.RYDs)
        self.assertEqual(nw.mode, nw.mode_mpmath)
        self.assertEqual(nw.dps, nw.dps_default_mpmath)
        for mat in dmat.values():
            nw.shape(mat) # Will get an exception if types are wrong.

class test_numpyContinuousInit(unittest.TestCase):
    def runTest(self):
        fp = lambda e: np.matrix([[e,e],[e,e]], dtype=np.complex128)
        rk.usePythonTypes()
        dmat = rk.initFromContinuousData(rk.mat_type_S, fp, rk.RYDs, 1.,5.,10)
        self.assertEqual(nw.mode, nw.mode_python)
        self.assertEqual(nw.dps, nw.dps_default_python)
        for mat in dmat.values():
            nw.shape(mat) # Will get an exception if types are wrong.

class test_mpmathContinuousInit(unittest.TestCase):
    def runTest(self):
        fp = lambda e: mpmath.matrix([[e,e],[e,e]])
        rk.useMpmathTypes()
        dmat = rk.initFromContinuousData(rk.mat_type_S, fp, rk.RYDs,1.,5.,10)
        self.assertEqual(nw.mode, nw.mode_mpmath)
        self.assertEqual(nw.dps, nw.dps_default_mpmath)
        for mat in dmat.values():
            nw.shape(mat) # Will get an exception if types are wrong.

if __name__ == "__main__":
    #Just for debug
    b = test_mpmathDiscreteInit()
    b.runTest()
