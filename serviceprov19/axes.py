# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 15:13:56 2015

@author: slehar
"""

import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons
import numpy as np

import agents

# Global variables
fig = None
winXInches = 20
winYInches = 16
axXLim = (0, 1.)
axYLim = (0, 1.)
plotWidth = 500
schedTitle = 'schedTitle'
#ax2yMin, ax2yMax = (.7, .9)
ax2yMin, ax2yMax = (0., 100.)
line = lineWht = lineBlk = lineOth = lineNptsd = None
provXCtr = .5
provYCtr = .95
provSize = .05
provXOrg = provXCtr - (provSize/2.)
provYOrg = provYCtr - (provSize/2.)
aspect = 1.
ax  = None
ax2 = None
ax3 = None
ax4 = None
check = None


# Checkbox states
checkService  = True
checkStepped  = False
checkPause    = False
checkEndBen   = True
checkDist     = False
checkGraphics = True

        
#########[ init ax Map Axes]########
def init_ax():
    
    global winXInches, winYInches, axXLim, axYLim, fig, ax, schedTitle
    
    plt.close('all')
    fig = plt.figure(figsize=(winXInches, winYInches))
    fig.canvas.set_window_title('ServiceProv19')
    #cid = fig.canvas.mpl_connect('button_press_event', onclick)
    
    schedTitle = fig.text(.7,  .9, 'Schedule', fontsize=14)
    fig.text(.78, .78, 'SPR', fontsize=16)
    fig.text(.88, .78, 'CBT', fontsize=16)
    ax = fig.add_axes([.05, .15, .64, .8])
    ax.set_xlim(axXLim)
    ax.set_ylim(axYLim)
    # ax.set_xticklabels([])
    # ax.set_yticklabels([])
    ax.set_xticks(np.arange(0,1.1,.1))
    ax.set_yticks(np.arange(0,1.1,.1))

#########[ init ax2 Plot Axes ]########
def init_ax2():
    
    global plotWidth, ax2yMin, ax2yMax 
    global ax2, line, lineWht, lineBlk, lineNptsd, lineOth
    
    # Add axes 2 for plot trace
    ax2 = fig.add_axes([.05,.02,.64,.1])
    ax2.set_xlim(0, plotWidth)
    # axes.ax2.axis((t - plotWidth, t, axes.ax2yMin, axes.ax2yMax))
    ax2.set_xlim(agents.preLaunch - plotWidth, -agents.preLaunch)
    # ax2.set_xlim(-agents.preLaunch, plotWidth+agents.preLaunch)
    ax2.set_ylim(ax2yMin, ax2yMax)
    
    # Set up plot line in axes 2
    '''
    line,    = ax2.plot(0, 0, color='blue',   linewidth=1, linestyle='-', 
                        alpha=1.0, label='All')
    lineWht, = ax2.plot(0, 0, color='red',    linewidth=1, linestyle='-', 
                        alpha=1.0, label='White')
    lineBlk, = ax2.plot(0, 0, color='cyan',  linewidth=1, linestyle='-', 
                        alpha=1.0, label='Black')
    lineOth, = ax2.plot(0, 0, color='orange', linewidth=1, linestyle='-', 
                        alpha=1.0, label='Other')
    '''
    lineNptsd, = ax2.plot(0, 0, color='k', linewidth=2, linestyle='-', 
                        alpha=1.0, label='nPtsd')
    ax2.legend(loc=6)

#########[ init ax3  Sched Axes ]########
def init_ax3():
    
    global ax3
    
    # ax3 = fig.add_axes([.72, .8, .12, .015*agents.maxEnrolled])
    ax3 = fig.add_axes([.72, .8, .034 + (.017 * agents.standardSched), .015*agents.maxEnrolled])
    ax3.set_xticklabels([])
    ax3.set_yticklabels([])
    ax3.set_xticks(range(1, agents.standardSched+2))
    ax3.set_yticks(range(1, agents.maxEnrolled))
    ax3.set_xlim((0, agents.standardSched+2))
    ax3.set_ylim((0, agents.maxEnrolled))
    ax3.grid(True)
    vLine1 = plt.Line2D((2,2),(0,agents.maxEnrolled), lw=4, color='g', zorder=3)
    vLine2 = plt.Line2D((7,7),(0,agents.maxEnrolled), lw=4, color='r', zorder=3)
    ax3.add_line(vLine1)
    ax3.add_line(vLine2)
    

# Checkbox function
def func(label):
    global checkService, checkStepped, checkPause, checkEndBen, checkDist, checkGraphics
    if label == 'Service':
        checkService = not checkService
    elif label == 'Stepped':
        checkStepped = not checkStepped
    elif label == 'Pause':
        checkPause = not checkPause
    elif label == 'EndBen':
        checkEndBen = not checkEndBen
    elif label == 'Dist':
        checkDist = not checkDist
        agents.circle.set_visible(checkDist)
    elif label == 'Graphics':
        checkGraphics = not checkGraphics

#########[ init ax4 Checkbox Axes ]########
def init_ax4():
    
    global ax4, check
    global checkService, checkStepped, checkPause
    global checkEndBen, checkDist, checkGraphics

    ax4 = fig.add_axes([.72, .15, .08, .12])
    ax4.set_xticklabels([])
    ax4.set_yticklabels([])
    ax4.set_xticks([])
    ax4.set_yticks([])
    
    # Define checkboxes
    check = CheckButtons(ax4, ('Service',   'Stepped', 'Pause',
                               'EndBen',    'Dist', 'Graphics'),
                              (checkService, checkStepped, checkPause,
                               checkEndBen, checkDist, checkGraphics))
                               
    # Attach checkboxes to checkbox function
    check.on_clicked(func)


#########[ init axes ]########
def init_axes():
    init_ax()
    init_ax2()
    init_ax3()
    init_ax4()
    















