import os
import sys
import shutil
fileDir = os.path.dirname(os.path.realpath(__file__))
rkPath = fileDir+'/../../../..'
sys.path.insert(0,rkPath)

import reskit as rk
import channelutil as cu
import twochanradialwell as tcrw

TEST_ROOT = "chart-Smat-fin-fit"
if os.path.isdir(TEST_ROOT):
    shutil.rmtree(TEST_ROOT)

calc = rk.get_asym_calc(rk.hartrees, [0,0])
csmat = tcrw.get_Smat_fun(1.0, 2.0, 2.0, calc, 1.0)
dmat = rk.get_dmat_from_continuous(rk.Smat, csmat, calc, 1., 8., 1200, "radwell")

sfittool = rk.get_tool(rk.mcsmatfit, dmat, TEST_ROOT)
cfin = sfittool.get_elastic_Fin(10)

chart = rk.get_tool(rk.chart, cfin, TEST_ROOT)
chart.plot_raw()
