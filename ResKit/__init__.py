import os
import sys
fileDir = os.path.dirname(os.path.realpath(__file__))
modPath = fileDir+'/modules' # Keep modules before dependencies
sys.path.insert(0,modPath)
depPath = fileDir+'/dependencies'
sys.path.insert(0,depPath)

import channelutil as cu
import tisutil as tu
import pynumwrap as nw

# If overridden, will look for the modules in the site-packages first.
dependencyOverride = False
def overrideDependencies():
    global dependencyOverride
    if not dependencyOverride:
        sys.path.remove(depPath)
        sys.path.append(depPath)
        dependencyOverride = True

mat_type_S = tu.mat_type_S
mat_type_K = tu.mat_type_K
mat_type_T = tu.mat_type_T

RYDs = cu.RYDs
HARTs = cu.HARTs
eVs = cu.eVs

type_mode_python = nw.mode_python
type_mode_mpmath = nw.mode_mpmath
def initFromDiscreteData(matType, matDict, units, typeMode=None, typeDps=None):
    tu.setTypeMode(typeMode, typeDps)
    return tu.getDiscreteScatteringMatrix(matType, matDict, units)

def initFromContinuousData(matType, funPtr, units, startEne, endEne, numPoints,
                           typeMode=None, typeDps=None):
    tu.setTypeMode(typeMode, typeDps)
    cMat = tu.getContinuousScatteringMatrix(matType, funPtr, units)
    return cMat.discretise(startEne, endEne, numPoints-1)

MOD_CHART = 0
MOD_SFIT_MC_ELASTIC = 1
def getModule(modID, resultsRoot=None, parmaFilePaths=None):
    if modID == MOD_CHART:
        import chart as mod
    elif modID == MOD_SFIT_MC_ELASTIC:
        import sfit_mc_elastic as mod
    else:
        raise Exception("Unrecognised module enum.")
    if resultsRoot is not None:
        mod.resultsRoot = resultsRoot
    if parmaFilePaths is not None:
        for i,parmaFilePath in enumerate(parmaFilePaths):
            if parmaFilePath is not None:
                mod.parmaFilePaths[i] = parmaFilePath
    return mod
