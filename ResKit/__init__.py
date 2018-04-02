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

TOOL_CHART = 0
TOOL_SFIT_MC_ELASTIC = 1
def getTool(toolID, data, resultsRoot=None, parmaFilePath=None):
    if toolID == TOOL_CHART:
        import chart as mod
    elif toolID == TOOL_SFIT_MC_ELASTIC:
        import sfit_mc_elastic as mod
    else:
        raise Exception("Unrecognised module enum.")
    mod.data = data
    if resultsRoot is not None:
        mod.resultsRoot = resultsRoot+os.sep
        mod.resultsRoot += data.getSourceStr()+os.sep+data.getHistStr()+os.sep
        mod.resultsRoot += nw.getConfigString()+os.sep+mod.toolName+os.sep
        if not os.path.isdir(mod.resultsRoot):
            os.makedirs(mod.resultsRoot)
    if parmaFilePath is not None:
        mod.parmaFilePath = parmaFilePath
    return mod

# TODO prevent changing types after getTool
def usePythonTypes(dps=nw.dps_default_python):
    nw.usePythonTypes(dps)

def useMpmathTypes(dps=nw.dps_default_mpmath):
    nw.useMpmathTypes(dps)

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
