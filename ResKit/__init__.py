import os
import sys
fileDir = os.path.dirname(os.path.realpath(__file__))
modPath = fileDir+'/modules' # Keep modules before dependencies
sys.path.insert(0,modPath)
depPath = fileDir+'/dependencies'
sys.path.insert(0,depPath)

# Only use this to get the defaults and enums (can't override):
import pynumwrap as nw
from channelutil.units import *

dependencyOverride = False
def overrideDependencies():
    global dependencyOverride
    if not dependencyOverride:
        sys.path.remove(depPath)
        sys.path.append(depPath)
        dependencyOverride = True

typeMode = nw.mode_python
typeDps = nw.dps_default_python
def usePythonTypes(dps=nw.dps_default_python):
    global typeMode
    global typeDps
    nw.usePythonTypes(dps)
    typeMode = nw.mode_python
    typeDps = dps
def useMpmathTypes(dps=nw.dps_default_mpmath):
    global typeMode
    global typeDps
    nw.useMpmathTypes(dps)
    typeMode = nw.mode_python
    typeDps = dps

MOD_CHART = 0
# Remove dMat since may want to use several??
def getModule(modID, parmaFilePaths=None, resultsRoot=None):
    if modID == MOD_CHART:
        import chart
        chart.dMat = dMat
        return chart
