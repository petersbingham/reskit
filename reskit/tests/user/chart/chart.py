import os
import sys
fileDir = os.path.dirname(os.path.realpath(__file__))
rkPath = fileDir+'/../../../..'
sys.path.insert(0,rkPath)

import shutil

import reskit as rk
rk.safe_mode = False
import channelutil as cu
import twochanradialwell as rw

if len(sys.argv) > 1 and sys.argv[1]=="mpmath":
    cu.use_mpmath_types()
    print "mpmath"
else:
    print "python"
  
TEST_ROOT = "chart"
if os.path.isdir(TEST_ROOT):
    shutil.rmtree(TEST_ROOT)

cal = cu.AsymCalc(cu.hartrees, [0,0])
csmat = rw.get_Smat_fun(1.0,2.0,2.0,cal,1.0)
print "Plot all mpmath data as S-matrix, direct from continuous data. No archive"
chart = rk.get_tool(rk.chart, csmat)
chart.plot_Smatrix()

print "Use discretised data"
dsmat = csmat.discretise(1.,8.,100)
chart = rk.get_tool(rk.chart, dsmat)

print "Plot all data as S-matrix. No archive. Row."
chart.plot_Smatrix(i=0)

print "Archive created"
chart = rk.get_tool(rk.chart, dsmat, TEST_ROOT)

print "Plot all data as S-matrix. Column."
chart.plot_Smatrix(j=1)

print "Plot center data as S-matrix. Element."
chart.plot_Smatrix(len(dsmat)/4,len(dsmat)*3/4,i=0,j=1)

print "Plot center data as S-matrix, five points only."
chart.plot_Smatrix(len(dsmat)/4,len(dsmat)*3/4,5)

print "Plot center data as S-matrix, five points only in eV."
chart.plot_Smatrix(len(dsmat)/4,len(dsmat)*3/4,5,cu.eVs)

print "Plot center data as T-matrix."
chart.plot_Tmatrix(len(dsmat)/4,len(dsmat)*3/4)

print "Plot center imag data as T-matrix."
chart.plot_Tmatrix(len(dsmat)/4,len(dsmat)*3/4,imag=True)

print "Plot all data as cross section."
chart.plot_XS()
print "Plot center imag data as cross section. All parameters."
chart.plot_XS(len(dsmat)/4,len(dsmat)*3/4,50,cu.eVs,True,True)

print "Plot center data as S-matrix, 1,1 element, imag and both axis logged."
chart.plot_Smatrix(len(dsmat)/4,len(dsmat)*3/4,logx=True,logy=True,imag=True,
                   i=0,j=0)

print "Plot all data as K-matrix."
chart.plot_Kmatrix()
print "Plot all data as UniOp matrix."
chart.plot_UniOpSMat()
print "Plot all data as raw matrix."
chart.plot_raw()
print "Plot all data as cross section matrix."
chart.plot_XSmat()
print "Plot all data as eigenphase sum. Specifying rydbergs."
chart.plot_EphaseSum(units=rk.rydbergs)
print "Plot all data as cross section. Specifying Hartrees."
chart.plot_EphaseSum(units=rk.hartrees)
print "Plot all data as eigenphase matrix."
chart.plot_EphaseMat()

# Check copy saved on file system
chart = rk.get_tool(rk.chart, dsmat, TEST_ROOT, "chart.yaml")
print "Plot all mpmath data as S-matrix using yml config and save to archive."
chart.plot_Smatrix()
print "This time as T-matrix but don't show."
chart = rk.get_tool(rk.chart, dsmat, TEST_ROOT, "chart_noshow.yaml")
chart.plot_Tmatrix()
