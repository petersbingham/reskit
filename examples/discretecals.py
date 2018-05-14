import sys

import reskit as rk
import channelutil as cu
import ukrmolmatreader as rmol

if len(sys.argv) != 2:
    raise Exception("Specify the molecule as a command line argument")
archive_path = "results"
if sys.argv[1] == "pyrazine":
    input_data_file = "kmatrix_input_pyrazine.dat"
    desc_str = "pyrazine"
    ang_mom = [3,5,5]
    sl = slice(0,1200)
elif sys.argv[1] == "uracil6ch":
    input_data_file = "kmatrix_input_uracil6ch.dat"
    desc_str = "uracil6ch"
    ang_mom = [1,2,2,3,3,3]
    sl = None

# Use mpmath types (optional)
rk.use_mpmath_types()

# Read in the K matrix data
kmatdict,_ = rmol.read_Kmats(input_data_file)

# Get a calculator with units and channel angular momentum
calc = rk.get_asym_calc(rk.rydbergs, ang_mom)
# Initialise the data into the required container
dkmat = rk.get_dmat_from_discrete(rk.Kmat, kmatdict, calc, desc_str)
# Slice the data set (optional)
if sl is not None:
    dkmat2 = dkmat[sl]

sfittool = rk.get_tool(rk.mcsmatfit, dkmat2, archive_path)

# Perform the calculation of the poles and the qualityindicators
cfins = sfittool.get_elastic_Fins(range(2,32,2))
sfittool.find_stable_Smat_poles(cfins)
