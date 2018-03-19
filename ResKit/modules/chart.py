import yaml

import os
import sys
resultsRoot = None
configDef = os.path.dirname(os.path.realpath(__file__)) + "/chart-default.yml"
parmaFilePaths = [configDef]

def _setChartParameters(dMat_plot, title):
    if title is not None:
        dMat_plot.setChartTitle(title)
    with open(parmaFilePaths[0], 'r') as f:
        config = yaml.load(f.read())
        dMat_plot.setChartParameters(colourCycle=config["colourCycle"])
        dMat_plot.setChartParameters(legPrefix=config["legPrefix"])
        dMat_plot.setChartParameters(useMarker=config["useMarker"])
        dMat_plot.setChartParameters(xsize=config["xsize"])
        dMat_plot.setChartParameters(ysize=config["ysize"])

def _getSaveString(startIndex, endIndex, numPoints, units, row, col, logx, logy,
                   imag):
    ret = "_" + str(startIndex) + "_" + str(endIndex) + "_" + str(numPoints) +\
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

def _plot(dmat_, startIndex, endIndex, numPoints, units, row, col, logx, logy, 
          imag, title, show):
    
    if endIndex is None:
        endIndex = len(dmat_)-1
    if numPoints is None:
        numPoints = endIndex - startIndex + 1
    if numPoints != len(dmat_):
        ris = dmat_.calculateReductionIndices(startIndex,endIndex,numPoints)[0]
        dmat_ = dmat_[ris[0]:ris[1]:ris[2]]

    if units is not None:
        dmat_ = dmat_.convertUnits(units)
    else:
        units = dmat_.units

    if row is not None and col is not None:
        dmat_ = dmat_.reduce(row).reduce(col)
    elif row is not None:
        dmat_ = dmat_.reduce(row)
    elif col is not None:
        dmat_ = dmat_.reduce(row, True)
    _setChartParameters(dmat_, title)
    savePath = None
    if resultsRoot is not None:
        savePath = resultsRoot + "/" + dmat_.chartTitle
        savePath += _getSaveString(startIndex, endIndex, numPoints, units, row,
                                   col, logx, logy, imag)
    dmat_.plot(logx, logy, imag, show, savePath)

def plotSmatrix(dMat, startIndex=0, endIndex=None, numPoints=None, units=None,
                row=None, col=None, logx=False, logy=False, imag=False, 
                title=None, show=True):
    dMat_plot = dMat.to_dSmat()
    _plot(dMat_plot, startIndex, endIndex, numPoints, units, row, col, logx, 
          logy, imag, title, show)

def plotKmatrix(dMat, startIndex=0, endIndex=None, numPoints=None, units=None,
                row=None, col=None, logx=False, logy=False, imag=False, 
                title=None, show=True):
    dMat_plot = dMat.to_dKmat()
    _plot(dMat_plot, startIndex, endIndex, numPoints, units, row, col, logx, 
          logy, imag, title, show)

def plotTmatrix(dMat, startIndex=0, endIndex=None, numPoints=None, units=None,
                row=None, col=None, logx=False, logy=False, imag=False, 
                title=None, show=True):
    dMat_plot = dMat.to_dTmat()
    _plot(dMat_plot, startIndex, endIndex, numPoints, units, row, col, logx, 
          logy, imag, title, show)

def plotXS(dMat, startIndex=0, endIndex=None, numPoints=None, units=None,
                row=None, col=None, logx=False, logy=False, imag=False, 
                title=None, show=True):
    dMat_plot = dMat.to_dXSmat()
    _plot(dMat_plot, startIndex, endIndex, numPoints, units, row, col, logx, 
          logy, imag, title, show)

def plotEPhase(dMat, startIndex=0, endIndex=None, numPoints=None, units=None,
                row=None, col=None, logx=False, logy=False, imag=False, 
                title=None, show=True):
    dMat_plot = dMat.to_dEPhaseMat()
    _plot(dMat_plot, startIndex, endIndex, numPoints, units, row, col, logx, 
          logy, imag, title, show)

def plotUniOpMat(startIndex=0, endIndex=None, numPoints=None, units=None,
                row=None, col=None, logx=False, logy=False, imag=False, 
                title=None, show=True):
    dMat_plot = dMat.to_dUniOpMat()
    _plot(dMat_plot, startIndex, endIndex, numPoints, units, row, col, logx, 
          logy, imag, title, show)

