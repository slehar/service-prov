import logging
import time
import datetime

logFilename = '/Users/slehar/Documents/PythonProgs/service-prov/serviceprov11/example.log'
logging.basicConfig(filename=logFilename,level=logging.DEBUG, filemode='w')

def func():
    logging.info('  in func()')
	
logging.info('Starting logging')
logging.info('Log file ServiceProv11.py %s\n\n', datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'))

logging.info('calling func()')

func()

count = 0
while True:
    logging.info('  logging %d'%count)
    count += 1
    time.sleep(1)
