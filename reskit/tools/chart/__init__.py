import yaml
import os

import toolhelper as th

toolDir = os.path.dirname(os.path.realpath(__file__))
toolName = "chart"

class Chart(th.tool):
    def __init__(self, data, archive_root, param_file_path, silent):
        th.tool.__init__(self, data, archive_root, param_file_path, toolDir,
                         silent)

    def _write_call(self, start, end, num_plot_points, units, i, j, logx, logy,
                    imag, show, funName):
        self.log.write_call(funName+"("+str(start)+","+str(end)+","\
                           +str(num_plot_points)+","+str(units)+","+str(i)+","\
                           +str(j)+","+str(logx)+","+str(logy)+","+str(imag)\
                           +","+str(show)+")")

    def _set_chart_parameters(self, dbase):
        with open(self.param_file_path, 'r') as f:
            config = yaml.load(f.read())
            self.log.write_parameters(config)
            dbase.set_chart_parameters(colour_cycle=config["colour_cycle"])
            dbase.set_chart_parameters(leg_prefix=config["leg_prefix"])
            dbase.set_chart_parameters(use_marker=config["use_marker"])
            dbase.set_chart_parameters(xsize=config["xsize"])
            dbase.set_chart_parameters(ysize=config["ysize"])

    def _get_save_string(self, start, end, num_plot_points, logx, logy, units):
        ret = " " + str(start) + "_" + str(end) + "_" + str(num_plot_points) +\
              "_" + units
        if logx:
            ret += "_logx"
        if logy:
            ret += "_logy"
        return ret + ".png"

    def _getdbase(self, start, end, num_plot_points, units):
        if self.data.is_discrete():
            if end is None:
                end = len(self.data)-1
            if num_plot_points is None:
                num_plot_points = end - start + 1
            dbase = self.data.create_reduced_length(start, end, num_plot_points)
        else:
            if end is None:
                end = 10.
            if num_plot_points is None:
                num_plot_points = 100
            dbase = self.data.discretise(start, end, num_plot_points)
    
        if units is not None:
            dbase = dbase.convert_ene_units(units)
        return dbase, start, end, num_plot_points

    def _plot(self, dbase, start, end, num_plot_points, i, j, logx, logy, imag, 
              show):
        dbase = self._reduceDimensions(dbase, i, j)
        self._set_chart_parameters(dbase)
        save_path = None
        if self.archive_root is not None:
            save_path = self.archive_root+dbase.chart_title
            save_path += self._get_save_string(start, end, num_plot_points, logx, 
                                              logy, dbase.x_units)
            self.log.write_msg("Chart saved to: "+save_path)
        dbase.plot(logx, logy, imag, show, save_path)

    ##### Public API #####

    def plot_Smatrix(self, start=0, end=None, num_plot_points=None, units=None,
                     i=None, j=None, logx=False, logy=False, imag=False, 
                     show=True):
        """
        Plots the S-matrix. There are additional advanced parameters in the
        tool yml file.
    
        Parameters
        ----------
        start / end : int or float, optional
            Indicates the start and end points to perform the plot between. If
            the Tool data is in discrete form it indicates the start / end index
            (if int) or the nearest start / end energy (if float). If the Tool
            data is in continuous form it indicates the start / end energy.
        num_plot_points : int, optional
            The number of points to plot, evenly distributed between start and
            end.
        units : int, optional
            If specified, then will convert to these units prior to plotting.
            Available options are reskit.rydbergs, reskit.hartrees and
            reskit.eVs.
        i : int, optional
            Zero-based row index to plot. Default is to plot all rows.
        j : int, optional
            Zero-based column index to plot. Default is to plot all columns.
        logx : bool, optional
            Switch to turn on x-axis log plotting.
        logy : bool, optional
            Switch to turn on y-axis log plotting.
        imag : bool, optional
            Switch to plot the imaginary component. By default just plots the
            real component.
        show : bool, optional
            Switch whether to show the chart or not. If False chart will still 
            be saved into the archive if there is an archive_root.
        """
        self._write_call(start, end, num_plot_points, units, i, j, logx, logy,
                         imag, show, "plot_Smatrix")
        dmat,start,end,num_plot_points = self._getdbase(start, end, 
                                                        num_plot_points, units)
        dmat = dmat.to_dSmat()
        self._plot(dmat, start, end, num_plot_points, i, j, logx, logy, imag,
                   show)
        self.log.write_call_end("plot_Smatrix")

    def plot_Kmatrix(self, start=0, end=None, num_plot_points=None, units=None,
                     i=None, j=None, logx=False, logy=False, imag=False, 
                     show=True):
        """
        Plots the K-matrix. See docs for plot_Smatrix for further details.
        """
        self._write_call(start, end, num_plot_points, units, i, j, logx, logy, 
                         imag, show, "plot_Kmatrix")
        dmat,start,end,num_plot_points = self._getdbase(start, end, 
                                                        num_plot_points, units)
        dmat = dmat.to_dKmat()
        self._plot(dmat, start, end, num_plot_points, i, j, logx, logy, imag,
                   show)
        self.log.write_call_end("plot_Kmatrix")

    def plot_Tmatrix(self, start=0, end=None, num_plot_points=None, units=None,
                     i=None, j=None, logx=False, logy=False, imag=False,
                     show=True):
        """
        Plots the T-matrix. See docs for plot_Smatrix for further details.
        """
        self._write_call(start, end, num_plot_points, units, i, j, logx, logy, 
                         imag, show, "plot_Tmatrix")
        dmat,start,end,num_plot_points = self._getdbase(start, end, 
                                                        num_plot_points, units)
        dmat = dmat.to_dTmat()
        self._plot(dmat, start, end, num_plot_points, i, j, logx, logy, imag,
                   show)
        self.log.write_call_end("plot_Tmatrix")

    def plot_UniOpSMat(self, start=0, end=None, num_plot_points=None, 
                       units=None, i=None, j=None, logx=False, logy=False, 
                       imag=False, show=True):
        """
        Plots the S-matrix following the unitary operation. See docs for
        plot_Smatrix for further details.
        """
        self._write_call(start, end, num_plot_points, units, i, j, logx, logy, 
                         imag, show, "plotUniOpMat")
        dmat,start,end,num_plot_points = self._getdbase(start, end, 
                                                        num_plot_points, units)
        dmat = dmat.to_dUniOpMat()
        self._plot(dmat, start, end, num_plot_points, i, j, logx, logy, imag,
                   show)
        self.log.write_call_end("plotUniOpMat")

    def plot_raw(self, start=0, end=None, num_plot_points=None, units=None,
                 i=None, j=None, logx=False, logy=False, imag=False, show=True):
        """
        Plots whatever form the Tool data happes to be in. See docs for
        plot_Smatrix for further details.
        """
        self._write_call(start, end, num_plot_points, units, i, j, logx, logy, 
                         imag, show, "plot_raw")
        dmat,start,end,num_plot_points = self._getdbase(start, end, 
                                                        num_plot_points, units)
        self._plot(dmat, start, end, num_plot_points, i, j, logx, logy, imag,
                   show)
        self.log.write_call_end("plot_raw")

    def plot_Ephase(self, start=0, end=None, num_plot_points=None, units=None,
                    i=None, j=None, logx=False, logy=False, imag=False, 
                    show=True):
        """
        Plots the eigenphase. See docs for plot_Smatrix for further details.
        """
        self._write_call(start, end, num_plot_points, units, i, j, logx, logy,
                         imag, show, "plot_Ephase")
        dmat,start,end,num_plot_points = self._getdbase(start, end, 
                                                        num_plot_points, units)
        dmat = dmat.to_dEPhaseMat()
        self._plot(dmat, start, end, num_plot_points, i, j, logx, logy, imag,
                   show)
        self.log.write_call_end("plot_Ephase")

    def plot_XS(self, start=0, end=None, num_plot_points=None, units=None, 
                logx=False, logy=False, show=True):
        """
        Plots the cross section. See docs for plot_Smatrix for further details.
        Note that there are no i, j, and imag parameters for this function.
        """
        self._write_call(start, end, num_plot_points, units, None, None, logx,
                         logy, False, show, "plot_XS")
        dmat,start,end,num_plot_points = self._getdbase(start, end,
                                                        num_plot_points, units)
        dsca = dmat.to_dXSsca()
        self._plot(dsca, start, end, num_plot_points, None, None, logx, logy,
                   False, show)
        self.log.write_call_end("plot_XS")

    def plot_XSmat(self, start=0, end=None, num_plot_points=None, units=None,
                   i=None, j=None, logx=False, logy=False, show=True):
        """
        Plots the cross section matrix. See docs for plot_Smatrix for further
        details. Note that there is no imag parameter for this function.
        """
        self._write_call(start, end, num_plot_points, units, i, j, logx, logy,
                         False, show, "plot_XSmat")
        dmat,start,end,num_plot_points = self._getdbase(start, end, 
                                                        num_plot_points, units)
        dmat = dmat.to_dXSmat()
        self._plot(dmat, start, end, num_plot_points, i, j, logx, logy, False,
                   show)
        self.log.write_call_end("plot_XSmat")
