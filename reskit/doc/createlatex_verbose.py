# Requires the following command in latex doc:
# \newcommand{\codefont}[1]{\texttt{#1}}

desc_margin = "0.5cm"
type_name_tab = "0.5cm"
type_desc_margin = "1.0cm"

function_doc_str = \
r'''\bigskip\noindent\codefont{{'{'}}{{FUNCTION_NAME}}{{'}'}}
\begin{addmargin}['''+desc_margin+r''']{0.0cm}
{{FUNCTION_DESC}} {{PARAMETERS_DESC}} {{RETURNS_DESC}}
\end{addmargin}
'''

params_str_start_doc_str = \
"\n\n\\noindent\\textbf{Parameters:}"
param_doc_str = \
r'''
\tabto{'''+type_name_tab+r'''}\codefont{{'{'}}{{PARAM_NAME}}{{'}'}}: \textit{{'{'}}{{PARAM_TYPE}}{{'}'}}
'''
params_doc_str = \
r'''
\tabto{'''+type_name_tab+r'''}\codefont{{'{'}}{{PARAM_NAME}}{{'}'}}: \textit{{'{'}}{{PARAM_TYPE}}{{'}'}}
\begin{addmargin}['''+type_desc_margin+r''']{0.0cm}
{{PARAM_DESC}}\end{addmargin}
'''

rets_str_start_doc_str = \
"\n\\noindent\\textbf{Returns:}"
retDocStr = \
r'''
\tabto{'''+type_name_tab+r'''}\codefont{{'{'}}{{RET_NAME}}{{'}'}}: \textit{{'{'}}{{RET_TYPE}}{{'}'}}
'''
rets_doc_str = \
r'''
\tabto{'''+type_name_tab+r'''}\codefont{{'{'}}{{RET_NAME}}{{'}'}}: \textit{{'{'}}{{RET_TYPE}}{{'}'}}
\begin{addmargin}['''+type_desc_margin+r''']{0.0cm}
{{RET_DESC}}\end{addmargin}
'''
