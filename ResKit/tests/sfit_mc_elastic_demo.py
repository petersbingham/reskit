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
sfit_mc_elastic = rk.getModule(rk.MOD_SFIT_MC_ELASTIC)

cFins = sfit_mc_elastic.getElasticFins(dSmat, range(2,20,2), cal)
sfit_mc_elastic.calculateQIs(cFins)


#### mpmath types ####
'''
cu.useMpmathTypes()
rw.useMpmathTypes()
cal = cu.asymCal([0.,0.], units=cu.HARTs)
cSmat = rw.getSmatFun(1.0,2.0,2.0,cal,1.0)
dSmat = cSmat.discretise(1.,8.,100)
'''