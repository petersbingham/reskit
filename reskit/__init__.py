import os
import sys
filedir = os.path.dirname(os.path.realpath(__file__))
modpath = filedir+'/tools' # Keep tools before site-packages
sys.path.insert(0,modpath)

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

rydbergs = cu.rydbergs
hartrees = cu.hartrees
eVs = cu.eVs

def get_asym_calc(units, angmoms=None, tot_spin=None, targ_spins=None):
    """
    Returns an AsymCalc for converting from wavenumber to energy.

    Parameters
    ----------
    units : int
        Specification of the energy units. Available options are reskit.rydbergs,
        reskit.hartrees and reskit.eVs.
    angmoms : list of ints, optional
        Specification of the angular momenta in each of the channels. Defaults 
        to zero in all channels.
    tot_spin : int, optional
        Specification of the total spin of the system. Defaults to 0.5.
    targ_spins : int or list of ints, optional
        Specification of the spin of the target state spin in each of the
        channels. Defaults to zero in all channels.
    Returns
    -------
    asymcalc : AsymCalc
    """
    return cu.AsymCalc(units, angmoms, tot_spin, targ_spins)

def get_dmat_from_discrete(mat_type, mat_dict, asymcalc, source_str):
    """
    Converts discrete energy dependent scattering data into a reskit compatible
    container (dMat). Types must match those specified using the
    use_python_types or use_mpmath_types functions.

    Parameters
    ----------
    mat_type : int 
        Specification of the scattering matrix type. Available options are
        reskit.Smat, reskit.Kmat and reskit.Tmat.
    mat_dict : energy dict of scattering matrices
        Scattering data to be used in the calculation. Can be either floats or
        mpmath types.
    asymcalc : AsymCalc
        As returned from the get_asym_calc function.
    source_str : str
        String provided to uniquely identify the scattering data. Will be used
        in the archiving of results.

    Returns
    -------
    dmat : dBase
    """
    return tu.get_discrete_scattering_matrix(mat_type, mat_dict, asymcalc,
                                             source_str)

def get_dmat_from_continuous(mat_type, fun_ref, asymcalc, start_ene, end_ene, 
                             num_points, source_str):
    """
    Discretises continuous energy dependent scattering data into a reskit
    compatible container (dMat). Types must match those specified using the
    use_python_types or use_mpmath_types functions.

    Parameters
    ----------
    mat_type : int 
        Specification of the scattering matrix type. Available options are
        reskit.Smat, reskit.Kmat and reskit.Tmat.
    fun_ref : function with float parameter
        A function of energy that will calculate the scattering matrix. Can be
        either floats or mpmath types.
    asymcalc : AsymCalc
        As returned from the get_asym_calc function.
    start_ene : float
        Start energy for the discretisation.
    end_ene : float
        End energy for the discretisation.
    num_points : float
        Number of energy points for the discretisation.
    source_str : str
        String provided to uniquely identify the scattering data. Will be used
        in the archiving of results.

    Returns
    -------
    dmat : dBase
    """
    cmat = tu.get_continuous_scattering_matrix(mat_type, fun_ref, asymcalc, 
                                               source_str)
    return cmat.discretise(start_ene, end_ene, num_points)

chart = 0
mcsmatfit = 1
def get_tool(toolID, data, archive_root=None, param_file_path=None, 
             silent=False):
    """
    Initialises and returns a Tool.

    Parameters
    ----------
    toolID : int 
        Specification of the Tool. Available options are reskit.chart and
        reskit.mcsmatfit.
    data
        Tool data. The type of this data is determined by the Tool.
    archive_root : str, optional
        Specification of the root location into which reskit will write its
        results.
    param_file_path : str, optional
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
    if toolID == chart:
        import chart as mod
        tool = mod.Chart
    elif toolID == mcsmatfit:
        import mcsmatfit as mod
        tool = mod.MCSMatFit
    else:
        raise Exception("Unrecognised module.")
    if archive_root is not None:
        data_root = archive_root+os.sep+data.get_source_str()+os.sep
        data_root += nw.getConfigString()+os.sep+data.get_hist_str()+os.sep
        archive_root = data_root+mod.toolName+os.sep
        if not os.path.isdir(data_root):
            os.makedirs(data_root)
            with th.fwopen(data_root+"checkdata.dat") as f:
                th.fw(f, data.get_check_str())
        else:
            if os.path.isfile(data_root+"checkdata.dat"):
                with th.fropen(data_root+"checkdata.dat") as f:
                    if str(f.read()) != str(data.get_check_str()):
                        s = "Supplied data does not correspond to that used "
                        s += "to originally create the data_root."
                        raise Exception(s)
            else:
                s = "Invalid archive state: data dir with no checkdata.dat."
                raise Exception(s)
        if not os.path.isdir(archive_root):
            os.makedirs(archive_root)

    return tool(data, archive_root, param_file_path, silent)

def use_python_types(dps=nw.dps_default_python):
    """
    Specifies to use python types.
    """
    try:
        nw.use_python_types(dps)
    except:
        s = "Types can only be changed at start of session in safeMode."
        raise Exception(s)

def use_mpmath_types(dps=nw.dps_default_mpmath):
    """
    Specifies to use mpmath types.

    Parameters
    ----------
    dps : int 
        Specifies the mpmath precision.
    """
    try:
        nw.use_mpmath_types(dps)
    except:
        s = "Types can only be changed at start of session in safeMode."
        raise Exception(s)
