# -*- coding: utf-8 -*-
# ServiceProv8.py
#
# Model of service provision
# Add treatment schedule & checkboxes

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
from matplotlib.widgets import CheckButtons
from collections import deque
import time
from matplotlib.path import Path
from random import random

import vertslider
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

delay = 0.0
A = 0.01   # Shunting decay term
doseValue = .2

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
rSigma = 3.

# Open figure and set axes 1 for drawing Artists
plt.close('all')
fig = plt.figure(figsize=(winXInches, winYInches))
fig.canvas.set_window_title('ServiceProv8')
ax = fig.add_axes([.05, .15, .8, .8])
ax.set_xlim(axXLim)
ax.set_ylim(axYLim)
ax.set_xticklabels([])
ax.set_yticklabels([])
ax.set_xticks([])
ax.set_yticks([])

# Service provider square and 2 sigma range
square = plt.Rectangle((provXOrg-provSize/2, provYOrg-provSize/2), 
                       provSize, provSize, fc=(0,1,0), ec='k')
ax.add_patch(square)
distCircle = plt.Circle((provXOrg, provYOrg), radius=rSigma, ec='r', fc='none',
                    linestyle='dashed', visible=False )
ax.add_patch(distCircle)

# Add axes 2 for plot trace
ax2 = fig.add_axes([.05,.02,.8,.1])
ax2yMin, ax2yMax = (.7, .9)
# ax2.set_ylim(0, 1)
ax2.set_xlim(0, plotWidth)
ax2.set_ylim(ax2yMin, ax2yMax)

# Set up plot line in axes 2
line, = ax2.plot(t, x, color='blue', linewidth=1, 
                 linestyle='-', alpha=1.0)  


axVsl = fig.add_axes([.88, .51, .05, .2])
axVsl.set_xticklabels([])
axVsl.set_yticklabels([])
axVsl.set_xticks([])
axVsl.set_yticks([])

# Distance Function
def distFunc(distVal):
    global rSigma
    
    rSigma = distVal
    distCircle.set_radius(rSigma)
    
# Distance Slider
vSl = vertslider.VertSlider(axVsl, 'Distance', 0, 10, valinit=rSigma)
vSl.on_changed(distFunc)

# Add axes 4 for check boxes
ax4 = fig.add_axes([.88, .15, .1, .1])
ax4.set_xticklabels([])
ax4.set_yticklabels([])
ax4.set_xticks([])
ax4.set_yticks([])

# Define checkboxes
check = CheckButtons(ax4, ('Service', 'Pause', 'EndBen', 'Dist'),
                           (False, False, False, False))
# Checkbox states                           
checkService = False
checkPause   = False
checkEndBen  = False
checkDist    = False

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
        distCircle.set_visible(checkDist)

# Attach checkboxes to checkbox function
check.on_clicked(func)

# Codes for four point Bezier spline
codes = [Path.MOVETO,
         Path.CURVE4,
         Path.CURVE4,
         Path.CURVE4,
         ]

    
#### Generate random arrangement of agents ####
agentId = 0
agents = []
totInput = 0.
bezLines = []

## for each agent
for agtId in range(nAgents):
    # print "agtId = %d"%agtId
    foundSpace = False
    while not foundSpace:
        xLoc = random() * 8. + 1.
        yLoc = random() * 7. + 1.
        # print "  xLoc, yLoc = (%4.2f, %4.2f)"%(xLoc, yLoc)
        collision = False
        for agt in range(len(agents)):
            xLoc1 = agents[agt]['xLoc']
            yLoc1 = agents[agt]['yLoc']
            dx = xLoc1 - xLoc
            dy = yLoc1 - yLoc
            dist = np.sqrt(dx**2 + dy**2)
            if dist < minSep:
                collision = True
                # print "  COLLISION !!!"
                break   # Stop going through more agents
        if not collision:
            foundSpace = True  
            # Otherwise keep searching
            
    circle = plt.Circle((xLoc, yLoc), .1, fc='r', ec='k')
    ax.add_patch(circle)
    
    iVal = np.random.random()  # Random input value (natural wellness)
    xVal = iVal/(A+iVal)
    totInput += iVal           
    verts = ((provXOrg, provYOrg), # Bezier link from provider to here
             ((provXOrg + xLoc)/2., provYOrg),
             (xLoc, (provYOrg + yLoc)/2.),
             (xLoc, yLoc))
    bezPath = Path(verts, codes)
    bezPatch = patches.PathPatch(bezPath, facecolor='none', 
                              lw=1, ec='#afafaf', visible=False)
    agents.append({'id':agtId,
                   'circ':circle,
                   'bezPatch':bezPatch,
                   'xLoc':xLoc,
                   'yLoc':yLoc,
                   'xVal':xVal,
                   'iVal':iVal,   
                   'treating':False,
                   'enrolled':False,
                   'nSched':0})
    ax.add_patch(bezPatch)
    bezLines.append(bezPatch)
    agentId += 1
    
    

