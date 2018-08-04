import os
import sys
fileDir = os.path.dirname(os.path.realpath(__file__))
rootDir = fileDir+os.sep+".."+os.sep+".."+os.sep
sys.path.insert(0,rootDir)
sys.path.insert(0,rootDir+"tools")

from numpydoc.docscrape import FunctionDoc
import jinja2 as j

verbose = False

if verbose:
    from createlatex_verbose import *
else:
    from createlatex_brief import *

reskitfuns = ["get_asym_calc","get_dmat_from_discrete","get_dmat_from_continuous",\
              "get_tool","use_python_types","use_mpmath_types"]
chartfunctions = ["plot_Smatrix", "plot_Kmatrix", "plot_Tmatrix", "plot_UniOpSMat",\
                  "plot_raw", "plot_EphaseSum", "plot_XS"]
# Order important since substrings:
mcsmatfitfunctions = ["get_elastic_Fins", "find_Fin_roots", "find_stable_Smat_poles",\
                      "get_elastic_Smat", "plot_Smat_fit", "plot_XS_fit"]
# Order important since substrings:
codeTypes = ["reskit.", "rydbergs", "hartrees", "eVs", "chart", "mcsmatfit",\
             "archive_root", "AsymCalc", "dMat", "Tool", "cMatSympypolyk",\
             "cSMatSympypolyk","cSmat","dSmat","dKmat","dTmat",\
             "cFinMatSympypolyk"]
# These are globals in the reskit interface. Conflict with cSmat etc
subcodeTypes = ["Kmat", "Smat", "Tmat"]

try:
    os.remove("doc.txt")
except:
    pass

def clean_str(string):
    return string.replace("_","\_").replace("\\textit{  }","")\
                 .replace("(\\textit{})","")

def code_font_str(string):
    # Put codeTypes last since it includes substrings
    for repStr in reskitfuns+chartfunctions+mcsmatfitfunctions+codeTypes:
        string = string.replace(repStr,"\codefont{"+repStr+"}")
    for repStr in subcodeTypes:
        string = string.replace("}"+repStr,"}\codefont{"+repStr+"}")
    return string

def clean_fun_desc_str(string):
    ret_str = string.replace("0.5", "$\\frac{1}{2}$")
    ret_str = ret_str.replace(" Fin ", " $F^{in}$ ")
    ret_str = ret_str.replace(" Fin.", " $F^{in}$.")
    ret_str = ret_str.replace(" Fins ", " $F^{in}$s ")
    ret_str = ret_str.replace(" Fins.", " $F^{in}$s.")
    return ret_str

def write_function(func_name, doc, add_info, param_append, ignore_params):
    data = doc._parsed_data
    func_desc = " ".join(data["Summary"])
    if len(add_info) > 1:
        if add_info[1][0]:
            func_desc = add_info[1][1]
        else:
            func_desc += add_info[1][1]
    params_str = ""
    rets_str = ""
    param_dat = data["Parameters"]
    if len(param_dat) > 0:
        write_params = True
        if func_name in ignore_params:
            if ignore_params[func_name] is None:
                write_params = False
            elif len(param_dat) == len(ignore_params[func_name]):
                write_params = False
        if write_params:
            if verbose:
                params_str = params_str_start_doc_str
            for param in param_dat:
                if func_name not in ignore_params or\
                param not in ignore_params[func_name]:
                    if len(param[2]) > 0:
                        param_desc = " ".join(param[2])
                        if param[0] in param_append:
                            param_desc += " " + param_append[param[0]]
                        t = j.Template(params_doc_str)
                        param_str = t.render(PARAM_NAME=param[0],
                                             PARAM_TYPE=param[1],
                                             PARAM_DESC=code_font_str(param_desc))
                    else:
                        t = j.Template(param_doc_str)
                        param_str = t.render(PARAM_NAME=param[0],
                                             PARAM_TYPE=param[1])
                    params_str += param_str
    if verbose and len(data["Returns"]) > 0:
        rets_str = rets_strStartDocStr
        for ret in data["Returns"]:
            if len(ret[2]) > 0:
                t = j.Template(retsDocStr)
                ret_str = t.render(RET_NAME=ret[0], RET_TYPE=ret[1], 
                                  RET_DESC=" ".join(ret[2]))
            else:
                t = j.Template(retDocStr)
                ret_str = t.render(RET_NAME=ret[0], RET_TYPE=ret[1])
            if len(ret[1]) == 0:
                ret_str = ret_str.replace(":","")
            rets_str += ret_str

    if len(add_info) > 0:
        if add_info[0][0]:
            func_name = add_info[0][1]
        else:
            func_name += add_info[0][1]
    func_name = clean_str(func_name)
    func_desc = clean_str(code_font_str(func_desc))
    params_str = clean_str(params_str)
    rets_str = clean_str(rets_str)
    if len(params_str) > 0:
        t = j.Template(function_doc_str)
    else:
        t = j.Template(function_doc_str_no_param)
    if verbose:
        fun_desc_str = t.render(FUNCTION_NAME = func_name, 
                                FUNCTION_DESC = func_desc,
                                PARAMETERS_DESC = params_str, 
                                RETURNS_DESC = rets_str)
    else:
        if len(params_str) > 0:
            fun_desc_str = t.render(FUNCTION_NAME = func_name, 
                                    FUNCTION_DESC = func_desc,
                                    PARAMETERS_DESC = params_str)
        else:
            fun_desc_str = t.render(FUNCTION_NAME = func_name, 
                                    FUNCTION_DESC = func_desc)
    if len(data["Parameters"])==0 and (not verbose or len(data["Returns"])==0):
        fun_desc_str += "\n"
    with open("doc.txt", 'a') as f:
        f.write(clean_fun_desc_str(fun_desc_str)+"\n\n")    

