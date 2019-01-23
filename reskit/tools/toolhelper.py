import os
import datetime
import io
import copy
import yaml
import platform
import matplotlib.pyplot as plt
from cycler import cycler
import sys

import numpy
import scipy
import sympy
import mpmath
import matplotlib
import yaml
import tabulate

import channelutil
import matfuncutil
import parsmat
import pynumutil
import pynumwrap
import stelempy
import tisutil
import twochanradialwell
import ukrmolmatreader
import reskit

class tool:
    def __init__(self, data, archive_root, param_file_path, tool_dir, silent):
        self.data = copy.deepcopy(data)
        self.archive_root = archive_root
        self.param_file_path = param_file_path
        if self.param_file_path is None:
            self.param_file_path = tool_dir+os.sep+"default.yaml"
        if self.archive_root is not None:
            self.log = Logger(self._get_log_file_path())
            if not silent:
                print self._get_log_file_path()
        else:
            self.log = Logger(None)

    def _get_log_file_path(self):
        return self.archive_root+"calc.log"

    def _get_config_cache_name(self):
        return "config.yaml"

    def _does_param_cache_match(self, cache_dir, param_key):
        with fropen(self.param_file_path) as f:
            config = yaml.load(f.read())

            if os.path.isdir(cache_dir):
                try:
                    cachePath = cache_dir+os.sep+self._get_config_cache_name()
                    with fropen(cachePath) as f:
                        p = config[param_key]
                        p_str = str(p)
                        p_cache_str = f.read()
                        return p_cache_str == p_str
                except Exception as inst:
                    self._file_error(str(inst))
        return False

    def _verify_param_cache(self, cache_dir, param_key):
        if os.path.isdir(cache_dir) and\
        not self._does_param_cache_match(cache_dir, param_key):
            self._config_error()

    def _config_error(self):
        estr = "Reskit Archive Error. Configuration contained in " \
        + self.param_file_path + " conflicts with a prior configuration with " \
        + "the same file name. All config files associated with a given data " \
        + "set must have unique names (these are specified as the " \
        + "param_file_path in the get_tool function).\n\nTO FIX: Uniquely " \
        + "rename the file: " + self.param_file_path + "."
        self.log.write_err(estr)
        raise Exception(estr)

    def _file_error(self, estr):
        msg = "Reskit File Error. Exception opening cache config: " + estr
        self.log.write_err(msg)
        raise Exception(msg)

    def _prepare_for_fit_plot(self, num_plot_points):
        with fropen(self.param_file_path) as f:
            config = yaml.load(f.read())
            p = config["fit_charts"]
            self.log.write_parameters(p)
    
            if num_plot_points is None:
                ln = len(self.data)
            else:
                ln = num_plot_points

            orig = self.data
            if num_plot_points is not None:
                orig = orig.create_reduced_length(num_points=ln)
            return p, ln, orig

    def _plot_fit(self, p, title, orig, fit_pnts, fit, num_plot_points, units,
                  y_axis_lbl, logx, logy, imag):
        xsize = p["xsize"]
        ysize = p["ysize"]

        fig = plt.figure(facecolor="white")
        if not imag:
            fig.suptitle(title)
        else:
            fig.suptitle(title + " imag")
        fig.set_size_inches(xsize, ysize, forward=True)
        valsize = orig.valsize()
        if len(p["colour_cycle"])!=3 or valsize==1:
            plt.gca().set_prop_cycle(cycler('color', p["colour_cycle"]))
        else:
            cyc = p["colour_cycle"]
            new_cyc = []
            for col in cyc:
                new_cyc.extend([col]*valsize)
            plt.gca().set_prop_cycle(cycler('color', new_cyc))

        if units is not None:
            orig = orig.convert_ene_units(units)
            fit_pnts = fit_pnts.convert_ene_units(units)
            fit = fit.convert_ene_units(units)
        else:
            units = orig.x_units

        ls1,_ = orig.get_plot_info(logx, logy, imag)
        fit_pnts.set_chart_parameters(use_marker=True)
        ls2,_ = fit.get_plot_info(logx, logy, imag)
        ls3,_ = fit_pnts.get_plot_info(logx, logy, imag)

        plt.legend([ls1[0],ls2[0],ls3[0]], ["Original","Fitted","Fit points"], 
                   prop={'size': 12})
        plt.xlabel("Energy (" + orig.x_units + ")", fontsize=12)
        plt.ylabel(y_axis_lbl, fontsize=12)
        if self.archive_root is not None:
            save_path = self.archive_root+"charts"+os.sep
            if not os.path.isdir(save_path):
                os.makedirs(save_path)
            save_path += title + "_" + units
            if logx:
                save_path += "_logx"
            if logy:
                save_path += "_logy"
            if num_plot_points is None:
                num_plot_points = len(self.data)
            save_path += "_" + str(num_plot_points)
            save_path += ".png"
            self.log.write_msg("Chart saved to: "+save_path)
            plt.savefig(save_path, bbox_inches='tight')
            matfuncutil.set_plot_paths(fig, save_path, True)
        if p["show"]:
            plt.show()

    def _reduceDimensions(self, dbase, i, j):
        if i is not None and j is not None:
            dbase = dbase.create_reduced_dim(i).create_reduced_dim(j)
        elif i is not None:
            dbase = dbase.create_reduced_dim(i)
        elif j is not None:
            dbase = dbase.create_reduced_dim(j, True)
        return dbase