avgInput = totInput/float(nAgents)

    
#### Update single agent ####
def update_agent(agent):
    
    global nEnrolled

    xVal = agent['xVal']
    inputVal = agent['iVal']
    
    # If service is on, service the agents    
    if checkService:
        square.set_fc('#00ff00')
        
        # If not in treatment consider enrolling
        if not agent['enrolled']:
            need = max((avgInput - xVal),0.)
            
            if checkDist:
                distProvX, distProvY = (agent['xLoc'] - provXOrg,
                                        agent['yLoc'] - provYOrg)
                distProv = np.sqrt(distProvX**2 + distProvY**2)
                gauss = (1./rSigma*np.sqrt(2.*np.pi)) * np.exp(-(distProv**2.)/(2.*rSigma**2))
                # print 'dx=%4.2f\tdy=%4.2f\tdistProv =\t%4.2f gauss=%12.5f'%(distProvX,distProvY,distProv, gauss) 
                probEnroll = need * (maxEnrolled - nEnrolled) * gauss
            else:
                probEnroll = need * (maxEnrolled - nEnrolled)
                
            # If probability exceeds random threshold then enroll
            if probEnroll > np.random.random():
                agent['enrolled'] = True
                nEnrolled += 1
                agent['nSched'] = standardSched
                agent['bezPatch'].set_visible(True)
                inputVal = agent['iVal']
                plt.text(agent['xLoc'], agent['yLoc'], '%d'%agent['id'])

        else:
            # Otherwise compute input treatment
            if random() > .25: # Randomize every other time to break sync
                
                # If patient not in treatment do next treatment
                if agent['treating'] == False:
                    agent['treating'] = True
                    agent['bezPatch'].set_lw(2)
                    agent['bezPatch'].set_ec('#00ff00')
                    inputVal = agent['iVal']
                    
                # Otherwise (treatment is on) turn it off
                else:
                    agent['treating'] = False;
                    agent['bezPatch'].set_lw(1)
                    agent['bezPatch'].set_ec('#afafaf')
                    if checkEndBen:
                        agent['iVal'] += doseValue/10.
                    else:
                        inputVal = agent['iVal'] + doseValue
                    agent['nSched'] -= 1
                    
                    # If treatment program done, un-enroll
                    if agent['nSched'] <= 0:
                        agent['nSched'] = 0
                        agent['enrolled'] = False
                        nEnrolled -= 1
                        agent['treating'] = 0.;
                        agent['bezPatch'].set_lw(1)
                        agent['bezPatch'].set_ec('#afafaf')
                        agent['bezPatch'].set_visible(False)
    
    # Else if service is off, shut off treatment
    else:
        agent['bezPatch'].set_visible(False)
        square.set_fc('#ffffff')
        inputVal = agent['iVal']
            
    
    # Shunting equation
    xVal += -A * xVal + (1 - xVal) * inputVal
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
    
    global x,t,lastX,lastT
    global dArray, tArray
    
    if checkPause:
        return
    
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
    if len(dArray) > plotWidth / dt:
        dArray.pop()
    tArray.appendleft(t)
    if len(tArray) > plotWidth / dt:
        tArray.pop()
    line.set_data(tArray,dArray)
    ax2.axis((t - plotWidth, t, ax2yMin, ax2yMax))
    # time.sleep(.1)
    
        

# Run the animation
ani = animation.FuncAnimation(fig, update, interval=100., repeat=True)

# Show plot
plt.show()
figmgr = plt.get_current_fig_manager()
figmgr.canvas.manager.window.raise_()
geom = figmgr.window.geometry()
xLoc, yLoc, dxWidth, dyHeight = geom.getRect()
figmgr.window.setGeometry(10, 10, dxWidth, dyHeight)
