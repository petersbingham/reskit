import os
import sys
fileDir = os.path.dirname(os.path.realpath(__file__))
modPath = fileDir+'/tools' # Keep tools before utilities
sys.path.insert(0,modPath)
depPath = fileDir+'/utilities'
sys.path.insert(0,depPath)

import channelutil as cu
import tisutil as tu
import pynumwrap as nw
import toolhelper as th

# Changing the types after a tool has been created renders old tools in an
# undefined state and they should not be used. safeMode prevents changing type
# after tools have been created.
safeMode = True

Smat = tu.Smat
Kmat = tu.Kmat
Tmat = tu.Tmat

RYDs = cu.RYDs
HARTs = cu.HARTs
eVs = cu.eVs

def getAsymCalc(units, ls=None):
    return cu.asymCal(units, ls)

def getdmatFromDiscrete(matType, matDict, asymCal, sourceStr):
    return tu.getDiscreteScatteringMatrix(matType, matDict, asymCal, sourceStr)

def getdmatFromContinuous(matType, funPtr, asymCal, startEne, endEne, numPoints,
                          sourceStr):
    cmat = tu.getContinuousScatteringMatrix(matType, funPtr, asymCal, sourceStr)
    return cmat.discretise(startEne, endEne, numPoints)

CHART = 0
SFIT_MC_RAK = 1
def getTool(toolID, data, archiveRoot=None, paramFilePath=None, silent=False):
    if safeMode:
        nw.lockType()
    if toolID == CHART:
        import chart as mod
        tool = mod.chart
    elif toolID == SFIT_MC_RAK:
        import sfit_mc_rak as mod
        tool = mod.sfit_mc_rak
    else:
        raise Exception("Unrecognised module.")
    if archiveRoot is not None:
        dataRoot = archiveRoot+os.sep+data.getSourceStr()+os.sep
        dataRoot += nw.getConfigString()+os.sep+data.getHistStr()+os.sep
        archiveRoot = dataRoot+mod.toolName+os.sep
        if not os.path.isdir(dataRoot):
            os.makedirs(dataRoot)
            with th.fwopen(dataRoot+"checkdata.dat") as f:
                th.fw(f, data.getCheckStr())
        else:
            if os.path.isfile(dataRoot+"checkdata.dat"):
                with th.fropen(dataRoot+"checkdata.dat") as f:
                    if str(f.read()) != str(data.getCheckStr()):
                        s = "Supplied data does not correspond to that used "
                        s += "to originally create the dataRoot."
                        raise Exception(s)
            else:
                s = "Invalid archive state: data dir with no checkdata.dat."
                raise Exception(s)
        if not os.path.isdir(archiveRoot):
            os.makedirs(archiveRoot)

    return tool(data, archiveRoot, paramFilePath, silent)

def usePythonTypes(dps=nw.dps_default_python):
    try:
        nw.usePythonTypes(dps)
    except:
        s = "Types can only be changed at start of session in safeMode."
        raise Exception(s)

def useMpmathTypes(dps=nw.dps_default_mpmath):
    try:
        nw.useMpmathTypes(dps)
    except:
        s = "Types can only be changed at start of session in safeMode."
        raise Exception(s)

# If overridden, will look for the modules in the site-utilities first.
utilityOverride = False
def overrideUtilities():
    global utilityOverride
    if not utilityOverride:
        sys.path.remove(depPath)
        sys.path.append(depPath)
        utilityOverride = True
        reload(cu)
        reload(tu)
        reload(nw)
