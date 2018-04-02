import yaml
import os
import copy
import io
import tabulate as t
import numpy as np

import pynumwrap as nw
import parSmat as psm
import stelempy as sp
import pynumutil as nu

import tool_helper as th

modeDir = os.path.dirname(os.path.realpath(__file__))
toolName = "sfit_mc_elastic"

class sfit_mc_elastic:
    def __init__(self, data, resultsRoot, parmaFilePath):
        self.data = copy.deepcopy(data)
        self.resultsRoot = resultsRoot
        self.parmaFilePath = parmaFilePath
        if self.parmaFilePath is None:
            self.parmaFilePath = modeDir+os.sep+"default.yml"
        #Some internal properties (mainly for testing)
        self.allCoeffsLoaded = False
        self.allRootsLoaded = False

    ##### General file and string Functions #####

    def _getCoeffDirName(self):
        return self.resultsRoot+"coeffs"+os.sep
    def _getRootDirName(self):
        return self.resultsRoot+"roots"+os.sep
    def _getPoleDirName(self):
        return self.resultsRoot+"poles"+os.sep

    def _ropen(self, fileName):
        return io.open(fileName, 'r', newline='\n', encoding="utf-8")
    def _wopen(self, fileName):
        return io.open(fileName, 'w', newline='\n', encoding="utf-8")
    def _w(self, f, o):
        f.write(unicode(o))

    def _getInputDescStr(self, N, ris0):
        return "N="+str(N)+"_"+"S="+str(ris0[0])+"_E="+str(ris0[1])

    def _getNumHeader(self, asymCal):
        return ["k","E ("+asymCal.getUnits()+")"]

    def _getkERow(self, val, asymCal):
        kstr = str(val).replace('(','').replace(')','').replace(' ','')
        Estr = str(asymCal.ke(val)).replace('(','').replace(')','')
        Estr = Estr.replace(' ','')
        return [kstr, Estr]

    ##### Coefficient File #####

    def _getCoeffDir(self, N, ris0):
        a = self._getCoeffDirName()+th.cfgName(self.parmaFilePath)
        b = os.sep+self._getInputDescStr(N, ris0)
        return a + b

    def _getCoeffPath(self, coeffDir, typeStr, i):
        return coeffDir+os.sep+typeStr+"_"+str(i)+".dat"

    def _fixNumpyFile(self, fileName):
        f1 = self._ropen(fileName)
        f2 = self._wopen(fileName+"_temp")
        for line in f1:
            self._w(f2, line.replace("+-", '-').replace("\r\n", '\n'))
        f1.close()
        f2.close()
        os.remove(fileName)
        os.rename(fileName + "_temp", fileName)

    def _saveCoeff(self, coeff, path, typeStr):
        for i,cmat in enumerate(coeff):
            coeffPath = self._getCoeffPath(path, typeStr, i)
            if nw.mode == nw.mode_python:
                np.savetxt(coeffPath, cmat, delimiter=",", newline='\n')
                self._fixNumpyFile(coeffPath)
            else:
                with self._wopen(coeffPath) as f:
                    self._w(f, cmat)

    def _saveCoeffs(self, coeffs, N, ris0):
        if self.resultsRoot is not None:
            coeffDir = self._getCoeffDir(N, ris0)
            if not os.path.isdir(coeffDir):
                os.makedirs(coeffDir)
            self._saveCoeff(coeffs[0], coeffDir, "A")
            self._saveCoeff(coeffs[1], coeffDir, "B")

    def _splitmpRows(self, s):
        if "(" in s:
            return s.split("(")[1:]
        else:
            return s.split("  ")

    def _fixmpMatStr(self, s):
        return s.replace("[","").replace("]","").replace("[","").replace(")","")

    def _loadCoeff(self, N, path, typeStr):
        coeffs = []
        for i in range(psm.getNumCoeffForN(N)):
            coeffPath = self._getCoeffPath(path, typeStr, i)
            if not os.path.isfile(coeffPath):
                return None
            try:
                if nw.mode == nw.mode_python:
                    coeff = np.asmatrix(np.loadtxt(coeffPath, 
                                                   dtype=np.complex128,
                                                   delimiter=","))
                    coeffs.append(coeff)
                else:
                    with self._ropen(coeffPath) as f:
                        s1 = f.read()
                        l1 = s1.split("\n")
                        l2 = [self._splitmpRows(s) for s in l1]
                        l3 = [map(lambda s:self._fixmpMatStr(s),l) for l in l2]
                        coeff = nw.mpmath.matrix(l3)
                        coeffs.append(coeff)
            except Exception as inst:
                # TODO log
                return None
        return coeffs

    def _loadCoeffs(self, N, ris0):
        if self.resultsRoot is not None:
            coeffDir = self._getCoeffDir(N, ris0)
            if os.path.isdir(coeffDir):
                coeffA = self._loadCoeff(N, coeffDir, "A")
                coeffB = self._loadCoeff(N, coeffDir, "B")
                if coeffA is not None and coeffB is not None:
                    return coeffA, coeffB
        return None

    def _getCoefficients(self, dSmat, N, ris0):
        self.allCoeffsLoaded = True
        dSmat2 = dSmat[ris0[0]:ris0[1]:ris0[2]]
        coeffs = self._loadCoeffs(N, ris0)
        if coeffs is None:
            coeffs = psm.calculateCoefficients(dSmat2, dSmat2.asymCal)
            self._saveCoeffs(coeffs, N, ris0)
            self.allCoeffsLoaded = False
        return coeffs

    ##### Root File #####

    def _getRootDir(self):
        return self._getRootDirName()+th.cfgName(self.parmaFilePath)

    def _getRootPath(self, rootDir, N, ris0):
        return rootDir+os.sep+self._getInputDescStr(N, ris0)+".dat"

    def _getRootFileHeaderStr(self, N, ris):
        Nstr = "N="+str(N)
        EminStr = "Emin="+str(ris[0][0])+"("+str(ris[1][0])+")"
        EmaxStr = "Emax="+str(ris[0][1])+"("+str(ris[1][1])+")"
        stepStr = "step="+str(ris[0][2])
        return Nstr+", "+EminStr+", "+EmaxStr+", "+stepStr+"\n\n"

    def _saveRoots(self, N, ris, roots, asymCal):
        if self.resultsRoot is not None:
            rootDir = self._getRootDir()
            if not os.path.isdir(rootDir):
                os.makedirs(rootDir)

            header = self._getNumHeader(asymCal)
            rows = []
            for root in roots:
                rows.append(self._getkERow(root, asymCal))

            rootPath = self._getRootPath(rootDir, N, ris[0])
            with self._wopen(rootPath) as f:
                self._w(f, self._getRootFileHeaderStr(N, ris))
                self._w(f, t.tabulate(rows,header))
                self._w(f, "\ncomplete")

    def _loadRoots(self, N, ris):
        if self.resultsRoot is not None:
            rootDir = self._getRootDir()
            if os.path.isdir(rootDir):
                rootPath = self._getRootPath(rootDir, N, ris[0])
                if not os.path.isfile(rootPath):
                    return None
                try:
                    with self._ropen(rootPath) as f:
                        fndStart = False
                        roots = []
                        for l in f:
                            if not fndStart:
                                if "---" in l:
                                    fndStart = True
                                continue
                            elif "complete" not in l:
                                roots.append(nw.complex(l.split()[0]))
                        if "complete" not in l:
                            # TODO log
                            return None
                        return roots
                except Exception as inst:
                    # TODO log
                    return None
        return None

    def _getRoots(self, p, cFin, asymCal):
        self.allRootsLoaded = True
        roots = self._loadRoots(cFin.fitInfo[0], cFin.fitInfo[1])
        if roots is None:
            cVal = cFin.determinant(**p["cPolyMat_determinant"])
            roots = cVal.findRoots(**p["cPolyVal_findRoots"])
            self._saveRoots(cFin.fitInfo[0], cFin.fitInfo[1], roots, 
                       asymCal)
            self.allRootsLoaded = False
        return roots

    ##### Pole Save #####

    def _getPoleDir(self, nList):
        a = self._getPoleDirName()+th.cfgName(self.parmaFilePath)
        b = os.sep+str(nList).replace(' ','')
        return a + b

    def _getPolePath(self, poleDir, dk):
        return poleDir+os.sep+"dk"+nu.sciStr(dk)+".dat"

    def _getPoleFileHeaderStr(self, numPoles, asymCal):
        return str(numPoles)+" poles, "+asymCal.getUnits()+"\n\n"

    def _getPoleRow(N, pole, status, asymCal):
        return [str(N), status] + self._getkERow(pole, asymCal)

    def _savePoleData(self, nList, poleData, asymCal):
        if self.resultsRoot is not None:
            poleDir = self._getPoleDir(nList)
            if not os.path.isdir(poleDir):
                os.makedirs(poleDir)
    
            for i,dk in enumerate(poleData[2]):
                header = ["N","status"] + self._getNumHeader(asymCal)
                rows = []
                for pole in poleData[0][i]:
                    for j in sorted(pole.keys()):
                        row = self._getPoleRow(nList[j], pole[j][0], 
                                               pole[j][2], asymCal)
                        rows.append(row)
                    rows.append(["","","",""])
    
                polePath = self._getPolePath(poleDir, dk)
                with self._wopen(polePath) as f:
                    self._w(f, self._getPoleFileHeaderStr(len(poleData[0][i]), 
                                                          asymCal))
                    self._w(f, t.tabulate(rows,header))

    ##### QI Save #####

    def _getQIPath(self, poleDir):
        return poleDir+os.sep+"QIs.dat"

    def _getQIFileHeaderStr(self, numPoles, asymCal):
        return str(numPoles)+" poles, "+asymCal.getUnits()+"\n\n"

    def _getQIRow(self, poleQI, asymCal):
        return self._getkERow(poleQI[0], asymCal) + [str(poleQI[1]), 
                                                     str(poleQI[2])]

    def _saveQIdata(self, nList, QIdat, asymCal):
        if self.resultsRoot is not None:
            header = self._getNumHeader(asymCal) + ["^dk","ENk"]
            rows = []
            for poleQI in QIdat[0]:
                rows.append(self._getQIRow(poleQI, asymCal))
            
            QIPath = self._getQIPath(self._getPoleDir(nList))
            with self._wopen(QIPath) as f:
                    self._w(f, self._getQIFileHeaderStr(len(QIdat[0]), 
                                                        asymCal))
                    self._w(f, t.tabulate(rows,header))

    ##### Public API #####

    def getElasticSmat(self, N):
        dSmat = self.data.to_dSmat()
        ris = dSmat.getSliceIndices(0,len(dSmat)-1,N)
        coeffs = self._getCoefficients(dSmat, N, ris[0])
        with self._ropen(self.parmaFilePath) as f:
            config = yaml.load(f.read())
            return psm.getElasticSmatFun(coeffs, dSmat.asymCal,
                                         **config["getElasticSmat"])

    def getElasticFins(self, Nlist):
        dSmat = self.data.to_dSmat()
        cFins = []
        for N in Nlist:
            ris = dSmat.getSliceIndices(0,len(dSmat)-1,N)
            coeffs = self._getCoefficients(dSmat, N, ris[0])
            cFin = psm.getElasticFinFun(coeffs, dSmat.asymCal)
            cFin.fitInfo = (N,ris)
            cFins.append(cFin)
        return cFins

    def calculateQIs(self, cFins):
        if len(cFins) > 0:
            with self._ropen(self.parmaFilePath) as f:
                config = yaml.load(f.read())
                p = config["calculateQIs"]
                allRoots = []
                nList = []
                asymCal = None
                if len(cFins) > 0:
                    for cFin in cFins:
                        if asymCal is not None:
                            assert asymCal == cFin.asymCal
                        asymCal = cFin.asymCal
                        roots = self._getRoots(p, cFin, asymCal)
                        allRoots.append(roots)
                        nList.append(cFin.fitInfo[0])

                    p = p["stelempy"]
                    poleData = sp.calculateConvergenceGroupsRange(allRoots, 
                                         p["startingDistThres"], 
                                         p["endDistThres"], p["cfSteps"])
                    self._savePoleData(nList, poleData, asymCal)
                    QIdat = sp.calculateQIsFromRange(poleData, p["amalgThres"])
                    self._saveQIdata(nList, QIdat, asymCal)
                    return QIdat
            return None, None
