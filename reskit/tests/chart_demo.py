import os
import sys
import shutil
fileDir = os.path.dirname(os.path.realpath(__file__))
rkPath = fileDir+'/../..'
sys.path.insert(0,rkPath)

import reskit as rk
rk.safeMode = False
import channelutil as cu
import twochanradialwell as rw

TEST_ROOT = "chart_demo"
if os.path.isdir(TEST_ROOT):
    shutil.rmtree(TEST_ROOT)

#### python Types ####
cal = cu.AsymCalc(cu.HARTs, [0,0])
csmat = rw.get_Smat_fun(1.0,2.0,2.0,cal,1.0)
dsmat = csmat.discretise(1.,8.,100)

chart = rk.get_tool(rk.chart, dsmat)

chart.plot_Smatrix()

chart.plot_Smatrix(len(dsmat)/4,len(dsmat)*3/4)
chart.plot_Smatrix(len(dsmat)/4,len(dsmat)*3/4,5)
chart.plot_Smatrix(len(dsmat)/4,len(dsmat)*3/4,5,cu.eVs)
chart.plot_Tmatrix(len(dsmat)/4,len(dsmat)*3/4)
chart.plot_Tmatrix(len(dsmat)/4,len(dsmat)*3/4,imag=True)
chart.plot_TotalXS(len(dsmat)/4,len(dsmat)*3/4)

chart.plot_Smatrix(len(dsmat)/4,len(dsmat)*3/4,i=0,j=0,logx=True,logy=True,
                  imag=True)

#### mpmath types ####
cu.use_mpmath_types()
rw.use_mpmath_types()
cal = cu.AsymCalc(cu.HARTs, [0,0])
csmat = rw.get_Smat_fun(1.0,2.0,2.0,cal,1.0)
chart = rk.get_tool(rk.chart, csmat)
chart.plot_Smatrix()
dsmat = csmat.discretise(1.,8.,100)
chart = rk.get_tool(rk.chart, dsmat)
chart.plot_Smatrix()

# Check copy saved on file system
chart = rk.get_tool(rk.chart, dsmat, TEST_ROOT, "chart-test.yml")
chart.plot_Smatrix()
