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
csmat = rw.getSmatFun(1.0,2.0,2.0,cal,1.0)
dsmat = csmat.discretise(1.,8.,100)

chart = rk.getTool(rk.CHART, dsmat)

chart.plotSmatrix()

chart.plotSmatrix(len(dsmat)/4,len(dsmat)*3/4)
chart.plotSmatrix(len(dsmat)/4,len(dsmat)*3/4,5)
chart.plotSmatrix(len(dsmat)/4,len(dsmat)*3/4,5,cu.eVs)
chart.plotTmatrix(len(dsmat)/4,len(dsmat)*3/4)
chart.plotTmatrix(len(dsmat)/4,len(dsmat)*3/4,imag=True)
chart.plotTotalXS(len(dsmat)/4,len(dsmat)*3/4)

chart.plotSmatrix(len(dsmat)/4,len(dsmat)*3/4,i=0,j=0,logx=True,logy=True,
                  imag=True)

#### mpmath types ####
cu.useMpmathTypes()
rw.useMpmathTypes()
cal = cu.AsymCalc(cu.HARTs, [0,0])
csmat = rw.getSmatFun(1.0,2.0,2.0,cal,1.0)
chart = rk.getTool(rk.CHART, csmat)
chart.plotSmatrix()
dsmat = csmat.discretise(1.,8.,100)
chart = rk.getTool(rk.CHART, dsmat)
chart.plotSmatrix()

# Check copy saved on file system
chart = rk.getTool(rk.CHART, dsmat, TEST_ROOT, "chart-test.yml")
chart.plotSmatrix()
