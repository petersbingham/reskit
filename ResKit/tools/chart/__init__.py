import yaml

import os
resultsRoot = None
modeDir = os.path.dirname(os.path.realpath(__file__))
parmaFilePath = modeDir+os.sep+"default.yml"

toolName = "chart"

def _setChartParameters(dMat_plot, title):
    if title is not None:
        dMat_plot.setChartTitle(title)
    with open(parmaFilePath, 'r') as f:
        config = yaml.load(f.read())
        dMat_plot.setChartParameters(colourCycle=config["colourCycle"])
        dMat_plot.setChartParameters(legPrefix=config["legPrefix"])
        dMat_plot.setChartParameters(useMarker=config["useMarker"])
        dMat_plot.setChartParameters(xsize=config["xsize"])
        dMat_plot.setChartParameters(ysize=config["ysize"])

def _getSaveString(start, end, numPoints, units, row, col, logx, logy, imag):
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

def _getdmat(mat, start, end, numPoints, units):
    if mat.isDiscrete():
        if end is None:
            end = len(mat)-1
        if numPoints is None:
            numPoints = end - start + 1
        dmat = mat.createReducedLength(start, end, numPoints)
    else:
        if end is None:
            end = 10.
        if numPoints is None:
            numPoints = 100
        dmat = mat.discretise(start, end, numPoints)

    if units is not None:
        dmat = dmat.convertUnits(units)
    else:
        units = dmat.units
    return dmat, start, end, numPoints, units

def _plot(dmat, start, end, numPoints, units, row, col, logx, logy, imag, title,
          show):
    if row is not None and col is not None:
        dmat = dmat.createReducedDim(row).createReducedDim(col)
    elif row is not None:
        dmat = dmat.createReducedDim(row)
    elif col is not None:
        dmat = dmat.createReducedDim(row, True)
    _setChartParameters(dmat, title)
    savePath = None
    if resultsRoot is not None:
        saveDir = resultsRoot+os.sep+toolName
        if not os.path.isdir(saveDir):
            os.makedirs(saveDir)
        savePath = saveDir+os.sep+dmat.chartTitle
        savePath += _getSaveString(start, end, numPoints, units, row,
                                   col, logx, logy, imag)
    dmat.plot(logx, logy, imag, show, savePath)

def plotSmatrix(mat, start=0, end=None, numPoints=None, units=None, row=None, 
                col=None, logx=False, logy=False, imag=False, title=None, 
                show=True):
    dmat,start,end,numPoints,units = _getdmat(mat, start, end, numPoints, units)
    dMat_plot = dmat.to_dSmat()
    _plot(dMat_plot, start, end, numPoints, units, row, col, logx, logy, imag, 
          title, show)

def plotKmatrix(mat, start=0, end=None, numPoints=None, units=None, row=None, 
                col=None, logx=False, logy=False, imag=False, title=None, 
                show=True):
    dmat,start,end,numPoints,units = _getdmat(mat, start, end, numPoints, units)
    dMat_plot = dmat.to_dKmat()
    _plot(dMat_plot, start, end, numPoints, units, row, col, logx, logy, imag, 
          title, show)

def plotTmatrix(mat, start=0, end=None, numPoints=None, units=None, row=None, 
                col=None, logx=False, logy=False, imag=False, title=None, 
                show=True):
    dmat,start,end,numPoints,units = _getdmat(mat, start, end, numPoints, units)
    dMat_plot = dmat.to_dTmat()
    _plot(dMat_plot, start, end, numPoints, units, row, col, logx, logy, imag, 
          title, show)

def plotXS(mat, start=0, end=None, numPoints=None, units=None, row=None, 
           col=None, logx=False, logy=False, imag=False, title=None, show=True):
    dmat,start,end,numPoints,units = _getdmat(mat, start, end, numPoints, units)
    dMat_plot = dmat.to_dXSmat()
    _plot(dMat_plot, start, end, numPoints, units, row, col, logx, logy, imag, 
          title, show)

def plotEPhase(mat, start=0, end=None, numPoints=None, units=None, row=None, 
               col=None, logx=False, logy=False, imag=False, title=None, 
               show=True):
    dmat,start,end,numPoints,units = _getdmat(mat, start, end, numPoints, units)
    dMat_plot = dmat.to_dEPhaseMat()
    _plot(dMat_plot, start, end, numPoints, units, row, col, logx, logy, imag, 
          title, show)

def plotUniOpMat(mat, start=0, end=None, numPoints=None, units=None, row=None, 
                 col=None, logx=False, logy=False, imag=False, title=None, 
                 show=True):
    dmat,start,end,numPoints,units = _getdmat(mat, start, end, numPoints, units)
    dMat_plot = dmat.to_dUniOpMat()
    _plot(dMat_plot, start, end, numPoints, units, row, col, logx, logy, imag, 
          title, show)
