import os
import datetime
import io
import copy
import yaml

class tool:
    def __init__(self, data, archiveRoot, paramFilePath, toolDir, silent):
        self.data = copy.deepcopy(data)
        self.archiveRoot = archiveRoot
        self.paramFilePath = paramFilePath
        if self.paramFilePath is None:
            self.paramFilePath = toolDir+os.sep+"default.yml"
        if self.archiveRoot is not None:
            self.log = logger(self._getLogFilePath())
            if not silent:
                print self._getLogFilePath()
        else:
            self.log = logger(None)

    def _getLogFilePath(self):
        return self.archiveRoot+"calc.log"

    def _getConfigCacheName(self):
        return "config.yml"

    def _doesParamCacheMatch(self, cacheDir, paramKey):
        with fropen(self.paramFilePath) as f:
            config = yaml.load(f.read())

            if os.path.isdir(cacheDir):
                try:
                    cachePath = cacheDir+os.sep+self._getConfigCacheName()
                    with fropen(cachePath) as f:
                        p = config[paramKey]
                        p_str = str(p)
                        p_cache_str = f.read()
                        return p_cache_str == p_str
                except Exception as inst:
                    self._fileError(str(inst))
        return False

    def _verifyParamCache(self, cacheDir, paramKey):
        if os.path.isdir(cacheDir) and\
        not self._doesParamCacheMatch(cacheDir, paramKey):
            self._configError()

    def _configError(self):
        eStr = "Error. Configuration at paramFilePath conflicts with a prior "
        eStr += "config with the same file name. Rename your parameter file."
        self.log.writeErr(eStr)
        raise Exception(eStr)

    def _fileError(self, eStr):
        self.log.writeErr(eStr)
        raise Exception("Error. Exception opening cache config: " + eStr)


class logger:
    def __init__(self, logFilePath):
        self.logFilePath = logFilePath

    def write(self, msg):
        if self.logFilePath is not None:
            with faopen(self.logFilePath) as f:
                fw(f,msg)

    def writeCall(self, funStr, internal=False):
        start = ""
        if not internal:
            start = "\n"
        msg = start + getDateTimeString() + ": " + funStr + "\n"
        self.write(msg)

    def writeCallEnd(self, funStr):
        msg = getDateTimeString() + ": " + funStr + " end\n"
        self.write(msg)

    def writeMsg(self, msg):
        msg = "  " + msg + "\n"
        self.write(msg)

    def writeErr(self, msg):
        msg = "  Error: " + msg + "\n"
        self.write(msg)

    def writeParameters(self, params):
        msg = "  Using parameters: " + str(params) + "\n"
        self.write(msg)

def fropen(fileName):
    return io.open(fileName, 'r', newline='\n', encoding="utf-8")
def fwopen(fileName):
    return io.open(fileName, 'w', newline='\n', encoding="utf-8")
def faopen(fileName):
    return io.open(fileName, 'a', newline='\n', encoding="utf-8")
def fw(f, o):
    f.write(unicode(o))

def cfgName(path):
    return os.path.splitext(path)[0].split(os.sep)[-1]

def getDateTimeString():
    return str(datetime.datetime.now())[:-3]

def getSubDirs(directory):
    return os.listdir(directory)
