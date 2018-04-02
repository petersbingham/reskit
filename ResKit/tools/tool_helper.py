import os

def cfgName(path):
    return os.path.splitext(path)[0].split(os.sep)[-1]
