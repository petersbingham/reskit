import os
import datetime
import io
import copy

class tool:
    def __init__(self, data, resultsRoot, parmaFilePath, toolDir):
        self.data = copy.deepcopy(data)
        self.resultsRoot = resultsRoot
        self.parmaFilePath = parmaFilePath
        if self.parmaFilePath is None:
            self.parmaFilePath = toolDir+os.sep+"default.yml"
        if self.resultsRoot is not None:
            self.log = logger(self._getLogFilePath())
            print self._getLogFilePath()
        else:
            self.log = logger(None)

    def _getLogFilePath(self):
        return self.resultsRoot+"calc.log"

class logger:
    def __init__(self, logFilePath):
        self.logFilePath = logFilePath

    def write(self, msg):
        if self.logFilePath is not None:
            with faopen(self.logFilePath) as f:
                fw(f,msg)

    def writeCall(self, funStr):
        msg = "\n" + getDateTimeString() + ": " + funStr + "\n"
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
