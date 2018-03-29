import yaml
import os
import sys
import copy
import tabulate as t

resultsRoot = None
configDir = os.path.dirname(os.path.realpath(__file__))
configDef = configDir + "/sfit_mc_elastic-default.yml"
parmaFilePaths = [configDef]

import pynumwrap as nw
import parSmat as psm
import stelempy as sp
import pynumutil as nu

import numpy as np

def _getInputDescStr(N, ris0):
    return "N="+str(N)+"_"+"S="+str(ris0[0])+"_E="+str(ris0[1])

def _getNumHeader(asymCal):
    return ["k","E ("+asymCal.getUnits()+")"]

def _getNumRow(val, asymCal):
    kstr = str(val).replace('(','').replace(')','')
    Estr = str(asymCal.ke(val)).replace('(','').replace(')','')
    return [kstr, Estr]

##### Coefficient Save #####

def _fixNumpyFile(fileName):
    f1 = open(fileName, 'r')
    f2 = open(fileName + "_temp", 'w')
    for line in f1:
        f2.write(line.replace("+-", '-'))
    f1.close()
    f2.close()
    os.remove(fileName)
    os.rename(fileName + "_temp", fileName)

def _saveCoeff(coeff, path, typeStr):
    fileBase = path+os.sep+typeStr+"_"
    for i,cmat in enumerate(coeff):
        fileName = fileBase+str(i)+".dat"
        if nw.mode == nw.mode_python:
            np.savetxt(fileName, cmat, delimiter=",")
            _fixNumpyFile(fileName)
        else:
            with open(fileName, 'w') as f:
                f.write(str(cmat))

def _saveCoeffs(coeffs, N, ris0):
    if resultsRoot is not None:
        path = resultsRoot+"coeffs"+os.sep+_getInputDescStr(N, ris0)
        if not os.path.isdir(path):
            os.makedirs(path)
        _saveCoeff(coeffs[0], path, "A")
        _saveCoeff(coeffs[1], path, "B")

def _calculateCoefficients(dSmat, N, ris0):
    dSmat2 = dSmat[ris0[0]:ris0[1]:ris0[2]]
    coeffs = psm.calculateCoefficients(dSmat2, dSmat2.asymCal)
    _saveCoeffs(coeffs, N, ris0)
    return coeffs

##### Root Save #####

def _getRootFileHeaderStr(N, ris, asymCal):
    Nstr = "N="+str(N)
    EminStr = "Emin="+str(ris[0][0])+"("+str(ris[1][0])+")"
    EmaxStr = "Emax="+str(ris[0][1])+"("+str(ris[1][1])+")"
    stepStr = "step="+str(ris[0][2])
    return Nstr+", "+EminStr+", "+EmaxStr+", "+stepStr+"\n\n"

def _saveRoots(N, ris, roots, asymCal):
    if resultsRoot is not None:
        path = resultsRoot+"roots"
        if not os.path.isdir(path):
            os.makedirs(path)
    
        header = _getNumHeader(asymCal)
        rows = []
        for root in roots:
            rows.append(_getNumRow(root, asymCal))
    
        fileName = path + os.sep+_getInputDescStr(N, ris[0])+".dat"
        with open(fileName, 'w') as f:
            f.write(_getRootFileHeaderStr(N, ris, asymCal))
            f.write(t.tabulate(rows,header))

##### Pole Save #####

def _getPoleInfoPath(nList):
    return resultsRoot+"poles"+os.sep+str(nList).replace(' ','')+os.sep

def _getPoleFileHeaderStr(numPoles, asymCal):
    return str(numPoles)+" poles, "+asymCal.getUnits()+"\n\n"

def _getPoleRow(N, pole, status, asymCal):
    return [str(N), status] + _getNumRow(pole, asymCal)

def _savePoleData(nList, poleData, asymCal):
    if resultsRoot is not None:
        path = _getPoleInfoPath(nList)
        if not os.path.isdir(path):
            os.makedirs(path)
    
        for i,dk in enumerate(poleData[2]):
            header = ["N","status"] + _getNumHeader(asymCal)
            rows = []
            for pole in poleData[0][i]:
                for j in sorted(pole.keys()):
                    row = _getPoleRow(nList[j], pole[j][0], pole[j][2], asymCal)
                    rows.append(row)
                rows.append(["","","",""])
    
            fileName = path+os.sep+"dk"+nu.sciStr(dk)+".dat"
            with open(fileName, 'w') as f:
                f.write(_getPoleFileHeaderStr(len(poleData[0][i]), asymCal))
                f.write(t.tabulate(rows,header))

##### QI Save #####

def _getQIFileHeaderStr(numPoles, asymCal):
    return str(numPoles)+" poles, "+asymCal.getUnits()+"\n\n"

def _getQIRow(poleQI, asymCal):
    return _getNumRow(poleQI[0], asymCal) + [str(poleQI[1]), str(poleQI[2])]

def _saveQIdata(nList, QIdat, asymCal):
    if resultsRoot is not None:
        header = _getNumHeader(asymCal) + ["^dk","ENk"]
        rows = []
        for poleQI in QIdat[0]:
            rows.append(_getQIRow(poleQI, asymCal))
        
        fileName = _getPoleInfoPath(nList)+os.sep+"QIs.dat"
        with open(fileName, 'w') as f:
                f.write(_getQIFileHeaderStr(len(QIdat[0]), asymCal))
                f.write(t.tabulate(rows,header))

##### Public API #####

def getElasticSmat(dMat, N):
    dSmat = dMat.to_dSmat()
    ris = dSmat.getSliceIndices(0,len(dSmat)-1,N)
    coeffs = _calculateCoefficients(dSmat, N, ris[0])
    with open(parmaFilePaths[0], 'r') as f:
        config = yaml.load(f.read())
        return psm.getElasticSmatFun(coeffs, dSmat.asymCal,
                                     **config["getElasticSmat"])

def getElasticFins(dMat, Nlist):
    dSmat = dMat.to_dSmat()
    cFins = []
    for N in Nlist:
        ris = dSmat.getSliceIndices(0,len(dSmat)-1,N)
        coeffs = _calculateCoefficients(dSmat, N, ris[0])
        cFin = psm.getElasticFinFun(coeffs, dSmat.asymCal)
        cFin.fitInfo = (N,ris)
        cFins.append(cFin)
    return cFins

def calculateQIs(cFins):
    if len(cFins) > 0:
        with open(parmaFilePaths[0], 'r') as f:
            config = yaml.load(f.read())
            allRoots = []
            nList = []
            asymCal = None
            for cFin in cFins:
                if asymCal is not None:
                    assert asymCal == cFin.asymCal
                asymCal = cFin.asymCal
                p = config["calculateQIs"]
                cVal = cFin.determinant(**p["cPolyMat_determinant"])
                roots = cVal.findRoots(**p["cPolyVal_findRoots"])
                allRoots.append(roots)
                nList.append(cFin.fitInfo[0])
                _saveRoots(cFin.fitInfo[0], cFin.fitInfo[1], roots, asymCal)

            p = p["stelempy"]
            poleData = sp.calculateConvergenceGroupsRange(allRoots, 
                            p["startingDistThres"], p["endDistThres"], p["cfSteps"])
            _savePoleData(nList, poleData, asymCal)
            QIdat = sp.calculateQIsFromRange(poleData, p["amalgThres"])
            _saveQIdata(nList, QIdat, asymCal)
            return QIdat
        return None, None
