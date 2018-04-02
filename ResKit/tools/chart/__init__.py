import yaml
import os
import copy

modeDir = os.path.dirname(os.path.realpath(__file__))
toolName = "chart"

class chart:
    def __init__(self, data, resultsRoot, parmaFilePath):
        self.data = copy.deepcopy(data)
        self.resultsRoot = resultsRoot
        self.parmaFilePath = parmaFilePath
        if self.parmaFilePath is None:
            self.parmaFilePath = modeDir+os.sep+"default.yml"

    def _setChartParameters(self, dMat_plot, title):
        if title is not None:
            dMat_plot.setChartTitle(title)
        with open(self.parmaFilePath, 'r') as f:
            config = yaml.load(f.read())
            dMat_plot.setChartParameters(colourCycle=config["colourCycle"])
            dMat_plot.setChartParameters(legPrefix=config["legPrefix"])
            dMat_plot.setChartParameters(useMarker=config["useMarker"])
            dMat_plot.setChartParameters(xsize=config["xsize"])
            dMat_plot.setChartParameters(ysize=config["ysize"])

    def _getSaveString(self, start, end, numPoints, units, row, col, logx, logy, 
                       imag):
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
        return ret

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
        if self.resultsRoot is not None:
            savePath = self.resultsRoot+os.sep+dmat.chartTitle
            savePath += self._getSaveString(start, end, numPoints, units, row,
                                            col, logx, logy, imag)
        dmat.plot(logx, logy, imag, show, savePath)

    ##### Public API #####

    def plotSmatrix(self, start=0, end=None, numPoints=None, units=None, 
                    row=None, col=None, logx=False, logy=False, imag=False, 
                    title=None, show=True):
        dmat,start,end,numPoints,units = self._getdmat(start, end, numPoints, 
                                                       units)
        dMat_plot = dmat.to_dSmat()
        self._plot(dMat_plot, start, end, numPoints, units, row, col, logx,
                   logy, imag, title, show)

    def plotKmatrix(self, start=0, end=None, numPoints=None, units=None, 
                    row=None, col=None, logx=False, logy=False, imag=False, 
                    title=None, show=True):
        dmat,start,end,numPoints,units = self._getdmat(start, end, numPoints, 
                                                       units)
        dMat_plot = dmat.to_dKmat()
        self._plot(dMat_plot, start, end, numPoints, units, row, col, logx, 
                   logy, imag, title, show)

    def plotTmatrix(self, start=0, end=None, numPoints=None, units=None, 
                    row=None, col=None, logx=False, logy=False, imag=False, 
                    title=None, show=True):
        dmat,start,end,numPoints,units = self._getdmat(start, end, numPoints, 
                                                       units)
        dMat_plot = dmat.to_dTmat()
        self._plot(dMat_plot, start, end, numPoints, units, row, col, logx, 
                   logy, imag, title, show)

    def plotXS(self, start=0, end=None, numPoints=None, units=None, row=None, 
               col=None, logx=False, logy=False, imag=False, title=None, 
               show=True):
        dmat,start,end,numPoints,units = self._getdmat(start, end, numPoints, 
                                                       units)
        dMat_plot = dmat.to_dXSmat()
        self._plot(dMat_plot, start, end, numPoints, units, row, col, logx, 
                   logy, imag, title, show)

    def plotEPhase(self, start=0, end=None, numPoints=None, units=None, 
                   row=None, col=None, logx=False, logy=False, imag=False, 
                   title=None, show=True):
        dmat,start,end,numPoints,units = self._getdmat(start, end, numPoints, 
                                                       units)
        dMat_plot = dmat.to_dEPhaseMat()
        self._plot(dMat_plot, start, end, numPoints, units, row, col, logx, 
                   logy, imag, title, show)

    def plotUniOpMat(self, start=0, end=None, numPoints=None, units=None, 
                     row=None, col=None, logx=False, logy=False, imag=False, 
                     title=None, show=True):
        dmat,start,end,numPoints,units = self._getdmat(start, end, numPoints, 
                                                       units)
        dMat_plot = dmat.to_dUniOpMat()
        self._plot(dMat_plot, start, end, numPoints, units, row, col, logx, 
                   logy, imag, title, show)
