import os
import sys
fileDir = os.path.dirname(os.path.realpath(__file__))
rkPath = fileDir+'/../../../..'
sys.path.insert(0,rkPath)

import shutil

import ukrmolmatreader as rmol
import twochanradialwell as rw
import reskit as rk

use_pyrazine = True

if sys.argv[1] == "mpmath":
    rk.use_mpmath_types()
    print "mpmath"
else:
    print "python"


TEST_ROOT = "chart"
if os.path.isdir(TEST_ROOT):
    shutil.rmtree(TEST_ROOT)

if sys.argv[2] == "radwell":
    calc = rk.get_asym_calc(rk.hartrees, [0,0])
    csmat = rw.get_Smat_fun(1.0,2.0,2.0,calc,1.0)
    dmat = rk.get_dmat_from_continuous(rk.Smat, csmat, calc, 1., 8., 200,
                                       "radwell")
else:
    # This data is only available in the distribution package.
    if sys.argv[2] == "pyrazine":
        input_data_file = "../../../../examples/kmatrix_input_pyrazine.txt"
        calc = rk.get_asym_calc(rk.rydbergs, [3,5,5])
    else:
        input_data_file = "../../../../examples/kmatrix_input_pbq.txt"
        calc = rk.get_asym_calc(rk.rydbergs, [1,3,3])
    kmatdict,_ = rmol.read_Kmats(input_data_file)
    dmat = rk.get_dmat_from_discrete(rk.Kmat, kmatdict, calc, "PBQ")


sfittool = rk.get_tool(rk.mcsmatfit, dmat, TEST_ROOT)

csmat = sfittool.get_elastic_Smat(10)

print "S matrix"
print "All elements. Default number of points"
sfittool.plot_Smat_fit(csmat)
print "All elements"
sfittool.plot_Smat_fit(csmat, 100)
print "Row eVs"
sfittool.plot_Smat_fit(csmat, 100, units=rk.eVs, i=1)
print "Column hartrees imaginary"
sfittool.plot_Smat_fit(csmat, 100, units=rk.hartrees, j=0, imag=True)
print "Element"
sfittool.plot_Smat_fit(csmat, 100, i=1, j=0)
print "Element logx"
sfittool.plot_Smat_fit(csmat, 100, i=1, j=0, logx=True)
print "Element imaginary logx and logy"
sfittool.plot_Smat_fit(csmat, 100, i=1, j=0, logx=True, logy=True, imag=True)

print "XS"
print "Default number of points"
sfittool.plot_XS_fit(csmat)
print "100 points"
sfittool.plot_XS_fit(csmat, 100)
print "eVs"
sfittool.plot_XS_fit(csmat, 100, units=rk.eVs)
print "logx and logy"
sfittool.plot_XS_fit(csmat, 100, logx=True, logy=True)

print "EigenPhase"
print "Default number of points"
sfittool.plot_EigenPhase_fit(csmat)
print "100 points"
sfittool.plot_EigenPhase_fit(csmat, 100)
print "eVs"
sfittool.plot_EigenPhase_fit(csmat, 100, units=rk.eVs)
print "logx and logy"
sfittool.plot_EigenPhase_fit(csmat, 100, logx=True, logy=True)

print ("Plot all data as S-matrix using yml config and save to archive. "
       "Plot using more points than in disrete set.")
sfittool = rk.get_tool(rk.mcsmatfit, dmat, TEST_ROOT)
sfittool.plot_Smat_fit(csmat, num_plot_points=600)

print "\nTest new config changes"
print "Plot dashed lines, high dpi."
sfittool = rk.get_tool(rk.mcsmatfit, dmat, TEST_ROOT, "v1_2_0_1.yaml")
sfittool.plot_Smat_fit(csmat)

print "Plot dashed fitted, no title as pdf."
sfittool = rk.get_tool(rk.mcsmatfit, dmat, TEST_ROOT, "v1_2_0_2.yaml")
sfittool.plot_Smat_fit(csmat)

print "Plot cycled dashed fitted, no title as pdf."
sfittool = rk.get_tool(rk.mcsmatfit, dmat, TEST_ROOT, "v1_2_0_3.yaml")
sfittool.plot_Smat_fit(csmat)

print "\nTest old config"
sfittool = rk.get_tool(rk.mcsmatfit, dmat, TEST_ROOT, "v1_1_1.yaml")
csmat = sfittool.get_elastic_Smat(10)
sfittool.plot_Smat_fit(csmat)
sfittool.plot_XS_fit(csmat, units=rk.eVs)
sfittool.plot_EigenPhase_fit(csmat, logx=True, logy=True)

cqmat = sfittool.get_elastic_Qmat(10)
print "Q matrix"
print "All elements. Default number of points"
sfittool.plot_Qmat_fit(cqmat)
print "All elements"
sfittool.plot_Qmat_fit(cqmat, 100)
print "Row eVs"
sfittool.plot_Qmat_fit(cqmat, 100, units=rk.eVs, i=1)
print "Column hartrees"
sfittool.plot_Qmat_fit(cqmat, 100, units=rk.hartrees, j=0)
print "Element"
sfittool.plot_Qmat_fit(cqmat, 100, i=1, j=0)
print "Element logx"
sfittool.plot_Qmat_fit(cqmat, 100, i=1, j=0, logx=True)
print "Element logx and logy"
sfittool.plot_Qmat_fit(cqmat, 100, i=1, j=0, logx=True, logy=True)

print "Q matrix eigenvalues"
print "All elements. Default number of points"
sfittool.plot_Qmat_evals_fit(cqmat)
print "All elements hartrees"
sfittool.plot_Qmat_evals_fit(cqmat, 100, units=rk.hartrees)
print "Row eVs"
sfittool.plot_Qmat_evals_fit(cqmat, 100, units=rk.eVs, i=1)
print "Element logx"
sfittool.plot_Qmat_evals_fit(cqmat, 100, i=1, logx=True)
print "Element logx and logy"
sfittool.plot_Qmat_evals_fit(cqmat, 100, i=1, logx=True, logy=True)
