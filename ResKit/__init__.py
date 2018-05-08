import os
import sys
fileDir = os.path.dirname(os.path.realpath(__file__))
modPath = fileDir+'/tools' # Keep tools before utilities
sys.path.insert(0,modPath)
depPath = fileDir+'/utilities'
sys.path.insert(0,depPath)

import channelutil as cu
import tisutil as tu
import pynumwrap as nw
import toolhelper as th

# Changing the types after a tool has been created renders old tools in an
# undefined state and they should not be used. safeMode prevents changing type
# after tools have been created.
safeMode = True

Smat = tu.Smat
Kmat = tu.Kmat
Tmat = tu.Tmat

RYDs = cu.RYDs
HARTs = cu.HARTs
eVs = cu.eVs

def getAsymCalc(units, ls=None):
    """
    Returns an asymCal for converting from wavenumber to energy.

    Parameters
    ----------
    units : int
        Specification of the energy units. Available options are ResKit.RYDs,
        ResKit.HARTs and ResKit.eVs.
    ls : list of ints, optional
        Specification of the angular momenta in each of the channels. Defaults 
        to zero in all channels.

    Returns
    -------
    asymcal : channelutil.asymCal
    """
    return cu.asymCal(units, ls)

def getdMatFromDiscrete(matType, matDict, asymCal, sourceStr):
    """
    Converts discrete energy dependent scattering data into a ResKit compatible
    container. Types must match those specified using the usePythonTypes or
    useMpmathTypes functions.

    Parameters
    ----------
    matType : int 
        Specification of the scattering matrix type. Available options are
        ResKit.Smat, ResKit.Kmat and ResKit.Tmat.
    matDict :  dict of scattering matrices keyed by energy.
        Scattering data to be used in the calculation. Can be either floats or
        mpmath types.
    asymCal : asymCal
        As returned from the getAsymCalc function.
    sourceStr : str
        String provided to uniquely identify the scattering data. Will be used
        in the archiving of results.

    Returns
    -------
    dmat : tisutil.dBase
    """
    return tu.getDiscreteScatteringMatrix(matType, matDict, asymCal, sourceStr)

def getdMatFromContinuous(matType, funPtr, asymCal, startEne, endEne, numPoints,
                          sourceStr):
    """
    Discretises continuous energy dependent scattering data into a ResKit
    compatible container. Types must match those specified using the
    usePythonTypes or useMpmathTypes functions.

    Parameters
    ----------
    matType : int 
        Specification of the scattering matrix type. Available options are
        ResKit.Smat, ResKit.Kmat and ResKit.Tmat.
    funPtr : function reference with energy parameter
        A function of energy that will calculate the scattering matrix. Can be
        either floats or mpmath types.
    asymCal : asymCal
        As returned from the getAsymCalc function.
    startEne : float
        Start energy for the discretisation.
    endEne : float
        End energy for the discretisation.
    numPoints : float
        Number of energy points for the discretisation.
    sourceStr : str
        String provided to uniquely identify the scattering data. Will be used
        in the archiving of results.

    Returns
    -------
    dmat : tisutil.dBase
    """
    cmat = tu.getContinuousScatteringMatrix(matType, funPtr, asymCal, sourceStr)
    return cmat.discretise(startEne, endEne, numPoints)

CHART = 0
SFIT_MC_RAK = 1
def getTool(toolID, data, archiveRoot=None, paramFilePath=None, silent=False):
    """
    Initialises and returns a tool.

    Parameters
    ----------
    toolID : int 
        Specification of the tool. Available options are ResKit.CHART and
        ResKit.SFIT_MC_RAK.
    data
        Tool data. The format of this data is determined by the Tool type.
    archiveRoot : str, optional
        Specification of the root location into which ResKit will write it's
        results.
    paramFilePath : str, optional
        Location of an existing yml file containing overrides for the more
        advanced routine parameters.
    silent : bool, optional
        Switch determining whether to suppress output to console.

    Returns
    -------
    tool : Tool
    """
    if safeMode:
        nw.lockType()
    if toolID == CHART:
        import chart as mod
        tool = mod.chart
    elif toolID == SFIT_MC_RAK:
        import sfit_mc_rak as mod
        tool = mod.sfit_mc_rak
    else:
        raise Exception("Unrecognised module.")
    if archiveRoot is not None:
        dataRoot = archiveRoot+os.sep+data.getSourceStr()+os.sep
        dataRoot += nw.getConfigString()+os.sep+data.getHistStr()+os.sep
        archiveRoot = dataRoot+mod.toolName+os.sep
        if not os.path.isdir(dataRoot):
            os.makedirs(dataRoot)
            with th.fwopen(dataRoot+"checkdata.dat") as f:
                th.fw(f, data.getCheckStr())
        else:
            if os.path.isfile(dataRoot+"checkdata.dat"):
                with th.fropen(dataRoot+"checkdata.dat") as f:
                    if str(f.read()) != str(data.getCheckStr()):
                        s = "Supplied data does not correspond to that used "
                        s += "to originally create the dataRoot."
                        raise Exception(s)
            else:
                s = "Invalid archive state: data dir with no checkdata.dat."
                raise Exception(s)
        if not os.path.isdir(archiveRoot):
            os.makedirs(archiveRoot)

    return tool(data, archiveRoot, paramFilePath, silent)

def usePythonTypes(dps=nw.dps_default_python):
    """
    Specifies to use python types.
    """
    try:
        nw.usePythonTypes(dps)
    except:
        s = "Types can only be changed at start of session in safeMode."
        raise Exception(s)

def useMpmathTypes(dps=nw.dps_default_mpmath):
    """
    Specifies to use mpmath types.

    Parameters
    ----------
    dps : int 
        Specifies the mpmath precision.
    """
    try:
        nw.useMpmathTypes(dps)
    except:
        s = "Types can only be changed at start of session in safeMode."
        raise Exception(s)

# If overridden, will look for the modules in the site-utilities first.
utilityOverride = False
def overrideUtilities():
    global utilityOverride
    if not utilityOverride:
        sys.path.remove(depPath)
        sys.path.append(depPath)
        utilityOverride = True
        reload(cu)
        reload(tu)
        reload(nw)
