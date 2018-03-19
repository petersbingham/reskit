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
        dmat = rk.initFromDiscreteData(rk.mat_type_S, data, rk.RYDs)
        self.assertEqual(dmat.getTypeMode(), nw.mode_python)
        self.assertEqual(dmat.getTypeDps(), nw.dps_default_python)
        nw.usePythonTypes()
        for mat in dmat.values():
            nw.shape(mat) # Will get an exception if types are wrong.

class test_mpmathDiscreteInit(unittest.TestCase):
    def runTest(self):
        data = {}
        data[1.] = mpmath.matrix([[1.,1.],[1.,1.]])
        data[2.] = mpmath.matrix([[2.,2.],[2.,2.]])
        dmat = rk.initFromDiscreteData(rk.mat_type_S, data, rk.RYDs,
                                       rk.type_mode_mpmath)
        self.assertEqual(dmat.getTypeMode(), nw.mode_mpmath)
        self.assertEqual(dmat.getTypeDps(), nw.dps_default_mpmath)
        nw.useMpmathTypes()
        for mat in dmat.values():
            nw.shape(mat) # Will get an exception if types are wrong.

class test_numpyContinuousInit(unittest.TestCase):
    def runTest(self):
        fp = lambda e: np.matrix([[e,e],[e,e]], dtype=np.complex128)
        dmat = rk.initFromContinuousData(rk.mat_type_S, fp, rk.RYDs,
                                         1.,5.,10)
        self.assertEqual(dmat.getTypeMode(), nw.mode_python)
        self.assertEqual(dmat.getTypeDps(), nw.dps_default_python)
        nw.usePythonTypes()
        for mat in dmat.values():
            nw.shape(mat) # Will get an exception if types are wrong.

class test_mpmathContinuousInit(unittest.TestCase):
    def runTest(self):
        fp = lambda e: mpmath.matrix([[e,e],[e,e]])
        dmat = rk.initFromContinuousData(rk.mat_type_S, fp, rk.RYDs,
                                         1.,5.,10, rk.type_mode_mpmath)
        self.assertEqual(dmat.getTypeMode(), nw.mode_mpmath)
        self.assertEqual(dmat.getTypeDps(), nw.dps_default_mpmath)
        nw.useMpmathTypes()
        for mat in dmat.values():
            nw.shape(mat) # Will get an exception if types are wrong.

if __name__ == "__main__":
    #Just for debug
    b = test_mpmathDiscreteInit()
    b.runTest()
