import os
import sys
fileDir = os.path.dirname(os.path.realpath(__file__))
modPath = fileDir+'/tools' # Keep tools before packages
sys.path.insert(0,modPath)
depPath = fileDir+'/packages'
sys.path.insert(0,depPath)

import channelutil as cu
import tisutil as tu
import pynumwrap as nw

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

def getdMatFromDiscrete(matType, matDict, asymCal, sourceStr):
    return tu.getDiscreteScatteringMatrix(matType, matDict, asymCal, sourceStr)

def getdMatFromContinuous(matType, funPtr, asymCal, startEne, endEne,
                          numPoints, sourceStr):
    cMat = tu.getContinuousScatteringMatrix(matType, funPtr, asymCal, sourceStr)
    return cMat.discretise(startEne, endEne, numPoints)

CHART = 0
SFIT_MC_RAK = 1
def getTool(toolID, data, resultsRoot=None, parmaFilePath=None):
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
    if resultsRoot is not None:
        resultsRoot = resultsRoot+os.sep
        resultsRoot += data.getSourceStr()+os.sep+nw.getConfigString()+os.sep
        resultsRoot += data.getHistStr()+os.sep+mod.toolName+os.sep
        if not os.path.isdir(resultsRoot):
            os.makedirs(resultsRoot)
    return tool(data, resultsRoot, parmaFilePath)

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

# If overridden, will look for the modules in the site-packages first.
packageOverride = False
def overridePackages():
    global packageOverride
    if not packageOverride:
        sys.path.remove(depPath)
        sys.path.append(depPath)
        packageOverride = True
        reload(cu)
        reload(tu)
        reload(nw)
