# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 17:17:16 2015

@author: slehar
"""

import axes
import agents
import updateagent


#### Update each loop ####
def update(num):

    global linetime, linedat
    global x,t,lastX,lastT
    global dArray, tArray
    
    # print '  In update count = %d'%num

    if axes.checkPause:
        return

    sumPtsd = 0.
    for agnum in range(agents.nAgents):
        updateagent.update_agent(agents.agents[agnum])
        sumPtsd += agents.agents[agnum]['xVal']

    avgPtsd = sumPtsd / float(agents.nAgents)
    # print '  avgPtsd = %f'%avgPtsd

    x = avgPtsd
    agents.lastT = agents.t
    agents.t += agents.dt
    agents.dArray.appendleft(x)
    if len(agents.dArray) > axes.plotWidth / agents.dt:
        agents.dArray.pop()
    agents.tArray.appendleft(agents.t)
    if len(agents.tArray) > axes.plotWidth / agents.dt:
        agents.tArray.pop()
    axes.line.set_data(agents.tArray,agents.dArray)
    axes.ax2.axis((agents.t - axes.plotWidth, agents.t, axes.ax2yMin, axes.ax2yMax))
