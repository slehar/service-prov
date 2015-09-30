# -*- coding: utf-8 -*-
# ServiceProv6.py
#
# Model of service provision
# Add therapy supply-side

import numpy as np
# from matplotlib.patches import Circle, Rectangle
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
from matplotlib.widgets import CheckButtons, Slider
from collections import deque
import time
from matplotlib.path import Path
"""
Created on Wed Jun 24 11:09:21 2015

@author: slehar
"""

# Parameters
provXCtr = 3.
provYCtr = .7
provSize = .2
provXOrg = provXCtr - (provSize/2.)
provYOrg = provYCtr - (provSize/2.)
delay = 0.01
A = 0.01   # Shunting decay term
inputValue = 0.1

# Global variables
avgPtsd = 0.
nAgents = 0
nEnrolled = 0
maxEnrolled = 4
standardSched = 10


# Open figure and set axes 1 for drawing Artists
plt.close('all')
fig = plt.figure(figsize=(15,5))
fig.canvas.set_window_title('ServiceProv6')
ax = fig.add_axes([.1, .5, .8, .4])
ax.set_xlim([0, 6])
ax.set_ylim([0, 1])
ax.set_xticklabels([])
ax.set_yticklabels([])
ax.set_xticks([])
ax.set_yticks([])

"""
fluid = plt.Rectangle((1, 1), 2, 2*flevel, fc=(0, 1, 0))
ax.add_patch(fluid)
circle = plt.Circle((6, 2), 1, fc='r', ec='k')
ax.add_patch(circle)
arrow = plt.Arrow(3, 2, 2, 0, ec='k', fc=(1, 1, 1))
ax.add_patch(arrow)
Elight = ax.text(.7, 1, r"E", fontsize=16, color='r', visible=False)
"""

arrows = []
codes = [Path.MOVETO,
         Path.CURVE4,
         Path.CURVE4,
         Path.CURVE4,
         ]

#### Generate row of agents ####
id = 0
xCoords = np.linspace(.5,5.5,num=10)
agents = []
totWellness = 0.
for xCoord in xCoords:
    circle = plt.Circle((xCoord, .2), .1, fc='r', ec='k')
    ax.add_patch(circle)
    dx = 3 - xCoord
    px = xCoord
    verts = ((provXCtr, provYCtr), 
             ((provXCtr + xCoord)/2., provYCtr),
             (xCoord, provYCtr),
             (xCoord, .2))
    bezPath = Path(verts, codes)
    bezPatch = patches.PathPatch(bezPath, facecolor='none', 
                              lw=1, ec='#afafaf', visible=False)
    ax.add_patch(bezPatch)
    arrows.append(bezPatch)
    randXVal = np.random.random()/2.0
    totWellness += randXVal
    agents.append({'id':id,         'circ':circle, 'bezPatch':bezPatch,
                   'xVal':randXVal, 'iVal':0.,     'enrolled':False,
                   'nSched':0})
    '''
    if id == 2:
        agents[id]['iVal'] = .1
        agents[id]['bezPatch'].set_visible(True)
        agents[id]['bezPatch'].set_lw(2)
        agents[id]['bezPatch'].set_ec('#00ff00')
    '''
    id += 1
    nAgents += 1
    
avgWellness = totWellness/float(nAgents)
    

    
# for agent in range(len(agents)):
#     print 'id: %d'%id

square = plt.Rectangle((provXOrg, provYOrg), 
                       provSize, provSize, fc=(0,1,0), ec='k')
ax.add_patch(square)

#### Update single agent ####
def update_agent(agent):
    
    global nEnrolled
    
    xVal = agent['xVal']
    lastXVal  = xVal
    
    # If not in treatment consider enrolling
    if not agent['enrolled']:
        need = max((avgWellness - xVal),0.)
        probEnroll = need * (maxEnrolled - nEnrolled)
        if probEnroll > np.random.random():
            agent['enrolled'] = True
            nEnrolled += 1
            agent['nSched'] = standardSched
            agent['bezPatch'].set_visible(True)
    else:
        # Otherwise compute input treatment
        # If input is off, turn it on
        if agent['iVal'] == 0.:
            agent['iVal'] = inputValue;
            agent['bezPatch'].set_lw(2)
            agent['bezPatch'].set_ec('#00ff00')
            
        # Otherwise (input is on) turn it off
        else:
            agent['iVal'] = 0.;
            agent['bezPatch'].set_lw(1)
            agent['bezPatch'].set_ec('#afafaf')
            agent['nSched'] -= 1
            
            # If treatment program done, un-enroll
            if agent['nSched'] <= 0:
                agent['nSched'] = 0
                agent['enrolled'] = False
                nEnrolled -= 1
                agent['iVal'] = 0.;
                agent['bezPatch'].set_lw(1)
                agent['bezPatch'].set_ec('#afafaf')
                agent['bezPatch'].set_visible(False)
   
    
    # Shunting equation
    xVal += -A * xVal + (1 - xVal) * agent['iVal']
    if xVal < 0.:
        xVal = 0.
    elif xVal > 1.:
        xVal = 1.
    agent['xVal'] = xVal
    r = (1. - xVal)
    g = xVal
    agent['circ'].set_facecolor((r, g, 0.))

    # Time delay
    if delay > 0.:
        time.sleep(delay)


#### Update each loop ####
def update(num):
    
    for agnum in range(len(agents)):
        update_agent(agents[agnum])
        

# Run the animation
ani = animation.FuncAnimation(fig, update, frames=100,
                              interval=1000, repeat=True)

# Show plot
plt.show()
figmgr = plt.get_current_fig_manager()
figmgr.canvas.manager.window.raise_()
geom = figmgr.window.geometry()
xLoc, yLoc, dxWidth, dyHeight = geom.getRect()
figmgr.window.setGeometry(10, 10, dxWidth, dyHeight)
