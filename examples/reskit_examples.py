import sys

import reskit as rk
import channelutil as cu
import ukrmolmatreader as rmol
import twochanradialwell as tcrw

archive_path = "results"

exceptStr = ("\n\nBad arguments. Should be: \"python reskit_examples.py 1st")+\
            (" 2nd\", where:\n 1st: Scattering system. Either: ")+\
            ("\n  radwell, pyrazine, uracil6ch or uracil10ch\n 2nd: Command. ")+\
            ("Either:\n  poles, plotSmat or plotTotXS.\n Eg: python")+\
            (" reskit_examples.py radwell poles")
if len(sys.argv) != 3:
    raise Exception(exceptStr)

if sys.argv[1] == "radwell":
    input_data_file = None
    desc_str = "radwell"
    ang_mom = [0,0]
    sl = None
elif sys.argv[1] == "pyrazine":
    input_data_file = "kmatrix_input_pyrazine.dat"
    desc_str = "pyrazine"
    ang_mom = [3,5,5]
    sl = slice(0,1200)
elif sys.argv[1] == "uracil6ch":
    input_data_file = "kmatrix_input_uracil6ch.dat"
    desc_str = "uracil6ch"
    ang_mom = [1,2,2,3,3,3]
    sl = None
elif sys.argv[1] == "uracil10ch":
    input_data_file = "kmatrix_input_uracil10ch.dat"
    desc_str = "uracil10ch"
    ang_mom = [0,1,1,2,2,2,3,3,3,3]
    sl = None
else:
    raise Exception(exceptStr)

# Use mpmath types (optional)
rk.use_mpmath_types()

if input_data_file is None:
  # System is a radial well
  # Get a calculator with units and channel angular momentum
  calc = rk.get_asym_calc(rk.hartrees, ang_mom)
  # Get a function pointer for the S matrix
  csmat = tcrw.get_Smat_fun(1.0, 2.0, 2.0, calc, 1.0)
  # Initialise the data into the required container
  dmat = rk.get_dmat_from_continuous(rk.Smat, csmat, calc, 1., 8., 1000,
                                      desc_str)
  paramPath = "radwell_poles.yml"
else:
  # System is a molecule
  # Read in the K matrix data
  # Get a calculator with units and channel angular momentum
  calc = rk.get_asym_calc(rk.rydbergs, ang_mom)
  kmatdict,_ = rmol.read_Kmats(input_data_file)
  # Initialise the data into the required container
  dmat = rk.get_dmat_from_discrete(rk.Kmat, kmatdict, calc, desc_str)
  paramPath = None

# Slice the data set
if sl is not None:
    dmat = dmat[sl]

sfittool = rk.get_tool(rk.mcsmatfit, dmat, archive_path, paramPath)
if sys.argv[2] == "poles":
  # Perform the calculation of the poles and the quality indicators
  cfins = sfittool.get_elastic_Fins(range(2,32,2))
  sfittool.find_stable_Smat_poles(cfins)
elif sys.argv[2] == "plotSmat" or sys.argv[2] == "plotTotXS":
  sfittool = rk.get_tool(rk.mcsmatfit, dmat, archive_path)
  # Perform the calculation of the poles and the quality indicators
  csmat = sfittool.get_elastic_Smat(20)
  if sys.argv[2] == "plotSmat":
    sfittool.plot_Smat_fit(csmat, num_plot_points=300)
  else:
    sfittool.plot_totXS_fit(csmat, num_plot_points=300, logy=True)
else:
    raise Exception(exceptStr)
