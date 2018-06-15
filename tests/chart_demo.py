import os
import sys
import shutil

import reskit as rk
rk.safeMode = False
import channelutil as cu
import twochanradialwell as rw

TEST_ROOT = "chart-demo"
if os.path.isdir(TEST_ROOT):
    shutil.rmtree(TEST_ROOT)

#### python Types ####
cal = cu.AsymCalc(cu.hartrees, [0,0])
csmat = rw.get_Smat_fun(1.0,2.0,2.0,cal,1.0)
dsmat = csmat.discretise(1.,8.,100)

chart = rk.get_tool(rk.chart, dsmat)

print "Plot all data as S-matrix"
chart.plot_Smatrix()

print "Plot center data as S-matrix"
chart.plot_Smatrix(len(dsmat)/4,len(dsmat)*3/4)

print "Plot center data as S-matrix, five points only."
chart.plot_Smatrix(len(dsmat)/4,len(dsmat)*3/4,5)

print "Plot center data as S-matrix, five points only in eV."
chart.plot_Smatrix(len(dsmat)/4,len(dsmat)*3/4,5,cu.eVs)

print "Plot center data as T-matrix"
chart.plot_Tmatrix(len(dsmat)/4,len(dsmat)*3/4)

print "Plot center imag data as T-matrix"
chart.plot_Tmatrix(len(dsmat)/4,len(dsmat)*3/4,imag=True)

print "Plot center imag data as total cross section"
chart.plot_TotalXS(len(dsmat)/4,len(dsmat)*3/4)

print "Plot center data as S-matrix, 1,1 element, imag and both axis logged."
chart.plot_Smatrix(len(dsmat)/4,len(dsmat)*3/4,i=0,j=0,logx=True,logy=True,
                  imag=True)

print "Plot all data as K-matrix"
chart.plot_Kmatrix()
print "Plot all data as UniOp matrix"
chart.plot_UniOpSMat()
print "Plot all data as raw matrix"
chart.plot_raw()
print "Plot all data as cross section"
chart.plot_XS()

#### mpmath types ####
cu.use_mpmath_types()
rw.use_mpmath_types()
cal = cu.AsymCalc(cu.hartrees, [0,0])
csmat = rw.get_Smat_fun(1.0,2.0,2.0,cal,1.0)
chart = rk.get_tool(rk.chart, csmat)
print "Plot all mpmath data as S-matrix. Direct from continuous data."
chart.plot_Smatrix()

dsmat = csmat.discretise(1.,8.,100)
chart = rk.get_tool(rk.chart, dsmat)
print "Plot all mpmath data as S-matrix, this time discretised."
chart.plot_Smatrix()

# Check copy saved on file system
chart = rk.get_tool(rk.chart, dsmat, TEST_ROOT, "chart-demo.yaml")
print "Plot all mpmath data as S-matrix using yml config and saved to archive."
chart.plot_Smatrix()
print "This time as T-matrix but don't show."
chart.plot_Tmatrix(show=False)
