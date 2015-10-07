# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 15:36:41 2015

@author: slehar
"""
from random import random, seed
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
from collections import deque
import time

# Local modules
import axes
import writelog
import sched

# Global variables
avgPtsd = 0.
nAgents = 100
nEnrolled = 0
maxEnrolled = 6
standardSched = 5
avgInput = 0.
square = None
circle = None
schedList = []
schedPtr = 0
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

########[ init agents ]########
def init_agents():
    
    global agents, nAgents, square, circle, avgInput
    
    totInput = 0.
    agentId = 0
    
    ## for each agent
    for agtId in range(nAgents):
        # writelog.write("agtId = %d\n"%agtId)
        foundSpace = False
        while not foundSpace:
            xLoc = random() * 8. + 1.
            yLoc = random() * 7. + 1.
            # writelog.write("  xLoc, yLoc = (%4.2f, %4.2f)\n"%(xLoc, yLoc))
            collision = False
            for agt in range(len(agents)):
                xLoc1 = agents[agt]['xLoc']
                yLoc1 = agents[agt]['yLoc']
                dx = xLoc1 - xLoc
                dy = yLoc1 - yLoc
                dist = np.sqrt(dx**2 + dy**2)
                if dist < minSep:
                    collision = True
                    # writelog.write("  COLLISION !!!\n")
                    break   # Stop going through more agents
            if not collision:
                foundSpace = True
                # Otherwise keep searching
    
        # Define agent's circle
        circle = plt.Circle((xLoc, yLoc), .1, fc='r', ec='k')
        axes.ax.add_patch(circle)
    
        # Define agent's bezier links
        iVal = random()  # Random input value (natural wellness)
        # xVal = iVal * 10.
        xVal = .75
        totInput += iVal
        verts = ((axes.provXCtr, axes.provYCtr), # Bezier lnk from prov. to here
                 ((axes.provXCtr + xLoc)/2., axes.provYCtr),
                 (xLoc, (axes.provYCtr + yLoc)/2.),
                 (xLoc, yLoc))
        bezPath = Path(verts, codes)
        bezPatch = patches.PathPatch(bezPath, facecolor='none',
                                  lw=1, ec='#afafaf', visible=False)
    
        # Agent ID number below circle
        idText = axes.ax.text(xLoc-.04, yLoc-.21, '%d'%agtId, visible=False)
    
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
                       'treatNo':0,        # current treatment #
                       'idText':idText})
        axes.ax.add_patch(bezPatch)
        bezLines.append(bezPatch)
        agentId += 1
    
    
    
    avgInput = totInput/float(nAgents)
    
    # Service provider square and 2 sigma range
    square = plt.Rectangle((axes.provXOrg, axes.provYOrg),
                           axes.provSize, axes.provSize, fc=(0,1,0), ec='k')
    axes.ax.add_patch(square)
    circle = plt.Circle((axes.provXOrg, axes.provYOrg), radius=rSigma, ec='r',
                        fc='none', linestyle='dashed', visible=False )
    axes.ax.add_patch(circle)



#### Update single agent ####
def update_agent(agent):

    global nEnrolled, schedList, schedPtr, tileListPtr, avgInput

    # print '  In update_agent agent = %d'%agent['id']
    # writelog.write('In update_agent agent = %d\n'%agent['id'])

    xVal = agent['xVal']
    inputVal = agent['iVal']

    # If service is on, service the agents
    if axes.checkService:
        square.set_fc('#00ff00')

        # If not scheduled for treatment consider enrolling
        if not agent['enrolled']:
            need = max((avgInput - xVal),0.)
            # writelog.write('  not enrolled avgInput= %5.2f xVal= %5.2f need=%5.2f\n'%
            #                     (avgInput, xVal, need))

            # Calculate probability of enrollment based on need
            if axes.checkDist:
                distProvX, distProvY = (agent['xLoc'] - axes.provXOrg,
                                        agent['yLoc'] - axes.provYOrg)
                distProv = np.sqrt(distProvX**2 + distProvY**2)
                gauss = (1./rSigma*np.sqrt(2.*np.pi)) * \
                        np.exp(-(distProv**2.)/(2.*rSigma**2))
                probEnroll = need * (maxEnrolled - nEnrolled) * gauss
            else:
                probEnroll = need * (maxEnrolled - nEnrolled)
                
            # writelog.write('  need = %f probEnroll = %5.2f\n'%(need,probEnroll))

            # If enroll probability exceeds random threshold then enroll
            if probEnroll > random():
                # writelog.write('  probEnroll > random\n')
                agent['enrolled'] = True
                nEnrolled += 1
                # agent['nSched'] = standardSched
                agent['bezPatch'].set_visible(True)
                inputVal = agent['iVal']
                agent['idText'].set_visible(True)

                # Register in schedList[]
                # writelog.write('About to enroll\n')
                if doingLogging:
                    writelog.write('Enrolling agent %d\n'% agent['id'])
                treatList = [None for i in range(standardSched)]
                treatList[agent['treatNo']] = agent['xVal']
                treatList.insert(0,agent['id'])
                schedList.append(treatList)

                # update schedule
                sched.updateSched(schedList)
                if doingLogging:
                    sched.printSched(schedList)

        # Otherwise if already enrolled compute input treatment
        else:
            if random() > .25: # Randomize every other time to break sync

                # If agent not being treated do next treatment
                if agent['treating'] == False:
                    if doingLogging:
                        writelog.write('  agent %d treatment %d ON\n'%(agent['id'], 
                                                                          agent['treatNo']))
                    agent['treating'] = True
                    agent['bezPatch'].set_lw(2)
                    agent['bezPatch'].set_ec('#00ff00')

                    # Turn on input
                    if axes.checkEndBen:
                        agent['iVal'] += doseValue/10. # endBen increase iVal
                    else:
                        inputVal = agent['iVal'] + doseValue
                        
                    # Increment treatment number
                    agent['treatNo'] += 1
 
                    if agent['treatNo'] >= standardSched+1:
                        writelog.write('  treatNo = %d standardSched = %d\n'%
                                         (agent['treatNo'], standardSched))
                        if doingLogging: writelog.write('Un-enroll agent %d treatment done\n'% 
                                                            agent['id'])
                        agent['enrolled'] = False
                        agent['treatNo'] = 0
                        # agent['treating'] = False
                        nEnrolled -= 1
                        agent['bezPatch'].set_lw(1)
                        agent['bezPatch'].set_visible(False)
                        agent['idText'].set_visible(False)
                        for entry in schedList:
                            if entry[0] == int(agent['id']):
                                schedList.remove(entry)
                                break
                    else:
                        for indx, sch in enumerate(schedList):
                            if sch[0] == int(agent['id']):
                                schedList[indx][agent['treatNo']] = agent['xVal']
                                break
                        if doingLogging: writelog.write('  agent %d treatment %d ON\n'%
                                           (agent['id'], agent['treatNo']))

                    # Update schedule
                    sched.updateSched(schedList)
                    if doingLogging:
                        sched.printSched(schedList)

                # Otherwise if patient being treated turn it off
                else:
                    agent['treating'] = False;
                    agent['bezPatch'].set_lw(1)
                    agent['bezPatch'].set_ec('#afafaf')
                    inputVal = agent['iVal']

                    if doingLogging: writelog.write('  agent %d treatment %d OFF\n'%
                                        (agent['id'], agent['treatNo']))

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

    global linetime, linedat
    global x,t,lastX,lastT
    global dArray, tArray
    
    # print '  In update count = %d'%num

    if axes.checkPause:
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
    axes.line.set_data(tArray,dArray)
    axes.ax2.axis((t - plotWidth, t, axes.ax2yMin, axes.ax2yMax))
    # time.sleep(.1)

