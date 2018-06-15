import os
import sys
fileDir = os.path.dirname(os.path.realpath(__file__))
rkPath = fileDir+'/../..'
sys.path.insert(0,rkPath)

import reskit as rk
import channelutil as cu
import pynumwrap as nw
rk.safeMode = False
import numpy as np
import mpmath

import unittest

class test_numpy_discrete_init(unittest.TestCase):
    def runTest(self):
        data = {}
        data[1.] = np.matrix([[1.,1.],[1.,1.]], dtype=np.complex128)
        data[2.] = np.matrix([[2.,2.],[2.,2.]], dtype=np.complex128)
        rk.use_python_types()
        cal = rk.get_asym_calc(cu.rydbergs, [0,0])
        dmat = rk.get_dmat_from_discrete(rk.Smat, data, cal, "dum1")
        self.assertEqual(nw.mode, nw.mode_python)
        self.assertEqual(nw.dps, nw.dps_default_python)
        for mat in dmat.values():
            nw.shape(mat) # Will get an exception if types are wrong.

class test_mpmath_discrete_init(unittest.TestCase):
    def runTest(self):
        data = {}
        data[1.] = mpmath.matrix([[1.,1.],[1.,1.]])
        data[2.] = mpmath.matrix([[2.,2.],[2.,2.]])
        rk.use_mpmath_types()
        cal = rk.get_asym_calc(cu.rydbergs, [0,0])
        dmat = rk.get_dmat_from_discrete(rk.Smat, data, cal, "dum2")
        self.assertEqual(nw.mode, nw.mode_mpmath)
        self.assertEqual(nw.dps, nw.dps_default_mpmath)
        for mat in dmat.values():
            nw.shape(mat) # Will get an exception if types are wrong.

class test_numpy_continuous_init(unittest.TestCase):
    def runTest(self):
        fp = lambda e: np.matrix([[e,e],[e,e]], dtype=np.complex128)
        rk.use_python_types()
        cal = rk.get_asym_calc(cu.rydbergs, [0,0])
        dmat = rk.get_dmat_from_continuous(rk.Smat, fp, cal, 1.,5.,10, "dum3")
        self.assertEqual(nw.mode, nw.mode_python)
        self.assertEqual(nw.dps, nw.dps_default_python)
        for mat in dmat.values():
            nw.shape(mat) # Will get an exception if types are wrong.

class test_mpmath_continuous_init(unittest.TestCase):
    def runTest(self):
        fp = lambda e: mpmath.matrix([[e,e],[e,e]])
        rk.use_mpmath_types()
        cal = rk.get_asym_calc(cu.rydbergs, [0,0])
        dmat = rk.get_dmat_from_continuous(rk.Smat, fp, cal, 1., 5., 10, "dum4")
        self.assertEqual(nw.mode, nw.mode_mpmath)
        self.assertEqual(nw.dps, nw.dps_default_mpmath)
        for mat in dmat.values():
            nw.shape(mat) # Will get an exception if types are wrong.

if __name__ == "__main__":
    #Just for debug
    b = test_mpmath_discrete_init()
    b.runTest()
