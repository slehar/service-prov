# -*- coding: utf-8 -*-
# ServiceProv7.py
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
from random import random
"""
Created on Wed Jun 24 11:09:21 2015

@author: slehar
"""

# Parameters
winXInches = 16
winYInches = 16
axXLim = (0, 10)
axYLim = (0, 10)
provXCtr = 5.
provYCtr = 9.5
provSize = .4
provXOrg = provXCtr - (provSize/2.)
provYOrg = provYCtr - (provSize/2.)
minSep = .25

delay = 0.01
A = 0.01   # Shunting decay term
inputValue = .2

# Global variables
avgPtsd = 0.
nAgents = 100
nEnrolled = 0
maxEnrolled = 5
standardSched = 5
flow = False
x = 0.001
t = 0.
lastX = 0.
lastT = 0.
dt = .5
A = .1
dArray = deque([0.])
tArray = deque([0.])
plotWidth = 500


# Open figure and set axes 1 for drawing Artists
plt.close('all')
fig = plt.figure(figsize=(winXInches, winYInches))
fig.canvas.set_window_title('ServiceProv7')
ax = fig.add_axes([.05, .15, .8, .8])
ax.set_xlim(axXLim)
ax.set_ylim(axYLim)
ax.set_xticklabels([])
ax.set_yticklabels([])
ax.set_xticks([])
ax.set_yticks([])

# Add axes 2 for plot trace
ax2 = fig.add_axes([.05,.02,.8,.1])
ax2.set_ylim(0, 1)
ax2.set_xlim(0, 10)

# Set up plot line in axes 2
line, = ax2.plot(t, x, color='blue', linewidth=1, 
                 linestyle='-', alpha=1.0)  


arrows = []
codes = [Path.MOVETO,
         Path.CURVE4,
         Path.CURVE4,
         Path.CURVE4,
         ]

#### Generate random arrangement of agents ####
agentId = 0
agents = []
totWellness = 0.
bezLines = []

## for each agent
for agtId in range(nAgents):
    print "agtId = %d"%agtId
    foundSpace = False
    while not foundSpace:
        xLoc = random() * 8. + 1.
        yLoc = random() * 7. + 1.
        print "  xLoc, yLoc = (%4.2f, %4.2f)"%(xLoc, yLoc)
        collision = False
        for agt in range(len(agents)):
            xLoc1 = agents[agt]['xLoc']
            yLoc1 = agents[agt]['yLoc']
            dx = xLoc1 - xLoc
            dy = yLoc1 - yLoc
            dist = np.sqrt(dx**2 + dy**2)
            if dist < minSep:
                collision = True
                print "  COLLISION !!!"
                break
        if not collision:
            foundSpace = True
            
    circle = plt.Circle((xLoc, yLoc), .1, fc='r', ec='k')
    ax.add_patch(circle)
    
    xVal = np.random.random()
    totWellness += xVal           
    verts = ((provXCtr, provYCtr), 
             ((provXCtr + xLoc)/2., provYCtr),
             (xLoc, (provYCtr + yLoc)/2.),
             (xLoc, yLoc))
    bezPath = Path(verts, codes)
    bezPatch = patches.PathPatch(bezPath, facecolor='none', 
                              lw=1, ec='#afafaf', visible=False)
    agents.append({'id':agtId,   'circ':circle, 'bezPatch':bezPatch,
                   'xLoc':xLoc,  'yLoc':yLoc,   'xVal':xVal, 'iVal':.2*xVal,   
                   'enrolled':False, 'nSched':0})
    ax.add_patch(bezPatch)
    bezLines.append(bezPatch)
    
    agentId += 1
    
    

avgWellness = 5.*totWellness/float(nAgents) + .01

    
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
        if random() > .25: # Randomize every other time to break sync
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
    
    global linetime, linedat
    global x,t,lastX,lastT
    global dArray, tArray
    
    sumPtsd = 0.
    for agnum in range(nAgents):
        update_agent(agents[agnum])
        sumPtsd += agents[agnum]['xVal']
        
    avgPtsd = sumPtsd / float(nAgents)
    # print '  avgPtsd = %f'%avgPtsd

    x = avgPtsd
    lastT = t
    t += dt
    dArray.appendleft(x)
    if len(dArray) >= plotWidth:
        dArray.pop()
    tArray.appendleft(t)
    if len(tArray) >= plotWidth:
        tArray.pop()
    line.set_data(tArray,dArray)
    ax2.axis((t - plotWidth, t, 0., 1.))
    # time.sleep(.1)
    
        

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
