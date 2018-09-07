import os
import sys
filedir = os.path.dirname(os.path.realpath(__file__))
modpath = filedir+'/tools' # Keep tools before utilities
sys.path.insert(0,filedir+os.sep+'tools')
if os.path.isdir(filedir+os.sep+'utilities'):
    sys.path.insert(0,filedir+os.sep+'utilities')

import channelutil as cu
import tisutil as tu
import pynumwrap as nw
import toolhelper as th
from reskit.release import __version__

# Changing the types after a tool has been created renders old tools in an
# undefined state and they should not be used. safe_mode prevents changing type
# after tools have been created.
safe_mode = True

Smat = tu.Smat
Kmat = tu.Kmat
Tmat = tu.Tmat

rydbergs = cu.rydbergs
hartrees = cu.hartrees
eVs = cu.eVs

filename_checkdata = "checkdata.dat"

reskit_err_str_unrecog_module = "Reskit Error. Unrecognised module."

reskit_err_str_typ_chg = "Reskit Error. Types can only be changed at start " \
+ "of session in safe_mode."

reskit_err_str_bad_data_root = "Reskit Archive Error. Supplied data does not " \
+ "correspond to that used to originally create the data root. The data " \
+ "associated with the source_str supplied to the get_dmat_from_discrete or " \
+ "get_dmat_from_continuous functions must not change between subsequent " \
+ "calculations.\n\nTO FIX: Either provide a different source_str for your " \
+ "new data or ensure the correct data has been supplied to the get_tool " \
+ "function."

reskit_err_str_missing_check_data_1 = "Reskit Archive Error. Data root with no " \
+ filename_checkdata + " file. There must always be a " + filename_checkdata \
+ " file contained in each data root. This is used to check that the same " \
+ "data is being used for successive calculations.\n\nTO FIX: Either check " \
+ "there are no required files in the folder: "
reskit_err_str_missing_check_data_2 = " and then delete it or provide a " \
+ "different source_str for your data to the get_dmat_from_discrete or " \
+ "get_dmat_from_continuous functions."

def get_asym_calc(units, angmoms=None, tot_spin=None, targ_spins=None):
    """
    Returns an AsymCalc for converting from momentum to energy.

    Parameters
    ----------
    units : int
        Specification of the energy units. Available options are
        reskit.rydbergs, reskit.hartrees and reskit.eVs.
    angmoms : list of ints, optional
        Specification of the angular momenta in each of the channels. Defaults 
        to zero in all channels.
    tot_spin : float, optional
        Specification of the total spin of the system. Defaults to 0.5. Only
        required for calculation of cross sections.
    targ_spins : float or list of floats, optional
        Specification of the spin of the target (e.g. electronic) state
        associated with each of the channels. Defaults to zero in all channels.
        Only required for calculation of cross sections.

    Returns
    -------
    asymcalc : AsymCalc
    """
    return cu.AsymCalc(units, angmoms, tot_spin, targ_spins)

def get_dmat_from_discrete(mat_type, mat_dict, asymcalc, source_str):
    """
    Converts discrete energy dependent scattering data into a reskit compatible
    container (ie. dSmat, dTmat or dKmat). Types must match those specified
    using the use_python_types or use_mpmath_types functions.

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
    compatible container (ie. dSmat, dTmat or dKmat). Types must match those
    specified using the use_python_types or use_mpmath_types functions.

    Parameters
    ----------
    mat_type : int 
        As for get_dmat_from_discrete.
    fun_ref : function with float parameter
        An energy function describing the elements of the scattering matrix. Can
        be either python float or mpmath.mpf type.
    asymcalc : AsymCalc
        As for get_dmat_from_discrete.
    start_ene : float
        Start energy for the discretisation.
    end_ene : float
        End energy for the discretisation.
    num_points : float
        Number of energy points for the discretisation.
    source_str : str
        As for get_dmat_from_discrete.

    Returns
    -------
    dmat : dBase
    """
    cmat = tu.get_continuous_scattering_matrix(mat_type, fun_ref, asymcalc, 
                                               source_str)
    return cmat.discretise(start_ene, end_ene, num_points)

chart = 0
mcsmatfit = 1
def get_tool(toolid, data, archive_root=None, param_file_path=None, 
             silent=False):
    """
    Initialises and returns a Tool.

    Parameters
    ----------
    toolid : int 
        Specification of the Tool. Available options are reskit.chart and
        reskit.mcsmatfit.
    data
        Tool data. This is the data container to be used by the Tool.
    archive_root : str, optional
        Specification of the location into which reskit will write its results.
    param_file_path : str, optional
        Location of an existing yaml file containing overrides for the more
        advanced routine parameters.
    silent : bool, optional
        Switch determining whether to suppress output to console.

    Returns
    -------
    tool : Tool
    """
    if safe_mode:
        nw.lockType()
    if toolid == chart:
        import chart as mod
        tool = mod.Chart
    elif toolid == mcsmatfit:
        import mcsmatfit as mod
        tool = mod.MCSMatFit
    else:
        raise Exception(reskit_err_str_unrecog_module)
    if archive_root is not None:
        data_root = archive_root+os.sep+data.get_source_str()+os.sep
        data_root += nw.getConfigString()+os.sep+data.get_hist_str()+os.sep
        archive_root = data_root+mod.toolName+os.sep
        if not os.path.isdir(data_root):
            os.makedirs(data_root)
            with th.fwopen(data_root+filename_checkdata) as f:
                th.fw(f, data.get_check_str())
        else:
            if os.path.isfile(data_root+filename_checkdata):
                with th.fropen(data_root+filename_checkdata) as f:
                    if str(f.read()) != str(data.get_check_str()):
                        raise Exception(reskit_err_str_bad_data_root)
            else:
                s = reskit_err_str_missing_check_data_1 + data_root
                s += reskit_err_str_missing_check_data_2
                raise Exception(s)
        if not os.path.isdir(archive_root):
            os.makedirs(archive_root)

    return tool(data, archive_root, param_file_path, silent)

def use_python_types():
    """
    Specifies to use python types.
    """
    try:
        nw.use_python_types()
    except:
        raise Exception(reskit_err_str_typ_chg)

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
        raise Exception(reskit_err_str_typ_chg)
