import os
import sys
fileDir = os.path.dirname(os.path.realpath(__file__))
rkPath = fileDir+'/../..'
sys.path.insert(0,rkPath)

import ResKit as rk
rk.safeMode = False
import channelutil as cu
import TwoChanRadialWell as rw

#### python Types ####
cal = cu.asymCal(cu.HARTs, [0,0])
cSmat = rw.getSmatFun(1.0,2.0,2.0,cal,1.0)
dSmat = cSmat.discretise(1.,8.,100)

chart = rk.getTool(rk.CHART, dSmat)
chart.plotSmatrix()

chart.plotSmatrix(len(dSmat)/4,len(dSmat)*3/4)
chart.plotSmatrix(len(dSmat)/4,len(dSmat)*3/4,5)
chart.plotSmatrix(len(dSmat)/4,len(dSmat)*3/4,5,cu.eVs)

chart.plotTmatrix(len(dSmat)/4,len(dSmat)*3/4)
chart.plotTmatrix(len(dSmat)/4,len(dSmat)*3/4,imag=True)
chart.plotTmatrix(len(dSmat)/4,len(dSmat)*3/4,row=0,col=0,logx=True,logy=True,
                  imag=True)

#### mpmath types ####
cu.useMpmathTypes()
rw.useMpmathTypes()
cal = cu.asymCal(cu.HARTs, [0,0])
cSmat = rw.getSmatFun(1.0,2.0,2.0,cal,1.0)
chart = rk.getTool(rk.CHART, cSmat)
chart.plotSmatrix()
dSmat = cSmat.discretise(1.,8.,100)
chart = rk.getTool(rk.CHART, dSmat)
chart.plotSmatrix()

# Check copy saved on file system
chart = rk.getTool(rk.CHART, dSmat, "./test", "chart-test.yml")
chart.plotSmatrix()
