import os
import sys
fileDir = os.path.dirname(os.path.realpath(__file__))
rootDir = fileDir+os.sep+".."+os.sep+".."+os.sep
sys.path.insert(0,rootDir)
sys.path.insert(0,rootDir+"tools")

from numpydoc.docscrape import FunctionDoc
import jinja2 as j

# Requires the following command in latex doc:
# \newcommand{\codefont}[1]{\texttt{#1}}

DESC_MARGIN = "0.5cm"
TYPE_NAME_TAB = "0.5cm"
TYPE_DESC_MARGIN = "1.0cm"

ResKitfuns = ["get_asym_calc","get_dmat_from_discrete","get_dmat_from_continuous",\
              "get_tool","use_python_types","use_mpmath_types","override_utilities"]
chartFunctions = ["plot_Smatrix", "plot_Kmatrix", "plot_Tmatrix", "plot_UniOpSMat",\
                  "plot_raw", "plot_EPhase", "plot_XS", "plot_TotalXS"]
mcsmatfitFunctions = ["get_elastic_Fin", "get_elastic_Fins", "find_Fin_roots",\
                      "find_stable_Smat_poles", "get_elastic_Smat", "plot_Smat_fit",\
                      "plot_totXS_fit"]
codeTypes = ["reskit.rydbergs", "reskit.hartrees", "reskit.eVs",\
             "reskit.Smat", "reskit.Kmat", "reskit.Tmat",\
             "reskit.chart", "reskit.mcsmatfit", "archive_root"]

functionDocStr = \
r'''\bigskip\noindent\codefont{{'{'}}{{FUNCTION_NAME}}{{'}'}}
\begin{addmargin}['''+DESC_MARGIN+r''']{0.0cm}
{{FUNCTION_DESC}} {{PARAMETERS_DESC}} {{RETURNS_DESC}}
\end{addmargin}
'''

paramsStrStartDocStr = \
"\n\n\\noindent\\textbf{Parameters:}"
paramDocStr = \
r'''
\tabto{'''+TYPE_NAME_TAB+r'''}\codefont{{'{'}}{{PARAM_NAME}}{{'}'}}: \textit{{'{'}}{{PARAM_TYPE}}{{'}'}}
'''
paramsDocStr = \
r'''
\tabto{'''+TYPE_NAME_TAB+r'''}\codefont{{'{'}}{{PARAM_NAME}}{{'}'}}: \textit{{'{'}}{{PARAM_TYPE}}{{'}'}}
\begin{addmargin}['''+TYPE_DESC_MARGIN+r''']{0.0cm}
{{PARAM_DESC}}\end{addmargin}
'''

retsStrStartDocStr = \
"\n\\noindent\\textbf{Returns:}"
retDocStr = \
r'''
\tabto{'''+TYPE_NAME_TAB+r'''}\codefont{{'{'}}{{RET_NAME}}{{'}'}}: \textit{{'{'}}{{RET_TYPE}}{{'}'}}
'''
retsDocStr = \
r'''
\tabto{'''+TYPE_NAME_TAB+r'''}\codefont{{'{'}}{{RET_NAME}}{{'}'}}: \textit{{'{'}}{{RET_TYPE}}{{'}'}}
\begin{addmargin}['''+TYPE_DESC_MARGIN+r''']{0.0cm}
{{RET_DESC}}\end{addmargin}
'''

try:
    os.remove("doc.txt")
except:
    pass

def cleanStr(string, typeStr):
    if len(typeStr) == 0:
        string = string.replace(":","")
    for repStr in ResKitfuns+chartFunctions+codeTypes:
        string = string.replace(repStr,"\codefont{"+repStr+"}")
    return string.replace("_","\\_").replace("\\textit{  }","")

def writeFunction(funcName, doc, addInfo, paramAppend):
    data = doc._parsed_data
    funcDesc = " ".join(data["Summary"])
    if len(addInfo) > 1:
        if addInfo[1][0]:
            funcDesc = addInfo[1][1]
        else:
            funcDesc += addInfo[1][1]
    paramsStr = ""
    retsStr = ""
    if len(data["Parameters"]) > 0:
        paramsStr = paramsStrStartDocStr
        for param in data["Parameters"]:
            if len(param[2]) > 0:
                param_desc = " ".join(param[2])
                if param[0] in paramAppend:
                    param_desc += " " + paramAppend[param[0]]
                t = j.Template(paramsDocStr)
                paramStr = t.render(PARAM_NAME=param[0], PARAM_TYPE=param[1],
                                    PARAM_DESC=param_desc)
            else:
                t = j.Template(paramDocStr)
                paramStr = t.render(PARAM_NAME=param[0], PARAM_TYPE=param[1])
            paramsStr += cleanStr(paramStr, param[1])
    if len(data["Returns"]) > 0:
        retsStr = retsStrStartDocStr
        for ret in data["Returns"]:
            if len(ret[2]) > 0:
                t = j.Template(retsDocStr)
                retStr = t.render(RET_NAME=ret[0], RET_TYPE=ret[1], 
                                  RET_DESC=" ".join(ret[2]))
            else:
                t = j.Template(retDocStr)
                retStr = t.render(RET_NAME=ret[0], RET_TYPE=ret[1])
            retsStr += cleanStr(retStr, ret[1])

    t = j.Template(functionDocStr)
    if len(addInfo) > 0:
        if addInfo[0][0]:
            funcName = addInfo[0][1]
        else:
            funcName += addInfo[0][1]
    funDescStr = t.render(FUNCTION_NAME = funcName, FUNCTION_DESC = funcDesc,
                          PARAMETERS_DESC = paramsStr, RETURNS_DESC = retsStr)
    if len(data["Parameters"]) == 0 and len(data["Returns"]) == 0:
        funDescStr += "\n"
    with open("doc.txt", 'a') as f:
        f.write(funDescStr+"\n\n")    

def writeDoc(mod, functions, name, addInfo=None, paramAppend=None):
    if addInfo is None:
        addInfo = []
    if paramAppend is None:
        paramAppend = {}
    addInfo.extend([[]]*(len(functions)-len(addInfo)))
    for i,function in enumerate(functions):
        funcName = getattr(mod, function)
        doc = FunctionDoc(funcName)
        writeFunction(name+"."+function, doc, addInfo[i], paramAppend)


import reskit
# Using inspect loses order
writeDoc(reskit, ResKitfuns, "reskit")

import chart
functions = ["plot_Smatrix"]
collectiveName = ", .plot_Kmatrix, .plot_Tmatrix, .plot_UniOpSMat, .plot_raw, "\
                 ".plot_EPhase, .plot_XS, .plot_TotalXS"
collectiveDesc = "Plots various scattering related quantities."
paramAppend = {"i" : "Not available for plot_EPhase and plot_TotalXS.",
               "j" : "Not available for plot_EPhase and plot_TotalXS.",
               "imag" : "Not available for plot_EPhase and plot_TotalXS."}
addInfo = [[(False, collectiveName), (True, collectiveDesc)]]
writeDoc(chart.Chart, functions, "chart", addInfo, paramAppend)

import mcsmatfit
writeDoc(mcsmatfit.MCSMatFit, mcsmatfitFunctions, "mcsmatfit")

