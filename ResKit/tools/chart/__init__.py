import yaml
import os

import toolhelper as th

toolDir = os.path.dirname(os.path.realpath(__file__))
toolName = "chart"

class chart(th.tool):
    def __init__(self, data, archiveRoot, paramFilePath, silent):
        th.tool.__init__(self, data, archiveRoot, paramFilePath, toolDir,
                         silent)

    def _writeCall(self, start, end, numPlotPoints, units, i, j, logx, logy,
                   imag, show, funName):
        self.log.writeCall(funName+"("+str(start)+","+str(end)+","\
                           +str(numPlotPoints)+","+str(units)+","+str(i)+","\
                           +str(j)+","+str(logx)+","+str(logy)+","+str(imag)\
                           +","+str(show)+")")

    def _setChartParameters(self, dbase):
        with open(self.paramFilePath, 'r') as f:
            config = yaml.load(f.read())
            self.log.writeParameters(config)
            dbase.setChartParameters(colourCycle=config["colourCycle"])
            dbase.setChartParameters(legPrefix=config["legPrefix"])
            dbase.setChartParameters(useMarker=config["useMarker"])
            dbase.setChartParameters(xsize=config["xsize"])
            dbase.setChartParameters(ysize=config["ysize"])

    def _getSaveString(self, start, end, numPlotPoints, logx, logy, units):
        ret = " " + str(start) + "_" + str(end) + "_" + str(numPlotPoints) +\
              "_" + units
        if logx:
            ret += "_logx"
        if logy:
            ret += "_logy"
        return ret + ".png"

    def _getdbase(self, start, end, numPlotPoints, units):
        if self.data.isDiscrete():
            if end is None:
                end = len(self.data)-1
            if numPlotPoints is None:
                numPlotPoints = end - start + 1
            dbase = self.data.createReducedLength(start, end, numPlotPoints)
        else:
            if end is None:
                end = 10.
            if numPlotPoints is None:
                numPlotPoints = 100
            dbase = self.data.discretise(start, end, numPlotPoints)
    
        if units is not None:
            dbase = dbase.convertUnits(units)
        return dbase, start, end, numPlotPoints

    def _plot(self, dbase, start, end, numPlotPoints, i, j, logx, logy, imag, 
              show):
        if i is not None and j is not None:
            dbase = dbase.createReducedDim(i).createReducedDim(j)
        elif i is not None:
            dbase = dbase.createReducedDim(i)
        elif j is not None:
            dbase = dbase.createReducedDim(j, True)
        self._setChartParameters(dbase)
        savePath = None
        if self.archiveRoot is not None:
            savePath = self.archiveRoot+dbase.chartTitle
            savePath += self._getSaveString(start, end, numPlotPoints, logx, 
                                            logy, dbase.units)
            self.log.writeMsg("Chart saved to: "+savePath)
        dbase.plot(logx, logy, imag, show, savePath)

    ##### Public API #####

    def plotSmatrix(self, start=0, end=None, numPlotPoints=None, units=None,
                    i=None, j=None, logx=False, logy=False, imag=False, 
                    show=True):
        """
        Plots the S-matrix.
    
        Parameters
        ----------
        start / end : int or float, optional
            Indicate the start and end points to perform he plot between. If the
            Tool data is in discrete form then will either indicate the start/
            end index (if int) or the nearest start/end energy (if float). If
            the Tool data is in continuous form then will indicate the start/end
            energy.
        numPlotPoints : int, optional
            The number of points to plot, evenly distributed between start and
            end.
        units : int, optional
            If specified, then will convert to these units prior to plotting.
            Available options are ResKit.RYDs, ResKit.HARTs and ResKit.eVs.
        i : int, optional
            Zero-based row index to plot. Default is to plot all rows.
        j : int, optional
            Zero-based column index to plot. Default is to plot all columns.
        logx : bool
            Switch to turn on x-axis log plotting.
        logy : bool
            Switch to turn on y-axis log plotting.
        imag : bool
            Switch to plot the imaginary component. By default just plots the
            real component.
        show : bool
            Switch whether to show the chart or not. If False chart will be
            saved into the archive if there is an archiveRoot.
        """
        self._writeCall(start, end, numPlotPoints, units, i, j, logx, logy,
                        imag, show, "plotSmatrix")
        dmat,start,end,numPlotPoints = self._getdbase(start, end, numPlotPoints,
                                                      units)
        dmat = dmat.to_dSmat()
        self._plot(dmat, start, end, numPlotPoints, i, j, logx, logy, imag,
                   show)
        self.log.writeCallEnd("plotSmatrix")

    def plotKmatrix(self, start=0, end=None, numPlotPoints=None, units=None,
                    i=None, j=None, logx=False, logy=False, imag=False, 
                    show=True):
        """
        Plots the K-matrix. See docs for plotSmatrix for further details.
        """
        self._writeCall(start, end, numPlotPoints, units, i, j, logx, logy, 
                        imag, show, "plotKmatrix")
        dmat,start,end,numPlotPoints = self._getdbase(start, end, numPlotPoints,
                                                      units)
        dmat = dmat.to_dKmat()
        self._plot(dmat, start, end, numPlotPoints, i, j, logx, logy, imag,
                   show)
        self.log.writeCallEnd("plotKmatrix")

    def plotTmatrix(self, start=0, end=None, numPlotPoints=None, units=None,
                    i=None, j=None, logx=False, logy=False, imag=False,
                    show=True):
        """
        Plots the T-matrix. See docs for plotSmatrix for further details.
        """
        self._writeCall(start, end, numPlotPoints, units, i, j, logx, logy, 
                        imag, show, "plotTmatrix")
        dmat,start,end,numPlotPoints = self._getdbase(start, end, numPlotPoints,
                                                      units)
        dmat = dmat.to_dTmat()
        self._plot(dmat, start, end, numPlotPoints, i, j, logx, logy, imag,
                   show)
        self.log.writeCallEnd("plotTmatrix")

    def plotUniOpSMat(self, start=0, end=None, numPlotPoints=None, units=None, 
                     i=None, j=None, logx=False, logy=False, imag=False,
                     show=True):
        """
        Plots the S-matrix following the unitary operation. See docs for
        plotSmatrix for further details.
        """
        self._writeCall(start, end, numPlotPoints, units, i, j, logx, logy, 
                        imag, show, "plotUniOpMat")
        dmat,start,end,numPlotPoints = self._getdbase(start, end, numPlotPoints,
                                                      units)
        dmat = dmat.to_dUniOpMat()
        self._plot(dmat, start, end, numPlotPoints, i, j, logx, logy, imag,
                   show)
        self.log.writeCallEnd("plotUniOpMat")

    def plotRaw(self, start=0, end=None, numPlotPoints=None, units=None, i=None,
                j=None, logx=False, logy=False, imag=False, show=True):
        """
        Plots whatever form the Tool data happes to be in. See docs for
        plotSmatrix for further details.
        """
        self._writeCall(start, end, numPlotPoints, units, i, j, logx, logy, 
                        imag, show, "plotRaw")
        dmat,start,end,numPlotPoints = self._getdbase(start, end, numPlotPoints,
                                                      units)
        self._plot(dmat, start, end, numPlotPoints, i, j, logx, logy, imag,
                   show)
        self.log.writeCallEnd("plotRaw")

    def plotEPhase(self, start=0, end=None, numPlotPoints=None, units=None,
                   i=None, j=None, logx=False, logy=False, imag=False, 
                   show=True):
        """
        Plots the eigenphase. See docs for plotSmatrix for further details.
        """
        self._writeCall(start, end, numPlotPoints, units, i, j, logx, logy,
                        imag, show, "plotEPhase")
        dmat,start,end,numPlotPoints = self._getdbase(start, end, numPlotPoints,
                                                      units)
        dmat = dmat.to_dEPhaseMat()
        self._plot(dmat, start, end, numPlotPoints, i, j, logx, logy, imag,
                   show)
        self.log.writeCallEnd("plotEPhase")

    def plotXS(self, start=0, end=None, numPlotPoints=None, units=None, i=None,
               j=None, logx=False, logy=False, show=True):
        """
        Plots the cross section. See docs for plotSmatrix for further details.
        Note that there is no imag parameter for this function.
        """
        self._writeCall(start, end, numPlotPoints, units, i, j, logx, logy,
                        imag, show, "plotXS")
        dmat,start,end,numPlotPoints = self._getdbase(start, end, numPlotPoints,
                                                      units)
        dmat = dmat.to_dXSmat()
        self._plot(dmat, start, end, numPlotPoints, i, j, logx, logy, imag,
                   show)
        self.log.writeCallEnd("plotXS")

    def plotTotalXS(self, start=0, end=None, numPlotPoints=None, units=None, 
                    logx=False, logy=False, show=True):
        """
        Plots the cross section. See docs for plotSmatrix for further details.
        Note that there are no i, j, and imag parameters for this function.
        """
        self._writeCall(start, end, numPlotPoints, units, None, None, logx,
                        logy, False, show, "plotTotalXS")
        dmat,start,end,numPlotPoints = self._getdbase(start, end, numPlotPoints,
                                                      units)
        dval = dmat.to_dXSmat().to_dTotXSval()
        self._plot(dval, start, end, numPlotPoints, None, None, logx, logy,
                   False, show)
        self.log.writeCallEnd("plotTotalXS")