class Logger:
    def __init__(self, log_file_path):
        self.log_file_path = log_file_path
        self.write("NEW SESSION: " + platform.platform() + " " +\
                   platform.processor() + ", Python " + sys.version,
                   start="\n\n")
        self.write("VERSIONS: " + self._get_version_strings() + "\n",
                   start="\n")

    def _vstr(self, package, start=False):
        vstr = ""
        if not start:
            vstr = ", "
        return vstr + package.__name__ + ":" + package.__version__

    def _get_version_strings(self):
        vstr = self._vstr(numpy,True) + self._vstr(scipy) + self._vstr(sympy) +\
               self._vstr(mpmath) + self._vstr(matplotlib) + self._vstr(yaml) +\
               self._vstr(tabulate) +\
               self._vstr(channelutil) + self._vstr(matfuncutil) +\
               self._vstr(parsmat) + self._vstr(pynumutil) +\
               self._vstr(pynumwrap) + self._vstr(stelempy) +\
               self._vstr(tisutil) + self._vstr(twochanradialwell) +\
               self._vstr(ukrmolmatreader) + self._vstr(reskit)
        return vstr

    def write(self, msg, start=""):
        if self.log_file_path is not None:
            with faopen(self.log_file_path) as f:
                fw(f, start + get_date_time_string() + ": " + msg)

    def write_call(self, fun_str, internal=False):
        start = ""
        if not internal:
            start = "\n"
        msg = fun_str + "\n"
        self.write(msg, start)

    def write_call_end(self, fun_str):
        msg = fun_str + " end\n"
        self.write(msg)

    def write_msg(self, msg):
        msg = "  " + msg + "\n"
        self.write(msg)

    def write_err(self, msg):
        msg = "  Error: " + msg + "\n"
        self.write(msg)

    def write_parameters(self, params):
        msg = "  Using parameters: " + str(params) + "\n"
        self.write(msg)

def fropen(file_name):
    return io.open(file_name, 'r', newline='\n', encoding="utf-8")
def fwopen(file_name):
    return io.open(file_name, 'w', newline='\n', encoding="utf-8")
def faopen(file_name):
    return io.open(file_name, 'a', newline='\n', encoding="utf-8")
def fw(f, o):
    f.write(unicode(o))

def cfg_name(path):
    return os.path.splitext(path)[0].split(os.sep)[-1]

def get_date_time_string():
    return str(datetime.datetime.now())[:-3]

def get_sub_dirs(directory):
    return os.listdir(directory)
