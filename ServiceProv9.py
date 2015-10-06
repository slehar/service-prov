# -*- coding: utf-8 -*-
# ServiceProv9.py
#
# Model of service provision
# Add treatment schedule & checkboxes

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
from matplotlib.widgets import CheckButtons, Slider
from collections import deque
import time
from matplotlib.path import Path
from random import random, seed
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
doseValue = .2

# Global variables
avgPtsd = 0.
nAgents = 100
nEnrolled = 0
maxEnrolled = 10
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
schedList = []
schedPtr = 0
tileList = []
tileListPtr = 0



# Open figure and set axes 1 for drawing Artists
plt.close('all')
fig = plt.figure(figsize=(winXInches, winYInches))
fig.canvas.set_window_title('ServiceProv9')
ax = fig.add_axes([.05, .15, .8, .8])
ax.set_xlim(axXLim)
ax.set_ylim(axYLim)
ax.set_xticklabels([])
ax.set_yticklabels([])
ax.set_xticks([])
ax.set_yticks([])

# Add axes 2 for plot trace
ax2 = fig.add_axes([.05,.02,.8,.1])
ax2yMin, ax2yMax = (.7, .9)
ax2.set_xlim(0, plotWidth)
ax2.set_ylim(ax2yMin, ax2yMax)

# Set up plot line in axes 2
line, = ax2.plot(t, x, color='blue', linewidth=1, 
                 linestyle='-', alpha=1.0)  

# Add axes 3 for treatment schedule
ax3 = fig.add_axes([.86, .8, .12, .015*maxEnrolled])
ax3.set_xticklabels([])
ax3.set_yticklabels([])
ax3.set_xticks(range(1, 13))
ax3.set_yticks(range(1, maxEnrolled))
ax3.set_xlim((0, 13))
ax3.set_ylim((0, maxEnrolled))
ax3.grid(True)

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
        circle.set_visible(checkDist)

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
    
    # Define agent's circle        
    circle = plt.Circle((xLoc, yLoc), .1, fc='r', ec='k')
    ax.add_patch(circle)
    
    # Define agent's bezier links    
    iVal = np.random.random()  # Random input value (natural wellness)
    xVal = iVal * 10.
    totInput += iVal           
    verts = ((provXCtr, provYCtr), # Bezier link from provider to here
             ((provXCtr + xLoc)/2., provYCtr),
             (xLoc, (provYCtr + yLoc)/2.),
             (xLoc, yLoc))
    bezPath = Path(verts, codes)
    bezPatch = patches.PathPatch(bezPath, facecolor='none', 
                              lw=1, ec='#afafaf', visible=False)

    # Agent ID number below circle
    idText = ax.text(xLoc-.04, yLoc-.21, '%d'%agtId, visible=False)

    # Append to agents list    
    agents.append({'id':agtId,
                   'circ':circle,
                   'bezPatch':bezPatch,
                   'xLoc':xLoc,
                   'yLoc':yLoc,
                   'xVal':xVal,
                   'iVal':iVal,   
                   'treating':False,
                   'enrolled':False,
                   'nSched':0,
                   'treatNo':0,
                   'idText':idText})
    ax.add_patch(bezPatch)
    bezLines.append(bezPatch)
    agentId += 1
    
    

avgInput = totInput/float(nAgents)

    
# for agent in range(len(agents)):
#     print 'id: %d'%id

# Service provider square and 2 sigma range
square = plt.Rectangle((provXOrg, provYOrg), 
                       provSize, provSize, fc=(0,1,0), ec='k')
ax.add_patch(square)
circle = plt.Circle((provXOrg, provYOrg), radius=rSigma, ec='r', fc='none',
                    linestyle='dashed', visible=False )
ax.add_patch(circle)

