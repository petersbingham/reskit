import os
import sys
fileDir = os.path.dirname(os.path.realpath(__file__))
modPath = fileDir+'/modules' # Keep modules before dependencies
sys.path.insert(0,modPath)
depPath = fileDir+'/dependencies'
sys.path.insert(0,depPath)

dependencyOverride = False
def overrideDependencies():
    global dependencyOverride
    if not dependencyOverride:
        sys.path.remove(depPath)
        sys.path.append(depPath)
        dependencyOverride = True

MOD_CHART = 0
def getModule(modID, parmaFilePaths=None, resultsRoot=None):
    if modID == MOD_CHART:
        import chart
        chart.dMat = dMat
        return chart
