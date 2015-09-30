# writeLog.py
#

import os
import datetime


#### function writeLog ####
def writeLog(msg):

    fp = open(globFilename,'a')
    fp.write(msg)
    fp.close()

#### function initLog ####
def initLog(logFilename):

    if os.path.exists(logFilename):
        os.remove(logFilename)
    fp = open(logFilename,'w')
    fp.write('Log file %s %s\n\n'%(logFilename, datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')))
    fp.close()
    return fp
    