#### Update Schedule ####
def updateSched(schedList):
    # print '\nIn UpdateSched():'
    ax3.clear()
    ax3.set_xticklabels([])
    ax3.set_yticklabels([])
    ax3.set_xticks(range(1, 13))
    ax3.set_yticks(range(1, maxEnrolled))
    ax3.set_xlim((0, 13))
    ax3.set_ylim((0, maxEnrolled))
    ax3.grid(True)
    for indx, sched in enumerate(schedList):
        # print repr(sched)
        ax3.text(.4, maxEnrolled - 1 - indx, str(sched[0]), size=10,
                 bbox=dict(fc='w', ec='w'))
        agentId = schedList[indx][0]
        for treatment in range(agents[agentId]['treatNo']):
            xVal = schedList[indx][treatment+1]
            r = (1. - xVal)
            g = xVal
            tile = plt.Rectangle((2 + treatment, maxEnrolled - 1 - indx), 1, 1,
                                 fc=(r,g,0))
            ax3.add_patch(tile)
                 
        

#### Update single agent ####
def update_agent(agent):
    
    global nEnrolled, schedList, schedPtr, tileListPtr

    xVal = agent['xVal']
    inputVal = agent['iVal']
        
    # If service is on, service the agents    
    if checkService:
        square.set_fc('#00ff00')
        
        # If not scheduled for treatment consider enrolling
        if not agent['enrolled']:
            need = max((avgInput - xVal),0.)
            
            # Calculate need
            if checkDist:
                distProvX, distProvY = (agent['xLoc'] - provXOrg,
                                        agent['yLoc'] - provYOrg)
                distProv = np.sqrt(distProvX**2 + distProvY**2)
                gauss = (1./rSigma*np.sqrt(2.*np.pi)) * \
                        np.exp(-(distProv**2.)/(2.*rSigma**2))
                # print 'dx=%4.2f\tdy=%4.2f\tdistProv =\t%4.2f gauss=%12.5f'%(distProvX,distProvY,distProv, gauss) 
                probEnroll = need * (maxEnrolled - nEnrolled) * gauss
            else:
                probEnroll = need * (maxEnrolled - nEnrolled)
                
            # If enroll probability exceeds random threshold then enroll
            if probEnroll > np.random.random():
                nEnrolled += 1
                agent['nSched'] = standardSched
                agent['bezPatch'].set_visible(True)
                inputVal = agent['iVal']
                agent['idText'].set_visible(True)
                
                # Register in schedList[]
                # print 'Enrolling agent %d'%agent['id']
                treatList = [-1 for i in range(standardSched)]
                # treatList.insert(0,int(agent['idText'].get_text()))
                treatList.insert(0,agent['id'])
                schedList.append(treatList)
                # schedPtr += 1
                updateSched(schedList)               

        # Otherwise if already enrolled compute input treatment
        else:
            if random() > .25: # Randomize every other time to break sync
                
                # If patient not being treated do next treatment
                if agent['treating'] == False:
                    # print '  agent %d not being treated start treating'%agent['id']
                    agent['treating'] = True
                    agent['bezPatch'].set_lw(2)
                    agent['bezPatch'].set_ec('#00ff00')
                    inputVal = agent['iVal']
                    treatNo = (agent['treatNo'] + 1)
                    if treatNo == standardSched + 1:
                        # print '  agent %d last treatment %d'%(agent['id'], treatNo)
                        agent['treatNo'] = 0
                    else:
                        agent['treatNo'] = treatNo
                        # print '  start treatment %d wellness %5.2f'%(treatNo, agent['xVal'])
                        for indx, entry in enumerate(schedList):
                            # print repr(entry)
                            if entry[0] == int(agent['id']):
                                schedList[indx][treatNo] = agent['xVal']
                                break
                    updateSched(schedList)
                    
                    
                    
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
                    # print '  agent %d treating %d on turn off'%(agent['id'], agent['nSched'])
                    
                    # If treatment program done, un-enroll
                    if agent['nSched'] <= 0:
                        agent['nSched'] = 0
                        agent['enrolled'] = False
                        nEnrolled -= 1
                        agent['treating'] = 0.;
                        agent['bezPatch'].set_lw(1)
                        agent['bezPatch'].set_ec('#afafaf')
                        agent['bezPatch'].set_visible(False)
                        agent['idText'].set_visible(False)
                        # print 'UN-Enrolling agent %d treatment done'%agent['id']
                        for entry in schedList:
                            # print repr(entry)
                            if entry[0] == int(agent['id']):
                                schedList.remove(entry)
                                break
                        updateSched(schedList)
                        
                        
                        # schedList = [x for x in schedList if x[0] != agent['id']]
                        
    
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