def write_doc(mod, functions, name, add_info=None, param_append=None,
              ignore_params=None):
    if add_info is None:
        add_info = []
    if param_append is None:
        param_append = {}
    if ignore_params is None:
        ignore_params = []
    add_info.extend([[]]*(len(functions)-len(add_info)))
    for i,function in enumerate(functions):
        func_name = getattr(mod, function)
        doc = FunctionDoc(func_name)
        if verbose:
            name += "." + function
        else:
            name = function
        write_function(name, doc, add_info[i], param_append, ignore_params)

desc_str = (
r"The interface to reskit is through the \codefont{\_\_init\_\_.py} package "
r"file shown in Figure~\ref{fig:ClassDiagram}. This section provides a summary "
r"of the available functions. Some of these are employed when a discrete set of "
r"scattering data (generated by other codes) is used and some when an "
r"analytical expression is provided for these data. The parameters of each of "
r"the functions are listed and described.")
with open("doc.txt", 'a') as f:
    f.write(desc_str)  
    f.write("\n\n")
import reskit
# Using inspect loses order
write_doc(reskit, reskitfuns, "reskit")

desc_str = (
"\\subsection{Tools}\n\label{sec_Tools}\n\nIn this section we describe the "
"functionality provided as part of the Tools. MCSMatFit performs the analytic "
"fit and pole identification whereas Chart provides utilities for the basic "
"plotting of data.\n\n\\subsubsection{MCSMatFit}\n\nThese routines perform the "
"fit and identify the poles as described in Section~\\ref{sec:Method}.\n\n")
with open("doc.txt", 'a') as f:
    f.write(desc_str)  
import mcsmatfit
write_doc(mcsmatfit.MCSMatFit, mcsmatfitfunctions, "mcsmatfit")

desc_str = "\\subsubsection{Chart}\n\n"
with open("doc.txt", 'a') as f:
    f.write(desc_str)  
import chart
functions = ["plot_raw"]
collective_name = ", plot_Smatrix, plot_Kmatrix, plot_Tmatrix, "\
                  "plot_UniOpSMat, plot_EphaseSum, plot_XS"
collective_desc = "Plots various scattering related quantities. A png image "\
                  "of the plot will be automatically saved into the archive."
add_info = [[(False, collective_name), (True, collective_desc)]]
write_doc(chart.Chart, functions, "chart", add_info)

desc_str = (
r"\noindent The \codefont{i} and \codefont{j} parameters are only available "
r"when the quantity to plot is a matrix (ie not for \codefont{plot\_Ephase} "
r"and \codefont{plot\_XS}).")
with open("doc.txt", 'a') as f:
    f.write(desc_str)
