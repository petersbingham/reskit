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

TEST_ROOT = "test_mcsmatfit_config"
if os.path.isdir(TEST_ROOT):
    shutil.rmtree(TEST_ROOT)

class parent_test(unittest.TestCase):
    def find_stable_Smat_poles(self):
        cal = rk.get_asym_calc(cu.hartrees, [0,0])
        csmat = rw.get_Smat_fun(1.0,2.0,2.0,cal,1.0)
        dsmat = csmat.discretise(1.,8.,100)

        mcsmatfit = rk.get_tool(rk.mcsmatfit, dsmat, archive_root=TEST_ROOT,
                               silent=True)
        cfins = mcsmatfit.get_elastic_Fins(range(2,4,2))
        mcsmatfit.find_stable_Smat_poles(cfins)

        # Import again with same config and check no exception
        rk.get_tool(rk.mcsmatfit, dsmat, archive_root=TEST_ROOT, silent=True)

        testPath = fileDir+os.sep+"test_mcsmatfit_data1"+os.sep+"default.yaml"
        self.assertRaises(Exception, rk.get_tool, rk.mcsmatfit, dsmat,
                          archive_root=TEST_ROOT, param_file_path=testPath,
                          silent=True)

        testPath = fileDir+os.sep+"test_mcsmatfit_data2"+os.sep+"default.yaml"
        self.assertRaises(Exception, rk.get_tool, rk.mcsmatfit, dsmat,
                          archive_root=TEST_ROOT, param_file_path=testPath,
                          silent=True)


class test_numpy(parent_test):
    def runTest(self):
        rk.use_python_types()
        self.find_stable_Smat_poles()

class test_mpmath(parent_test):
    def runTest(self):
        rk.use_mpmath_types()
        self.find_stable_Smat_poles()

if __name__ == "__main__":
    #Just for debug
    b = test_numpy()
    b.runTest()
