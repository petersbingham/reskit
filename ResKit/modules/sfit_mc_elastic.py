import yaml

import os
import sys
resultsRoot = None
configDir = os.path.dirname(os.path.realpath(__file__))
configDef1 = configDir + "/sfit_mc_elastic-coeffs-default.yml"
configDef2 = configDir + "/sfit_mc_elastic-roots-QIs-default.yml"
parmaFilePaths = [configDef1, configDef2]

import parSmat as psm
import stelempy as sp

def _initTypes(dMat):
    psm.setTypeMode(dMat.getTypeMode(), dMat.getTypeDps())

def getElasticSmats(dMat, Nlist, asymCalc):
    _initTypes(dMat)
    dSmat = dMat.to_dSmat()
    cSmats = []
    for N in Nlist:
        ris = dSmat.calculateReductionIndices(0,len(dSmat)-1,N)[0]
        dSmat2 = dSmat[ris[0]:ris[1]:ris[2]]
        coeffs = psm.calculateCoefficients(dSmat2, asymCalc)
        cSmats.append(psm.getElasticSmatFun(coeffs, asymCalc))
    return cSmats

def getElasticFins(dMat, Nlist, asymCalc):
    _initTypes(dMat)
    dSmat = dMat.to_dSmat()
    cFins = []
    for N in Nlist:
        ris = dSmat.calculateReductionIndices(0,len(dSmat)-1,N)[0]
        dSmat2 = dSmat[ris[0]:ris[1]:ris[2]]
        coeffs = psm.calculateCoefficients(dSmat2, asymCalc)
        cFins.append(psm.getElasticFinFun(coeffs, asymCalc))
    return cFins

def calculateQIs(cFins):
    roots = []
    for cFin in cFins:
        cVal = cFin.determinant()
        roots.append(cVal.findRoots())
    with open(parmaFilePaths[1], 'r') as f:
        config = yaml.load(f.read())
        p = config["stelempy"]
        ret = sp.calculateConvergenceGroupsRange(roots, p["startingDistThres"],
                            p["endDistThres"], p["cfSteps"])
        return sp.calculateQIsFromRange(ret, p["amalgThres"])
