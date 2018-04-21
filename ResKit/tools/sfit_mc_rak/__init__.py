import yaml
import os
import tabulate as t
import numpy as np

import pynumwrap as nw
import parSmat as psm
import stelempy as sp
import pynumutil as nu

import tool_helper as th

toolDir = os.path.dirname(os.path.realpath(__file__))
toolName = "sfit_mc_rak"

class sfit_mc_rak(th.tool):
    def __init__(self, data, resultsRoot, paramFilePath):
        th.tool.__init__(self, data, resultsRoot, paramFilePath, toolDir)
        #Two internal properties (mainly for testing):
        self.allCoeffsLoaded = False
        self.allRootsLoaded = False
        self._verifyParamCaches()

    def _verifyParamCaches(self):
        self._verifyParamCache(self._getRootConfigDir(), "findRoots")
        self._verifyParamCache(self._getPoleConfigDir(), "findPoles")

    ##### General file and string Functions #####

    def _getCoeffDirBase(self):
        return self.resultsRoot+"coeffs"+os.sep
    def _getRootConfigDirBase(self):
        return self.resultsRoot+"roots"+os.sep
    def _getPoleDirBase(self):
        return self.resultsRoot+"poles"+os.sep

    def _getRootConfigDir(self):
        return self._getRootConfigDirBase()+th.cfgName(self.paramFilePath)
    def _getPoleConfigDir(self):
        return self._getPoleDirBase()+th.cfgName(self.paramFilePath)

    def _getRootConfigPath(self):
        return self._getRootConfigDir()+os.sep+self._getConfigCacheName()
    def _getPoleConfigPath(self):
        return self._getPoleConfigDir()+os.sep+self._getConfigCacheName()

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
        a = self._getCoeffDirBase()+th.cfgName(self.paramFilePath)
        b = os.sep+self._getInputDescStr(N, ris0)
        return a + b

    def _getCoeffPath(self, coeffDir, typeStr, i):
        return coeffDir+os.sep+typeStr+"_"+str(i)+".dat"

    def _fixNumpyFile(self, fileName):
        f1 = th.fropen(fileName)
        f2 = th.fwopen(fileName+"_temp")
        for line in f1:
            th.fw(f2, line.replace("+-", '-').replace("\r\n", '\n'))
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
                with th.fwopen(coeffPath) as f:
                    th.fw(f, cmat)

    def _saveCoeffs(self, coeffs, N, ris0):
        if self.resultsRoot is not None:
            coeffDir = self._getCoeffDir(N, ris0)
            if not os.path.isdir(coeffDir):
                os.makedirs(coeffDir)
            self._saveCoeff(coeffs[0], coeffDir, "A")
            self._saveCoeff(coeffs[1], coeffDir, "B")
            self.log.writeMsg("Coeffs saved to: "+coeffDir)

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
                    with th.fropen(coeffPath) as f:
                        s1 = f.read()
                        l1 = s1.split("\n")
                        l2 = [self._splitmpRows(s) for s in l1]
                        l3 = [map(lambda s:self._fixmpMatStr(s),l) for l in l2]
                        coeff = nw.mpmath.matrix(l3)
                        coeffs.append(coeff)
            except Exception as inst:
                self.log.writeErr(str(inst))
                return None
        return coeffs

    def _loadCoeffs(self, N, ris0):
        if self.resultsRoot is not None:
            coeffDir = self._getCoeffDir(N, ris0)
            if os.path.isdir(coeffDir):
                coeffA = self._loadCoeff(N, coeffDir, "A")
                coeffB = self._loadCoeff(N, coeffDir, "B")
                if coeffA is not None and coeffB is not None:
                    self.log.writeMsg("Coefficients loaded from: "+coeffDir)
                    return coeffA, coeffB
        return None

    def _getCoefficients(self, dSmat, N, ris0):
        dSmat2 = dSmat[ris0[0]:ris0[1]:ris0[2]]
        coeffs = self._loadCoeffs(N, ris0)
        if coeffs is None:
            coeffs = psm.calculateCoefficients(dSmat2, dSmat2.asymCal)
            self.log.writeMsg("Coefficients calculated")
            self._saveCoeffs(coeffs, N, ris0)
            self.allCoeffsLoaded = False
        return coeffs

    ##### Root File #####

    def _getRootPath(self, rootDir, N, ris0):
        return rootDir+os.sep+self._getInputDescStr(N, ris0)+".dat"

    def _saveRootConfig(self, p):
        with th.fwopen(self._getRootConfigPath()) as f:
            th.fw(f, str(p))

    def _getRootFileHeaderStr(self, N, ris):
        Nstr = "N="+str(N)
        EminStr = "Emin="+str(ris[0][0])+"("+str(ris[1][0])+")"
        EmaxStr = "Emax="+str(ris[0][1])+"("+str(ris[1][1])+")"
        stepStr = "step="+str(ris[0][2])
        return Nstr+", "+EminStr+", "+EmaxStr+", "+stepStr+"\n\n"

    def _saveRoots(self, N, ris, roots, asymCal, p):
        if self.resultsRoot is not None:
            rootDir = self._getRootConfigDir()
            if not os.path.isdir(rootDir):
                os.makedirs(rootDir)

            header = self._getNumHeader(asymCal)
            rows = []
            for root in roots:
                rows.append(self._getkERow(root, asymCal))

            rootPath = self._getRootPath(rootDir, N, ris[0])
            with th.fwopen(rootPath) as f:
                th.fw(f, self._getRootFileHeaderStr(N, ris))
                th.fw(f, t.tabulate(rows,header))
                th.fw(f, "\ncomplete")
                self.log.writeMsg("Roots saved to: "+rootPath)

            self._saveRootConfig(p)

    def _loadRoots(self, N, ris):
        if self.resultsRoot is not None:
            rootDir = self._getRootConfigDir()
            if os.path.isdir(rootDir):
                rootPath = self._getRootPath(rootDir, N, ris[0])
                if not os.path.isfile(rootPath):
                    return None
                try:
                    with th.fropen(rootPath) as f:
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
                            self.log.writeErr("Incomplete root file")
                            return None
                        self.log.writeMsg("Roots loaded from: "+rootPath)
                        return roots
                except Exception as inst:
                    self.log.writeErr(str(inst))
                    return None
        return None

    def _getRoots(self, p, cFin, asymCal):
        roots = self._loadRoots(cFin.fitInfo[0], cFin.fitInfo[1])
        if roots is None:
            cVal = cFin.determinant(**p["cPolyMat_determinant"])
            roots = cVal.findRoots(**p["cPolyVal_findRoots"])
            self.log.writeMsg("Roots calculated")
            self._saveRoots(cFin.fitInfo[0], cFin.fitInfo[1], roots, asymCal, p)
            self.allRootsLoaded = False
        return roots

    ##### Pole Save #####

    def _getPoleDir(self, nList):
        return self._getPoleConfigDir() + os.sep+str(nList).replace(' ','')

    def _getPolePath(self, poleDir, dk):
        return poleDir+os.sep+"dk"+nu.sciStr(dk)+".dat"

    def _savePoleConfig(self, p):
        with th.fwopen(self._getPoleConfigPath()) as f:
            th.fw(f, str(p))

    def _getPoleFileHeaderStr(self, numPoles, asymCal):
        return str(numPoles)+" poles, "+asymCal.getUnits()+"\n\n"

    def _getPoleRow(N, pole, status, asymCal):
        return [str(N), status] + self._getkERow(pole, asymCal)

    def _savePoleData(self, nList, poleData, asymCal, p):
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
                with th.fwopen(polePath) as f:
                    th.fw(f, self._getPoleFileHeaderStr(len(poleData[0][i]), 
                                                          asymCal))
                    th.fw(f, t.tabulate(rows,header))
                    self.log.writeMsg("Poles saved to: "+polePath)
            self._savePoleConfig(p)

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
            with th.fwopen(QIPath) as f:
                th.fw(f, self._getQIFileHeaderStr(len(QIdat[0]), asymCal))
                th.fw(f, t.tabulate(rows,header))
                self.log.writeMsg("QI data saved to: "+QIPath)

    ##### Public API #####

    def getElasticSmat(self, N):
        self.log.writeCall("getElasticSmat("+str(N)+")")
        dSmat = self.data.to_dSmat()
        ris = dSmat.getSliceIndices(0,len(dSmat)-1,N)
        self.log.writeMsg("Calculating for slice:"+str(ris))
        self.allCoeffsLoaded = True
        coeffs = self._getCoefficients(dSmat, N, ris[0])
        with th.fropen(self.paramFilePath) as f:
            config = yaml.load(f.read())
            self.log.writeParameters(config["getElasticSmat"])
            ret = psm.getElasticSmatFun(coeffs, dSmat.asymCal,
                                        **config["getElasticSmat"])
            self.log.writeMsg("Calculation completed")
            self.log.writeCallEnd("getElasticSmat")
            return ret

    def getElasticFins(self, Nlist):
        self.log.writeCall("getElasticFins("+str(Nlist)+")")
        dSmat = self.data.to_dSmat()
        cFins = []
        for N in Nlist:
            ris = dSmat.getSliceIndices(0,len(dSmat)-1,N)
            self.log.writeMsg("Calculating for N="+str(N)+",slice:"+str(ris))
            self.allCoeffsLoaded = True
            coeffs = self._getCoefficients(dSmat, N, ris[0])
            cFin = psm.getElasticFinFun(coeffs, dSmat.asymCal)
            self.log.writeMsg("CFins calculated")
            cFin.fitInfo = (N,ris)
            cFins.append(cFin)
        self.log.writeCallEnd("getElasticFins")
        return cFins

    def findRoots(self, cFins, internal=False):
        self.log.writeCall("findRoots("+str(map(lambda x: x.fitInfo[0],
                                                cFins))+")", internal)
        class RootsList(list):
            def __init__(self):
                list.__init__(self)
                self.nList = []
                self.asymCal = None

        allRoots = RootsList()
        if len(cFins) > 0:
            with th.fropen(self.paramFilePath) as f:
                config = yaml.load(f.read())
                p = config["findRoots"]
                self.log.writeParameters(p)
                self.allRootsLoaded = True
                for cFin in cFins:
                    if allRoots.asymCal is not None:
                        assert allRoots.asymCal == cFin.asymCal
                    allRoots.asymCal = cFin.asymCal
                    roots = self._getRoots(p, cFin, allRoots.asymCal)
                    allRoots.append(roots)
                    allRoots.nList.append(cFin.fitInfo[0])
        self.log.writeCallEnd("findRoots")
        return allRoots

    def findPoles(self, cFinsOrRoots):
        try:
            paramStr = str(map(lambda x: x.fitInfo[0], cFinsOrRoots))
        except AttributeError:
            paramStr = str(cFinsOrRoots.nList)

        self.log.writeCall("findPoles("+paramStr+")")        
        if len(cFinsOrRoots) > 0:
            try:
                cFinsOrRoots.nList # Test for the parameter type.
                allRoots = cFinsOrRoots
            except AttributeError:
                allRoots = self.findRoots(cFinsOrRoots, True)
            if len(allRoots) > 0:
                with th.fropen(self.paramFilePath) as f:
                    config = yaml.load(f.read())
                    p = config["findPoles"]
                    self.log.writeParameters(p)
                    pp = p["stelempy"]
                    poleData = sp.calculateConvergenceGroupsRange(allRoots, 
                                         pp["startingDistThres"], 
                                         pp["endDistThres"], pp["cfSteps"])
                    self.log.writeMsg("Convergence groups calculated")
                    self._savePoleData(allRoots.nList, poleData,
                                       allRoots.asymCal, p)
                    QIdat = sp.calculateQIsFromRange(poleData, pp["amalgThres"])
                    self.log.writeMsg("QIs calculated")
                    self._saveQIdata(allRoots.nList, QIdat, allRoots.asymCal)
                    self.log.writeCallEnd("findPoles")
                    return QIdat
        self.log.writeCallEnd("findPoles")
        return None, None
