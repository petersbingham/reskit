import yaml
import os

import toolhelper as th

toolDir = os.path.dirname(os.path.realpath(__file__))
toolName = "chart"

class chart(th.tool):
    def __init__(self, data, archiveRoot, paramFilePath, silent):
        th.tool.__init__(self, data, archiveRoot, paramFilePath, toolDir,
                         silent)

    def _writeCall(self, start, end, numPoints, units, row, col, logx, logy,
                   imag, title, show, funName):
        self.log.writeCall(funName+"("+str(start)+","+str(end)+","\
                           +str(numPoints)+","+str(units)+","+str(row)+","\
                           +str(col)+","+str(logx)+","+str(logy)+","+str(imag)\
                           +","+str(title)+","+str(show)+")")

    def _setChartParameters(self, dMat_plot, title):
        if title is not None:
            dMat_plot.setChartTitle(title)
        with open(self.paramFilePath, 'r') as f:
            config = yaml.load(f.read())
            self.log.writeParameters(config)
            dMat_plot.setChartParameters(colourCycle=config["colourCycle"])
            dMat_plot.setChartParameters(legPrefix=config["legPrefix"])
            dMat_plot.setChartParameters(useMarker=config["useMarker"])
            dMat_plot.setChartParameters(xsize=config["xsize"])
            dMat_plot.setChartParameters(ysize=config["ysize"])

    def _getSaveString(self, start, end, numPoints, row, col, logx, logy, imag,
                       units):
        ret = "_" + str(start) + "_" + str(end) + "_" + str(numPoints) +\
              "_" + units
        if row:
            ret += "_row" + str(row)
        if col:
            ret += "_col" + str(col)
        if logx:
            ret += "_logx"
        if logy:
            ret += "_logy"
        if imag:
            ret += "_imag"
        return ret + ".png"

    def _getdmat(self, start, end, numPoints, units):
        if self.data.isDiscrete():
            if end is None:
                end = len(self.data)-1
            if numPoints is None:
                numPoints = end - start + 1
            dmat = self.data.createReducedLength(start, end, numPoints)
        else:
            if end is None:
                end = 10.
            if numPoints is None:
                numPoints = 100
            dmat = self.data.discretise(start, end, numPoints)
    
        if units is not None:
            dmat = dmat.convertUnits(units)
        else:
            units = dmat.units
        return dmat, start, end, numPoints, units

    def _plot(self, dmat, start, end, numPoints, units, row, col, logx, logy,
              imag, title, show):
        if row is not None and col is not None:
            dmat = dmat.createReducedDim(row).createReducedDim(col)
        elif row is not None:
            dmat = dmat.createReducedDim(row)
        elif col is not None:
            dmat = dmat.createReducedDim(row, True)
        self._setChartParameters(dmat, title)
        savePath = None
        if self.archiveRoot is not None:
            savePath = self.archiveRoot+dmat.chartTitle
            savePath += self._getSaveString(start, end, numPoints, row, col, 
                                            logx, logy, imag, dMat_plot.units)
            self.log.writeMsg("Chart saved to: "+savePath)
        dmat.plot(logx, logy, imag, show, savePath)

    ##### Public API #####

    def plotSmatrix(self, start=0, end=None, numPoints=None, units=None,
                    row=None, col=None, logx=False, logy=False, imag=False,
                    title=None, show=True):
        self._writeCall(start, end, numPoints, units, row, col, logx, logy,
                        imag, title, show, "plotSmatrix")
        dmat,start,end,numPoints,units = self._getdmat(start, end, numPoints,
                                                       units)
        dMat_plot = dmat.to_dSmat()
        self._plot(dMat_plot, start, end, numPoints, units, row, col, logx,
                   logy, imag, title, show)
        self.log.writeCallEnd("plotSmatrix")

    def plotKmatrix(self, start=0, end=None, numPoints=None, units=None,
                    row=None, col=None, logx=False, logy=False, imag=False,
                    title=None, show=True):
        self._writeCall(start, end, numPoints, units, row, col, logx, logy,
                        imag, title, show, "plotKmatrix")
        dmat,start,end,numPoints,units = self._getdmat(start, end, numPoints,
                                                       units)
        dMat_plot = dmat.to_dKmat()
        self._plot(dMat_plot, start, end, numPoints, units, row, col, logx,
                   logy, imag, title, show)
        self.log.writeCallEnd("plotKmatrix")

    def plotTmatrix(self, start=0, end=None, numPoints=None, units=None,
                    row=None, col=None, logx=False, logy=False, imag=False,
                    title=None, show=True):
        self._writeCall(start, end, numPoints, units, row, col, logx, logy,
                        imag, title, show, "plotTmatrix")
        dmat,start,end,numPoints,units = self._getdmat(start, end, numPoints,
                                                       units)
        dMat_plot = dmat.to_dTmat()
        self._plot(dMat_plot, start, end, numPoints, units, row, col, logx,
                   logy, imag, title, show)
        self.log.writeCallEnd("plotTmatrix")

    def plotXS(self, start=0, end=None, numPoints=None, units=None, row=None,
               col=None, logx=False, logy=False, imag=False, title=None,
               show=True):
        self._writeCall(start, end, numPoints, units, row, col, logx, logy,
                        imag, title, show, "plotXS")
        dmat,start,end,numPoints,units = self._getdmat(start, end, numPoints,
                                                       units)
        dMat_plot = dmat.to_dXSmat()
        self._plot(dMat_plot, start, end, numPoints, units, row, col, logx,
                   logy, imag, title, show)
        self.log.writeCallEnd("plotXS")

    def plotEPhase(self, start=0, end=None, numPoints=None, units=None,
                   row=None, col=None, logx=False, logy=False, imag=False,
                   title=None, show=True):
        self._writeCall(start, end, numPoints, units, row, col, logx, logy,
                        imag, title, show, "plotEPhase")
        dmat,start,end,numPoints,units = self._getdmat(start, end, numPoints,
                                                       units)
        dMat_plot = dmat.to_dEPhaseMat()
        self._plot(dMat_plot, start, end, numPoints, units, row, col, logx,
                   logy, imag, title, show)
        self.log.writeCallEnd("plotEPhase")

    def plotUniOpMat(self, start=0, end=None, numPoints=None, units=None,
                     row=None, col=None, logx=False, logy=False, imag=False,
                     title=None, show=True):
        self._writeCall(start, end, numPoints, units, row, col, logx, logy,
                        imag, title, show, "plotUniOpMat")
        dmat,start,end,numPoints,units = self._getdmat(start, end, numPoints,
                                                       units)
        dMat_plot = dmat.to_dUniOpMat()
        self._plot(dMat_plot, start, end, numPoints, units, row, col, logx,
                   logy, imag, title, show)
        self.log.writeCallEnd("plotUniOpMat")

    def plotRaw(self, start=0, end=None, numPoints=None, units=None, row=None, 
                col=None, logx=False, logy=False, imag=False, title=None, 
                show=True):
        self._writeCall(start, end, numPoints, units, row, col, logx, logy,
                        imag, title, show, "plotRaw")
        dmat,start,end,numPoints,units = self._getdmat(start, end, numPoints,
                                                       units)
        self._plot(dmat, start, end, numPoints, units, row, col, logx, logy, 
                   imag, title, show)
        self.log.writeCallEnd("plotRaw")
