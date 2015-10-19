# -*- coding: utf-8 -*-
"""
Tests logging

Created on Wed Sep 30 14:21:05 2015

@author: slehar
"""

import logging

logging.basicConfig(filename='LoggingTest.log', level=logging.DEBUG)

logging.info('Start info logging')

i = 5
for i in range(5):
    logging.info('  iter %d',i)
    
logging.info('Done!')