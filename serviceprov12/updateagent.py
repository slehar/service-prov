# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 12:17:56 2015

@author: slehar
"""

import numpy as np
from random import random
import time

import writelog
import axes
import agents
import sched


#### Update single agent ####
def update_agent(agent):

    global nEnrolled, schedList, schedPtr, tileListPtr, avgInput

    # print '  In update_agent agent = %d'%agent['id']
    # writelog.write('In update_agent agent = %d\n'%agent['id'])

    xVal = agent['xVal']
    inputVal = agent['iVal']

    # If service is on, service the agents
    if axes.checkService:
        agents.square.set_fc('#00ff00')

        # If not scheduled for treatment consider enrolling
        if not agent['enrolled']:
            need = max((agents.avgInput - xVal),0.)
            # writelog.write('  not enrolled avgInput= %5.2f xVal= %5.2f need=%5.2f\n'%
            #                     (avgInput, xVal, need))

            # Calculate probability of enrollment based on need
            if axes.checkDist:
                distProvX, distProvY = (agent['xLoc'] - axes.provXOrg,
                                        agent['yLoc'] - axes.provYOrg)
                distProv = np.sqrt(distProvX**2 + distProvY**2)
                gauss = (1./agents.rSigma*np.sqrt(2.*np.pi)) * \
                        np.exp(-(distProv**2.)/(2.*agents.rSigma**2))
                probEnroll = need * (agents.maxEnrolled - agents.nEnrolled) * gauss
            else:
                probEnroll = need * (agents.maxEnrolled - agents.nEnrolled)
                
            # writelog.write('  need = %f probEnroll = %5.2f\n'%(need,probEnroll))

            # If enroll probability exceeds random threshold then enroll
            if probEnroll > random():
                # writelog.write('  probEnroll > random\n')
                agent['enrolled'] = True
                agents.nEnrolled += 1
                # agent['nSched'] = standardSched
                agent['bezPatch'].set_visible(True)
                inputVal = agent['iVal']
                agent['idText'].set_visible(True)

                # Register in schedList[]
                # writelog.write('About to enroll\n')
                if agents.doingLogging:
                    writelog.write('Enrolling agent %d\n'% agent['id'])
                treatList = [None for i in range(agents.standardSched)]
                treatList[agent['treatNo']] = agent['xVal']
                treatList.insert(0,agent['id'])
                sched.schedList.append(treatList)

                # update schedule
                sched.updateSched(sched.schedList)
                if agents.doingLogging:
                    sched.printSched(sched.schedList)

        # Otherwise if already enrolled compute input treatment
        else:
            if random() > .25: # Randomize every other time to break sync

                # If agent not being treated do next treatment
                if agent['treating'] == False:
                    if agents.doingLogging:
                        writelog.write('  agent %d treatment %d ON\n'%(agent['id'], 
                                                                          agent['treatNo']))
                    agent['treating'] = True
                    agent['bezPatch'].set_lw(2)
                    agent['bezPatch'].set_ec('#00ff00')

                    # Turn on input
                    if axes.checkEndBen:
                        agent['iVal'] += agents.doseValue/10. # endBen increase iVal
                    else:
                        inputVal = agent['iVal'] + agents.doseValue
                        
                    # Increment treatment number
                    agent['treatNo'] += 1
 
                    if agent['treatNo'] >= agents.standardSched+1:
                        writelog.write('  treatNo = %d standardSched = %d\n'%
                                         (agent['treatNo'], agents.standardSched))
                        if agents.doingLogging: writelog.write('Un-enroll agent %d treatment done\n'% 
                                                            agent['id'])
                        agent['enrolled'] = False
                        agent['treatNo'] = 0
                        # agent['treating'] = False
                        agents.nEnrolled -= 1
                        agent['bezPatch'].set_lw(1)
                        agent['bezPatch'].set_visible(False)
                        agent['idText'].set_visible(False)
                        for entry in sched.schedList:
                            if entry[0] == int(agent['id']):
                                sched.schedList.remove(entry)
                                break
                    else:
                        for indx, sch in enumerate(sched.schedList):
                            if sch[0] == int(agent['id']):
                                sched.schedList[indx][agent['treatNo']] = agent['xVal']
                                break
                        if agents.doingLogging: writelog.write('  agent %d treatment %d ON\n'%
                                           (agent['id'], agent['treatNo']))

                    # Update schedule
                    sched.updateSched(sched.schedList)
                    if agents.doingLogging:
                        sched.printSched(sched.schedList)

                # Otherwise if patient being treated turn it off
                else:
                    agent['treating'] = False;
                    agent['bezPatch'].set_lw(1)
                    agent['bezPatch'].set_ec('#afafaf')
                    inputVal = agent['iVal']

                    if agents.doingLogging: writelog.write('  agent %d treatment %d OFF\n'%
                                        (agent['id'], agent['treatNo']))

                        # schedList = [x for x in schedList if x[0] != agent['id']]


    # Else if service is off, shut off treatment
    else:
        agent['bezPatch'].set_visible(False)
        agents.square.set_fc('#ffffff')
        inputVal = agent['iVal']


    # Shunting equation
    xVal += -agents.A * xVal + (1 - xVal) * inputVal
    if xVal < 0.:
        xVal = 0.
    elif xVal > 1.:
        xVal = 1.
    agent['xVal'] = xVal
    r = (1. - xVal)
    g = xVal
    agent['circ'].set_facecolor((r, g, 0.))

    # Time delay
    if agents.delay > 0.:
        time.sleep(agents.delay)
