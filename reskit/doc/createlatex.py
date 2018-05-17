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
                  "plot_raw", "plot_Ephase", "plot_XS", "plot_TotalXS"]
# Order important since substrings:
mcsmatfitfunctions = ["get_elastic_Fins", "get_elastic_Fin", "find_Fin_roots",\
                      "find_stable_Smat_poles", "get_elastic_Smat", "plot_Smat_fit",\
                      "plot_totXS_fit"]
# Order important since substrings:
codeTypes = ["reskit.rydbergs", "reskit.hartrees", "reskit.eVs", "Kmat",\
             "Tmat", "chart", "mcsmatfit", "archive_root", "AsymCalc", "dMat",\
             "Tool", "cPolykmat", "cPolySmat","Smat"]

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
    return string

def write_function(func_name, doc, add_info, param_append):
    data = doc._parsed_data
    func_desc = " ".join(data["Summary"])
    if len(add_info) > 1:
        if add_info[1][0]:
            func_desc = add_info[1][1]
        else:
            func_desc += add_info[1][1]
    params_str = ""
    rets_str = ""
    if len(data["Parameters"]) > 0:
        if verbose:
            params_str = params_str_start_doc_str
        for param in data["Parameters"]:
            if len(param[2]) > 0:
                param_desc = " ".join(param[2])
                if param[0] in param_append:
                    param_desc += " " + param_append[param[0]]
                t = j.Template(params_doc_str)
                param_str = t.render(PARAM_NAME=param[0], PARAM_TYPE=param[1],
                                     PARAM_DESC=code_font_str(param_desc))
            else:
                t = j.Template(param_doc_str)
                param_str = t.render(PARAM_NAME=param[0], PARAM_TYPE=param[1])
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

    t = j.Template(function_doc_str)
    if len(add_info) > 0:
        if add_info[0][0]:
            func_name = add_info[0][1]
        else:
            func_name += add_info[0][1]
    func_name = clean_str(func_name)
    func_desc = clean_str(code_font_str(func_desc))
    params_str = clean_str(params_str)
    rets_str = clean_str(rets_str)
    if verbose:
        fun_desc_str = t.render(FUNCTION_NAME = func_name, 
                                FUNCTION_DESC = func_desc,
                                PARAMETERS_DESC = params_str, 
                                RETURNS_DESC = rets_str)
    else:
        fun_desc_str = t.render(FUNCTION_NAME = func_name, 
                                FUNCTION_DESC = func_desc,
                                PARAMETERS_DESC = params_str)
    if len(data["Parameters"])==0 and (not verbose or len(data["Returns"])==0):
        fun_desc_str += "\n"
    with open("doc.txt", 'a') as f:
        f.write(fun_desc_str+"\n\n")    

def write_doc(mod, functions, name, add_info=None, param_append=None):
    if add_info is None:
        add_info = []
    if param_append is None:
        param_append = {}
    add_info.extend([[]]*(len(functions)-len(add_info)))
    for i,function in enumerate(functions):
        func_name = getattr(mod, function)
        doc = FunctionDoc(func_name)
        if verbose:
            name += "." + function
        else:
            name = function
        write_function(name, doc, add_info[i], param_append)

with open("doc.txt", 'a') as f:
    f.write("**** RESKIT DOCS ****\n")  
import reskit
# Using inspect loses order
write_doc(reskit, reskitfuns, "reskit")

with open("doc.txt", 'a') as f:
    f.write("**** CHART DOCS ****\n")  
import chart
functions = ["plot_Smatrix"]
collective_name = ", plot_Kmatrix, plot_Tmatrix, plot_UniOpSMat, plot_raw, "\
                  "plot_Ephase, plot_XS, plot_TotalXS"
collective_desc = "Plots various scattering related quantities."
param_append = {"i" : "Not available for plot_Ephase and plot_TotalXS.",
                "j" : "Not available for plot_Ephase and plot_TotalXS.",
                "imag" : "Not available for plot_Ephase and plot_TotalXS."}
add_info = [[(False, collective_name), (True, collective_desc)]]
write_doc(chart.Chart, functions, "chart", add_info, param_append)

with open("doc.txt", 'a') as f:
    f.write("**** MCSMATFIT DOCS ****\n")  
import mcsmatfit
write_doc(mcsmatfit.MCSMatFit, mcsmatfitfunctions, "mcsmatfit")
