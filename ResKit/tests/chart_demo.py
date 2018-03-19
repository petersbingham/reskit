import os
import sys
fileDir = os.path.dirname(os.path.realpath(__file__))
rkPath = fileDir+'/../..'
sys.path.insert(0,rkPath)

import ResKit as rk
import channelutil as cu
import TwoChanRadialWell as rw

#### python Types ####

cal = cu.asymCal([0.,0.], units=cu.HARTs)
cSmat = rw.getSmatFun(1.0,2.0,2.0,cal,1.0)
dSmat = cSmat.discretise(1.,8.,100)
chart = rk.getModule(rk.MOD_CHART)

chart.plotSmatrix(dSmat)

chart.plotSmatrix(dSmat,len(dSmat)/4,len(dSmat)*3/4)
chart.plotSmatrix(dSmat,len(dSmat)/4,len(dSmat)*3/4,5)
chart.plotSmatrix(dSmat,len(dSmat)/4,len(dSmat)*3/4,5,cu.eVs)

chart.plotTmatrix(dSmat,len(dSmat)/4,len(dSmat)*3/4)
chart.plotTmatrix(dSmat,len(dSmat)/4,len(dSmat)*3/4,imag=True)
chart.plotTmatrix(dSmat,len(dSmat)/4,len(dSmat)*3/4,row=0,col=0,
                  logx=True,logy=True,imag=True)

#### mpmath types ####

cu.useMpmathTypes()
rw.useMpmathTypes()
cal = cu.asymCal([0.,0.], units=cu.HARTs)
cSmat = rw.getSmatFun(1.0,2.0,2.0,cal,1.0)
dSmat = cSmat.discretise(1.,8.,100)
chart.plotSmatrix(dSmat)

# Check copy saved on file system
chart = rk.getModule(rk.MOD_CHART, ".", ["chart-test.yml"])
chart.plotSmatrix(dSmat)
