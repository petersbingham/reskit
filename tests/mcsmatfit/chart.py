import sys
import os
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
