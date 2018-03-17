import os
import sys
fileDir = os.path.dirname(os.path.realpath(__file__))
depPath = fileDir+'/dependencies'
sys.path.insert(0,depPath)

dependencyOverride = False
def overrideDependencies():
  global dependencyOverride
  if not dependencyOverride:
    sys.path.remove(depPath)
    sys.path.append(depPath)
    dependencyOverride = True

