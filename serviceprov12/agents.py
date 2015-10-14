# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 15:36:41 2015

@author: slehar
"""
from random import seed
from matplotlib.path import Path
from collections import deque

# Local modules
# import axes
import writelog
# import updateagent
# import updateall

# Global variables
avgPtsd = 0.
nAgents = 100
nEnrolled = 0
maxEnrolled = 6
standardSched = 5
avgInput = 0.
square = None
circle = None
tileList = []
tileListPtr = 0
doingLogging = True
doseValue = .2
delay = 0.0
A = 0.1   # Shunting decay term
x = 0.001
t = 0.
lastX = 0.
lastT = 0.
dt = .5
dArray = deque([0.])
tArray = deque([0.])
plotWidth = 500

agents = []
totInput = 0.
bezLines = []

minSep = .25
rSigma = 3.

# Initialize random seed
seed(2)
writelog.init('run.log')


# Codes for four-point Bezier spline
codes = [Path.MOVETO,
         Path.CURVE4,
         Path.CURVE4,
         Path.CURVE4,
         ]

agents = []



