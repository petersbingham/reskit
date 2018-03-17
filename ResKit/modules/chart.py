dMat = None
resultsPath = None

def _plot(dmat_, startIndex=0, endIndex=None, numPoints=None, units=None,
          row=None, col=None):
    if startIndex is not None or endIndex is not None or numPoints is not None:
        if startIndex is None:
            startIndex = 0
        if endIndex is None:
            endIndex = len(dmat_)-1
        if numPoints is None:
            numPoints = endIndex - startIndex + 1
        ris = dSmat.calculateReductionIndices(startIndex,endIndex,numPoints)[0]
        dMat_plot = dmat_[ris[0]:ris[1]:ris[2]]
    else:
        dMat_plot = dmat_

    if units is not None:
        dMat_plot = dMat_plot.convertUnits(units)

    if row is not None and col is not None:
        dMat_plot = dMat_plot.reduce(row).reduce(col).plot()
    elif row is not None:
        dMat_plot = dMat_plot.reduce(row)
    elif col is not None:
        dMat_plot = dMat_plot.reduce(row, True)
    dMat_plot.plot()

def plotSmatrix(dMat, startIndex=0, endIndex=None, numPoints=None, units=None,
                row=None, col=None):
    dMat_plot = dMat.to_dSmat()
    self._plot(dMat_plot, startIndex, endIndex, numPoints, units, row, col)

def plotKmatrix(dMat, startIndex=0, endIndex=None, numPoints=None, units=None,
                row=None, col=None):
    dMat_plot = dMat.to_dKmat()
    self._plot(dMat_plot, startIndex, endIndex, numPoints, units, row, col)

def plotTmatrix(dMat, startIndex=0, endIndex=None, numPoints=None, units=None,
                row=None, col=None):
    dMat_plot = dMat.to_dTmat()
    self._plot(dMat_plot, startIndex, endIndex, numPoints, units, row, col)

def plotXS(dMat, startIndex=0, endIndex=None, numPoints=None, units=None,
                row=None, col=None):
    dMat_plot = dMat.to_dXSmat()
    self._plot(dMat_plot, startIndex, endIndex, numPoints, units, row, col)

def plotEPhase(dMat, startIndex=0, endIndex=None, numPoints=None, units=None,
                row=None, col=None):
    dMat_plot = dMat.to_dEPhaseMat()
    self._plot(dMat_plot, startIndex, endIndex, numPoints, units, row, col)

def plotUniOpMat(startIndex=0, endIndex=None, numPoints=None, units=None,
                row=None, col=None):
    dMat_plot = dMat.to_dUniOpMat()
    self._plot(dMat_plot, startIndex, endIndex, numPoints, units, row, col)

