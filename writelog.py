# writelog

import os
import datetime

logFilename = ''
filePointer = None

####[ initLogfile() ]####
def initLogfile(fileNameParam):
    global logFilename, filePointer

    logFilename = fileNameParam
    if os.path.exists(logFilename):
        os.remove(logFilename)
    filePointer = open(logFilename,'w')
    filePointer.write('Log file: %s %s\n\n'%(logFilename, datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')))
    filePointer.close()

####[ function writeLog ]####
def writeLog(msg):
    fp = open(logFilename,'a')
    fp.write(msg)
    fp.close()


    
