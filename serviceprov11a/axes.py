# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 15:13:56 2015

@author: slehar
"""

import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons

import agents

# Global variables
fig = None
winXInches = 16
winYInches = 16
axXLim = (0, 10)
axYLim = (0, 10)
plotWidth = 500
ax2yMin, ax2yMax = (.7, .9)
line = None
provXCtr = 5.
provYCtr = 9.5
provSize = .4
provXOrg = provXCtr - (provSize/2.)
provYOrg = provYCtr - (provSize/2.)
ax  = None
ax2 = None
ax3 = None
ax4 = None
check = None


# Checkbox states
checkService = False
checkPause   = False
checkEndBen  = False
checkDist    = False

#########[ init ax ]########
def init_ax():
    
    global winXInches, winYInches, axXLim, axYLim, fig, ax
    
    plt.close('all')
    fig = plt.figure(figsize=(winXInches, winYInches))
    fig.canvas.set_window_title('ServiceProv11a')
    ax = fig.add_axes([.05, .15, .8, .8])
    ax.set_xlim(axXLim)
    ax.set_ylim(axYLim)
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_xticks([])
    ax.set_yticks([])

#########[ init ax2 ]########
def init_ax2():
    
    global plotWidth, ax2yMin, ax2yMax, ax2, line
    
    # Add axes 2 for plot trace
    ax2 = fig.add_axes([.05,.02,.8,.1])
    ax2.set_xlim(0, plotWidth)
    ax2.set_ylim(ax2yMin, ax2yMax)
    
    # Set up plot line in axes 2
    line, = ax2.plot(0, 0, color='blue', linewidth=1,
                     linestyle='-', alpha=1.0)

#########[ init ax3 ]########
def init_ax3():
    
    global ax3
    
    ax3 = fig.add_axes([.86, .8, .12, .015*agents.maxEnrolled])
    ax3.set_xticklabels([])
    ax3.set_yticklabels([])
    ax3.set_xticks(range(1, 7))
    ax3.set_yticks(range(1, agents.maxEnrolled))
    ax3.set_xlim((0, 7))
    ax3.set_ylim((0, agents.maxEnrolled))
    ax3.grid(True)

# Checkbox function
def func(label):
    global checkService, checkPause, checkEndBen, checkDist
    if label == 'Service':
        checkService = not checkService
    elif label == 'Pause':
        checkPause = not checkPause
    elif label == 'EndBen':
        checkEndBen = not checkEndBen
    elif label == 'Dist':
        checkDist = not checkDist
        agents.circle.set_visible(checkDist)

#########[ init ax4 ]########
def init_ax4():
    
    global ax4, checkService, checkPause, checkEndBen, checkDist, check

    ax4 = fig.add_axes([.88, .15, .1, .1])
    ax4.set_xticklabels([])
    ax4.set_yticklabels([])
    ax4.set_xticks([])
    ax4.set_yticks([])
    
    # Define checkboxes
    check = CheckButtons(ax4, ('Service',   'Pause',    'EndBen',    'Dist'),
                              (checkService, checkPause, checkEndBen, checkDist))
                               
    # Attach checkboxes to checkbox function
    check.on_clicked(func)


















