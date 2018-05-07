import yaml
import os
import tabulate as t
import numpy as np

import pynumwrap as nw
import parSmat as psm
import stelempy as sp
import pynumutil as nu

import toolhelper as th

toolDir = os.path.dirname(os.path.realpath(__file__))
toolName = "sfit_mc_rak"

class sfit_mc_rak(th.tool):
    def __init__(self, data, archiveRoot, paramFilePath, silent):
        th.tool.__init__(self, data, archiveRoot, paramFilePath, toolDir,
                         silent)
        #Two internal properties (mainly for testing):
        self.allCoeffsLoaded = False
        self.allRootsLoaded = False
        self._verifyParamCaches()

    def _verifyParamCaches(self):
        self._verifyParamCache(self._getRootConfigDir(), "findFinRoots")
        self._verifyParamCache(self._getPoleConfigDir(), "findStableSmatPoles")

    ##### General file and string Functions #####

    def _getCoeffDirBase(self):
        return self.archiveRoot+"coeffs"+os.sep
    def _getRootConfigDirBase(self):
        return self.archiveRoot+"roots"+os.sep
    def _getPoleDirBase(self):
        return self.archiveRoot+"poles"+os.sep

    def _getRootConfigDir(self):
        return self._getRootConfigDirBase()+th.cfgName(self.paramFilePath)
    def _getPoleConfigDir(self):
        return self._getPoleDirBase()+th.cfgName(self.paramFilePath)

    def _getRootConfigPath(self):
        return self._getRootConfigDir()+os.sep+self._getConfigCacheName()
    def _getPoleConfigPath(self):
        return self._getPoleConfigDir()+os.sep+self._getConfigCacheName()

    def _getInputDescStr(self, Npts, ris0):
        return "Npts="+str(Npts)+"_"+"S="+str(ris0[0])+"_E="+str(ris0[1]-1)

    def _getNumHeader(self, asymCal):
        return ["k","E ("+asymCal.getUnits()+")"]

    def _getkERow(self, val, asymCal):
        kstr = str(val).replace('(','').replace(')','').replace(' ','')
        Estr = str(asymCal.ke(val)).replace('(','').replace(')','')
        Estr = Estr.replace(' ','')
        return [kstr, Estr]

    ##### Coefficient File #####

    def _getCoeffDir(self, Npts, ris0):
        a = self._getCoeffDirBase()+th.cfgName(self.paramFilePath)
        b = os.sep+self._getInputDescStr(Npts, ris0)
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

    def _saveCoeffs(self, coeffs, Npts, ris0):
        if self.archiveRoot is not None:
            coeffDir = self._getCoeffDir(Npts, ris0)
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

    def _loadCoeff(self, Npts, path, typeStr):
        coeffs = []
        for i in range(psm.getNumCoeffForNpts(Npts)):
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

    def _loadCoeffSet(self, Npts, coeffDir):
        coeffA = self._loadCoeff(Npts, coeffDir, "A")
        coeffB = self._loadCoeff(Npts, coeffDir, "B")
        if coeffA is not None and coeffB is not None:
            self.log.writeMsg("Coefficients loaded from: "+coeffDir)
            return coeffA, coeffB
        return None

    def _loadCoeffs(self, Npts, ris0):
        if self.archiveRoot is not None:
            # First try the supplied config.
            coeffDir = self._getCoeffDir(Npts, ris0)
            if os.path.isdir(coeffDir):
                return self._loadCoeffSet(Npts, coeffDir)
            # Now look for other configs that have compatible coeffs.
            coeffBaseDir = self._getCoeffDirBase()
            if os.path.isdir(coeffBaseDir):
                for coeffConfigDirName in th.getSubDirs(coeffBaseDir):
                    coeffConfigDir = coeffBaseDir+os.sep+coeffConfigDirName
                    for coeffDirName in th.getSubDirs(coeffConfigDir):
                        if "Npts="+str(Npts)+"_" in coeffDirName:
                            coeffDir = coeffConfigDir+os.sep+coeffDirName
                            return self._loadCoeffSet(Npts, coeffDir)
        return None

    def _getCoefficients(self, Npts, ris0):
        coeffs = self._loadCoeffs(Npts, ris0)
        if coeffs is None:
            dsmat = self.data[ris0[0]:ris0[1]:ris0[2]].to_dSmat()
            coeffs = psm.calculateCoefficients(dsmat, dsmat.asymCal)
            self.log.writeMsg("Coefficients calculated")
            self._saveCoeffs(coeffs, Npts, ris0)
            self.allCoeffsLoaded = False
        return coeffs

    ##### Root File #####

    def _getRootPath(self, rootDir, Npts, ris0):
        return rootDir+os.sep+self._getInputDescStr(Npts, ris0)+".dat"

    def _saveRootConfig(self, p):
        with th.fwopen(self._getRootConfigPath()) as f:
            th.fw(f, str(p))

    def _getRootFileHeaderStr(self, Npts, ris):
        Nstr = "Npts="+str(Npts)
        EminStr = "Emin="+str(ris[0][0])+"("+str(ris[1][0])+")"
        EmaxStr = "Emax="+str(ris[0][1]-1)+"("+str(ris[1][1])+")"
        stepStr = "step="+str(ris[0][2])
        return Nstr+", "+EminStr+", "+EmaxStr+", "+stepStr+"\n\n"

    def _saveRoots(self, Npts, ris, roots, asymCal, p):
        if self.archiveRoot is not None:
            rootDir = self._getRootConfigDir()
            if not os.path.isdir(rootDir):
                os.makedirs(rootDir)

            header = self._getNumHeader(asymCal)
            rows = []
            for root in roots:
                rows.append(self._getkERow(root, asymCal))

            rootPath = self._getRootPath(rootDir, Npts, ris[0])
            with th.fwopen(rootPath) as f:
                th.fw(f, self._getRootFileHeaderStr(Npts, ris))
                th.fw(f, t.tabulate(rows,header))
                th.fw(f, "\ncomplete")
                self.log.writeMsg("Roots saved to: "+rootPath)

            self._saveRootConfig(p)

    def _getRootPathIfExists(self, rootDir, Npts, ris0):
        rootPath = self._getRootPath(rootDir, Npts, ris0)
        if os.path.isfile(rootPath):
            return rootPath
        return None

    def _findCompatibleRootDir(self, Npts, ris):
        # First try the supplied config.
        rootConfigDir = self._getRootConfigDir()
        if os.path.isdir(rootConfigDir):
            rootPath = self._getRootPathIfExists(rootConfigDir, Npts, ris[0])
            if rootPath is not None:
                return rootPath
        # Now look for other configs that have compatible roots.
        rootBaseDir = self._getRootConfigDirBase()
        if os.path.isdir(rootBaseDir):
            for rootConfigDirName in th.getSubDirs(rootBaseDir):
                rootConfigDir = rootBaseDir+os.sep+rootConfigDirName
                if self._doesParamCacheMatch(rootConfigDir, "findFinRoots"):
                    rootPath = self._getRootPathIfExists(rootConfigDir, Npts,
                                                         ris[0])
                    if rootPath is not None:
                        return rootPath
        return None

    def _loadRoots(self, Npts, ris, p):
        if self.archiveRoot is not None:
            rootPath = self._findCompatibleRootDir(Npts, ris)
            if rootPath is not None:
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

    def _getRoots(self, p, cfin, asymCal):
        roots = self._loadRoots(cfin.fitInfo[0], cfin.fitInfo[1], p)
        if roots is None:
            cVal = cfin.determinant(**p["cPolyMat_determinant"])
            roots = cVal.findRoots(**p["cPolyVal_findRoots"])
            self.log.writeMsg("Roots calculated")
            self._saveRoots(cfin.fitInfo[0], cfin.fitInfo[1], roots, asymCal, p)
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

    def _getPoleRow(self, Npts, pole, status, asymCal):
        return [str(Npts), status] + self._getkERow(pole, asymCal)

    def _savePoleData(self, nList, poleData, asymCal, p):
        if self.archiveRoot is not None:
            poleDir = self._getPoleDir(nList)
            if not os.path.isdir(poleDir):
                os.makedirs(poleDir)

            for i,dk in enumerate(poleData[2]):
                header = ["Npts","status"] + self._getNumHeader(asymCal)
                rows = []
                for pole in poleData[0][i]:
                    for j in sorted(pole.keys()):
                        m = self._getPoleRow(nList[j], pole[j][0],
                                               pole[j][2], asymCal)
                        rows.append(m)
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

    def _savePoledata(self, nList, poleDat, asymCal):
        if self.archiveRoot is not None:
            header = self._getNumHeader(asymCal) + ["^dk","ENk"]
            rows = []
            for poleQI in poleDat[0]:
                rows.append(self._getQIRow(poleQI, asymCal))

            QIPath = self._getQIPath(self._getPoleDir(nList))
            with th.fwopen(QIPath) as f:
                th.fw(f, self._getQIFileHeaderStr(len(poleDat[0]), asymCal))
                th.fw(f, t.tabulate(rows,header))
                self.log.writeMsg("QI data saved to: "+QIPath)

    def _updateContainerStrings(self, Npts, cont, chartTitle=None):
        cont.setSourceStr(self.data.getSourceStr())
        cont.appendHistStr(self.data.getHistStr())
        cont.appendHistStr("sfit_mc_rat_N="+str(Npts))
        if chartTitle is not None:
            cont.setChartTitle("Fin")

    ##### Plots #####

    def _checkForFitPlot(self, csmat):
        try:
            csmat.sfit_mc_rak_SplotCompatible
        except Exception:
            self.log.writeErr("Not a csmat")
            return None

    ##### Public API #####

    def getElasticFin(self, Npts):
        """
        Performs an Fin fit using the specified number of fit points.

        Parameters
        ----------
        Npts : int
            Number of points to use in the fit. Must be an even number.

        Returns
        -------
        cfin : tisutil.cPolykmat
        """
        self.log.writeCall("getElasticFin("+str(Npts)+")")
        ris = self.data.getSliceIndices(numPoints=Npts)
        self.log.writeMsg("Calculating for Npts="+str(Npts)+",slice:"+str(ris))
        self.allCoeffsLoaded = True
        coeffs = self._getCoefficients(Npts, ris[0])
        cfin = psm.getElasticFinFun(coeffs, self.data.asymCal)
        cfin.fitInfo = (Npts,ris)
        self._updateContainerStrings(Npts, cfin, "Fin")
        self.log.writeMsg("cfin calculated")
        self.log.writeCallEnd("getElasticFin")
        return cfin

    def getElasticFins(self, NptsList):
        """
        Performs Fin fits using the specified list of fit points.

        Parameters
        ----------
        NptsList : list of ints
            List of fit points, each of which will be used to produce a fit.

        Returns
        -------
        cfins : list of tisutil.cPolykmat
        """
        self.log.writeCall("getElasticFins("+str(NptsList)+")")
        cfins = []
        for Npts in NptsList:
            cfins.append(self.getElasticFin(Npts))
        self.log.writeCallEnd("getElasticFins")
        return cfins

    def findFinRoots(self, cfins, internal=False):
        """
        Finds the roots of a list of parameterised Fins.

        Parameters
        ----------
        cfins : list of tisutil.cPolykmat
            Container representing the parameterised Fins.

        Returns
        -------
        allRoots : list of float or mpmath.mpcs
        """
        self.log.writeCall("findFinRoots("+str(map(lambda x: x.fitInfo[0],
                                                   cfins))+")", internal)
        class RootsList(list):
            def __init__(self):
                list.__init__(self)
                self.nList = []
                self.asymCal = None

        allRoots = RootsList()
        if len(cfins) > 0:
            with th.fropen(self.paramFilePath) as f:
                config = yaml.load(f.read())
                p = config["findFinRoots"]
                self.log.writeParameters(p)
                self.allRootsLoaded = True
                for cfin in cfins:
                    if allRoots.asymCal is not None:
                        assert allRoots.asymCal == cfin.asymCal
                    allRoots.asymCal = cfin.asymCal
                    roots = self._getRoots(p, cfin, allRoots.asymCal)
                    allRoots.append(roots)
                    allRoots.nList.append(cfin.fitInfo[0])
        self.log.writeCallEnd("findFinRoots")
        return allRoots

    def findStableSmatPoles(self, cfinsOrRoots):
        """
        Finds the S-matrix poles as the stable roots of the Fins from either
        a list of Fins or from a list of Fin roots.

        Parameters
        ----------
        cfinsOrRoots : list of either cfins or list of floats
            As returned from either getElasticFins or findFinRoots.

        Returns
        -------
        poleDat : list of lists.
            List of poles and their calculated quality indicators.
        amalgPoleDat : list of lists.
            List of poles that had been combined according to the amalgamation
            threshold specified in the paramFile.
        """
        try:
            paramStr = str(map(lambda x: x.fitInfo[0], cfinsOrRoots))
        except AttributeError:
            paramStr = str(cfinsOrRoots.nList)

        self.log.writeCall("findStableSmatPoles("+paramStr+")")
        if len(cfinsOrRoots) > 0:
            try:
                cfinsOrRoots.nList # Test for the parameter type.
                allRoots = cfinsOrRoots
            except AttributeError:
                allRoots = self.findFinRoots(cfinsOrRoots, True)
            if len(allRoots) > 0:
                with th.fropen(self.paramFilePath) as f:
                    config = yaml.load(f.read())
                    p = config["findStableSmatPoles"]
                    self.log.writeParameters(p)
                    pp = p["stelempy"]
                    endDistThres = None
                    try:
                        endDistThres = float(pp["endDistThres"])
                    except TypeError:
                        pass
                    poleData = sp.calculateConvergenceGroupsRange(allRoots,
                                         float(pp["startingDistThres"]),
                                         endDistThres, int(pp["cfSteps"]))
                    self.log.writeMsg("Convergence groups calculated")
                    self._savePoleData(allRoots.nList, poleData,
                                       allRoots.asymCal, p)
                    poleDat = sp.calculateQIsFromRange(poleData,
                                                     float(pp["amalgThres"]))
                    self.log.writeMsg("QIs calculated")
                    self._savePoledata(allRoots.nList, poleDat, allRoots.asymCal)
                    self.log.writeCallEnd("findStableSmatPoles")
                    return poleDat
        self.log.writeCallEnd("findStableSmatPoles")
        return None, None

    def getElasticSmat(self, Npts):
        """
        Performs S-matrix fits using the specified number of fit points.

        Parameters
        ----------
        Npts : int
            Number of points to use in the fit. Must be an even number.

        Returns
        -------
        csmat : tisutil.cPolySmat
        """
        self.log.writeCall("getElasticSmat("+str(Npts)+")")
        ris = self.data.getSliceIndices(numPoints=Npts)
        self.log.writeMsg("Calculating for slice:"+str(ris))
        self.allCoeffsLoaded = True
        coeffs = self._getCoefficients(Npts, ris[0])
        csmat = psm.getElasticSmatFun(coeffs, self.data.asymCal)
        csmat.fitInfo = (Npts,ris)
        csmat.sfit_mc_rak_SplotCompatible = True
        self._updateContainerStrings(Npts, csmat)
        self.log.writeMsg("Calculation completed")
        self.log.writeCallEnd("getElasticSmat")
        return csmat

    def plotSmatFit(self, csmat, numPlotPoints=None, units=None, i=None, j=None,
                    logx=False, logy=False, imag=False, show=True):
        """
        Plots the original data, the fit points used and the resultant S-matrix
        for the specified element/s.

        Parameters
        ----------
        csmat : tisutil.cPolySmat
            Fitted S-matrix returned from getElasticSmat.
        numPlotPoints, units, i, j, logx, logy, imag, show
            Refer to the chart tool for description.
        """
        Npts = csmat.fitInfo[0]
        self.log.writeCall("plotSmatFit("+str(Npts)+")")
        self._checkForFitPlot(csmat)
        ret = self._prepareForFitPlot(numPlotPoints)  
        if ret is not None:
            p, ln, orig = ret

            orig = orig.to_dSmat()
            orig = orig.createReducedDim(i).createReducedDim(j)

            ris0 = csmat.fitInfo[1][0]
            fitPnts = self.data[ris0[0]:ris0[1]:ris0[2]]
            fitPnts = fitPnts.to_dSmat()
            fitPnts = fitPnts.createReducedDim(i).createReducedDim(j)

            rng = orig.getRange()
            dsmat = csmat.discretise(rng[0], rng[1], ln)
            fit = dsmat.createReducedDim(i).createReducedDim(j)

            title = "S matrix fit for Npts="+str(Npts)
            title += ", m="+str(i+1)+", n="+str(j+1)

            self._plotFit(p, title, orig, fitPnts, fit, numPlotPoints, units,
                          logx, logy, imag, show)

        self.log.writeCallEnd("plotSmatFit")

    def plotTotalXSFit(self, csmat, numPlotPoints=None, units=None, logx=False,
                       logy=False, show=True):
        """
        Plots total cross section conversions from the original S-matrix data,
        the fit points used and the resultant S-matrix. Refer to the chart tool
        for a description of the parameters.

        Parameters
        ----------
        csmat : tisutil.cPolySmat
            Fitted S-matrix returned from getElasticSmat.
        numPlotPoints, units, logx, logy, show
            Refer to the chart tool for description.
        """
        Npts = csmat.fitInfo[0]
        self.log.writeCall("plotTotalXSFit("+str(Npts)+")")
        self._checkForFitPlot(csmat)
        ret = self._prepareForFitPlot(numPlotPoints)  
        if ret is not None:
            p, ln, orig = ret

            orig = orig.to_dXSmat().to_dTotXSval()

            ris0 = csmat.fitInfo[1][0]
            fitPnts = self.data[ris0[0]:ris0[1]:ris0[2]]
            fitPnts = fitPnts.to_dXSmat().to_dTotXSval()

            rng = orig.getRange()
            dsmat = csmat.discretise(rng[0], rng[1], ln)
            fit = dsmat.to_dXSmat().to_dTotXSval()

            title = "Total Cross Section fit for Npts="+str(Npts)

            self._plotFit(p, title, orig, fitPnts, fit, numPlotPoints, units,
                          logx, logy, False, show)

        self.log.writeCallEnd("plotTotalXSFit")
