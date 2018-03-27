import os
import sys
fileDir = os.path.dirname(os.path.realpath(__file__))
modPath = fileDir+'/tools' # Keep modules before dependencies
sys.path.insert(0,modPath)
depPath = fileDir+'/parts'
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

def getdMatFromDiscrete(matType, matDict, asymCal):
    return tu.getDiscreteScatteringMatrix(matType, matDict, asymCal)

def getdMatFromContinuous(matType, funPtr, asymCal, startEne, endEne, 
                          numPoints):
    cMat = tu.getContinuousScatteringMatrix(matType, funPtr, asymCal)
    return cMat.discretise(startEne, endEne, numPoints-1)

MOD_CHART = 0
MOD_SFIT_MC_ELASTIC = 1
def getTool(modID, resultsRoot=None, parmaFilePaths=None):
    if modID == MOD_CHART:
        import chart as mod
    elif modID == MOD_SFIT_MC_ELASTIC:
        import sfit_mc_elastic as mod
    else:
        raise Exception("Unrecognised module enum.")
    if resultsRoot is not None:
        mod.resultsRoot = resultsRoot+os.sep+nw.getConfigString()+os.sep
    if parmaFilePaths is not None:
        for i,parmaFilePath in enumerate(parmaFilePaths):
            if parmaFilePath is not None:
                mod.parmaFilePaths[i] = parmaFilePath
    return mod

def usePythonTypes(dps=nw.dps_default_python):
    nw.usePythonTypes(dps)

def useMpmathTypes(dps=nw.dps_default_mpmath):
    nw.useMpmathTypes(dps)

# If overridden, will look for the modules in the site-packages first.
dependencyOverride = False
def overrideDependencies():
    global dependencyOverride
    if not dependencyOverride:
        sys.path.remove(depPath)
        sys.path.append(depPath)
        dependencyOverride = True
