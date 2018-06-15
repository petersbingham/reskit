import reskit as rk
import channelutil as cu
import twochanradialwell as tcrw

calc = rk.get_asym_calc(rk.hartrees, [0,0])
csmat = tcrw.get_Smat_fun(1.0, 2.0, 2.0, calc, 1.0)
dmat = rk.get_dmat_from_continuous(rk.Smat, csmat, calc, 1., 8., 1200, "radwell")

sfittool = rk.get_tool(rk.mcsmatfit, dmat, "chart_Smat_fin_fit")
cfin = sfittool.get_elastic_Fin(10)

chart = rk.get_tool(rk.chart, cfin, "chart_Smat_fin_fit")
chart.plot_raw()
