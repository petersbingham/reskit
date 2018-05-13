# Requires the following command in latex doc:
# \usepackage{enumitem}

function_doc_str = \
r'''\bigskip\noindent\codefont{{'{'}}{{FUNCTION_NAME}}{{'}'}}: {{FUNCTION_DESC}}
\begin{itemize}[noitemsep,topsep=1pt, label={\tiny\raisebox{1ex}{\textbullet}}]
{{PARAMETERS_DESC}}
\end{itemize}
'''

param_doc_str = \
r'''
\item\codefont{{'{'}}{{PARAM_NAME}}{{'}'}} (\textit{{'{'}}{{PARAM_TYPE}}{{'}'}})

'''
params_doc_str = \
r'''
\item\codefont{{'{'}}{{PARAM_NAME}}{{'}'}} (\textit{{'{'}}{{PARAM_TYPE}}{{'}'}}): {{PARAM_DESC}}

'''
