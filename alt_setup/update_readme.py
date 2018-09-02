import io

import os
import sys
filedir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0,filedir+os.sep+'..'+os.sep+'reskit')
import release

def transform_line(l):
    l = l.replace("git clone", "unzip")
    return l.replace("cd reskit", "cd reskitCPC-"+release.__version__)

new_lines = []
with io.open("README.md", 'r', newline='\n', encoding="utf-8") as f:
    writing = True
    for l in f:
        if "Getting reskit" in l:
            writing = False
        elif not writing and "##" in l:
            writing = True
        if writing:
            new_lines.append(transform_line(l))

with io.open("README.md", 'w', newline='\n', encoding="utf-8") as f:
    for l in new_lines:
        f.write(l)
