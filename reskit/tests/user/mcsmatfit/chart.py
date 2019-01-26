import os
import sys
fileDir = os.path.dirname(os.path.realpath(__file__))
rkPath = fileDir+'/../../../..'
sys.path.insert(0,rkPath)

import shutil

import channelutil as cu
import ukrmolmatreader as rmol
import twochanradialwell as rw
import reskit as rk

if len(sys.argv) > 1 and sys.argv[1]=="mpmath":
    cu.use_mpmath_types()
    print "mpmath"
else:
    print "python"

TEST_ROOT = "chart"
if os.path.isdir(TEST_ROOT):
    shutil.rmtree(TEST_ROOT)

calc = cu.AsymCalc(cu.hartrees, [0,0])
csmat = rw.get_Smat_fun(1.0,2.0,2.0,calc,1.0)
dmat = rk.get_dmat_from_continuous(rk.Smat, csmat, calc, 1., 8., 200,
                                   "radwell")

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

print "Plot all data as S-matrix using yml config and save to archive."
sfittool = rk.get_tool(rk.mcsmatfit, dmat, TEST_ROOT)
sfittool.plot_Smat_fit(csmat)

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
