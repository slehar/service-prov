# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 15:39:06 2015

@author: slehar
"""
import StringIO
import matplotlib.pyplot as plt

import agents
import writelog
import axes

# function printSched
def printSched(schedList):
    for indx, entry in enumerate(schedList):
        outStr=StringIO.StringIO()
        outStr.write(' %3d: ['%entry[0])
        
        outStr.write(' %3d: ['%entry[0])
        for tr in range(1,agents.standardSched+1):
            if entry[tr] == None:
                outStr.write('  ~  ')
            else:
                outStr.write('%4.2f '%entry[tr])
        outStr.write(']\n')
        writelog.write(outStr.getvalue())
        outStr.close()

#### Update Schedule ####
def updateSched(schedList):
    # print '\nIn UpdateSched():'
    axes.ax3.clear()
    axes.ax3.set_xticklabels([])
    axes.ax3.set_yticklabels([])
    axes.ax3.set_xticks(range(1, 7))
    axes.ax3.set_yticks(range(1, agents.maxEnrolled))
    axes.ax3.set_xlim((0, 7))
    axes.ax3.set_ylim((0, agents.maxEnrolled))
    axes.ax3.grid(True)
    for indx, sched in enumerate(schedList):
        # print repr(sched)
        axes.ax3.text(.4, agents.maxEnrolled - 1 - indx + .3, str(sched[0]), size=12,
                 bbox=dict(fc='w', ec='w'))
        agentId = schedList[indx][0]
        for treatment in range(1, agents.agents[agentId]['treatNo']+1):
            if schedList[indx][treatment]:
                xVal = schedList[indx][treatment]
                r = (1. - xVal)
                g = xVal
                tile = plt.Rectangle((1 + treatment, agents.maxEnrolled - 1 - indx), 1, 1,
                                     fc=(r,g,0))
                axes.ax3.add_patch(tile)

