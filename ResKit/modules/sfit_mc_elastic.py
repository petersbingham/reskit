import yaml

import os
import sys
resultsRoot = None
configDir = os.path.dirname(os.path.realpath(__file__))
configDef = configDir + "/sfit_mc_elastic-default.yml"
parmaFilePaths = [configDef]

import parSmat as psm
import stelempy as sp

def _setTypeMode(dMat):
    psm.setTypeMode(dMat.getTypeMode(), dMat.getTypeDps())

def _calculateCoefficients(dSmat, N, asymCalc):
    ris = dSmat.calculateReductionIndices(0,len(dSmat)-1,N)[0]
    dSmat2 = dSmat[ris[0]:ris[1]:ris[2]]
    return psm.calculateCoefficients(dSmat2, asymCalc)

def getElasticSmats(dMat, Nlist, asymCalc):
    _setTypeMode(dMat)
    dSmat = dMat.to_dSmat()
    cSmats = []
    for N in Nlist:
        coeffs = _calculateCoefficients(dSmat, N, asymCalc)
        with open(parmaFilePaths[0], 'r') as f:
            config = yaml.load(f.read())
            cSmats.append(psm.getElasticSmatFun(coeffs, asymCalc,
                                                **config["getElasticSmats"]))
    return cSmats

def getElasticFins(dMat, Nlist, asymCalc):
    _setTypeMode(dMat)
    dSmat = dMat.to_dSmat()
    cFins = []
    for N in Nlist:
        coeffs = _calculateCoefficients(dSmat, N, asymCalc)
        cFins.append(psm.getElasticFinFun(coeffs, asymCalc))
    return cFins

def calculateQIs(cFins):
    with open(parmaFilePaths[0], 'r') as f:
        config = yaml.load(f.read())
        roots = []
        for cFin in cFins:
            p = config["calculateQIs"]
            cVal = cFin.determinant(**p["cPolyMat_determinant"])
            roots.append(cVal.findRoots(**p["cPolyVal_findRoots"]))

        p = p["stelempy"]
        ret = sp.calculateConvergenceGroupsRange(roots, p["startingDistThres"],
                            p["endDistThres"], p["cfSteps"])
        return sp.calculateQIsFromRange(ret, p["amalgThres"])
