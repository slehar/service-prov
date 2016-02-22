# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 15:36:41 2015

@author: slehar
"""
from random import random, seed, randint
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as mpatches
from collections import deque
import StringIO
import time

# Local modules
import axes
import image
import writelog

# Global variables
avgPtsd = 0.
# nAgents = 150
nAgents = 500
nAgentsWht = 0
nAgentsBlk = 0
nAgentsOth = 0
nEnrolled = 0
maxEnrolled = 6
useProbCBT = False
# standardSched = 6
standardSched = 10
steppedSched = 5
avgInput = 0.
square = None
circle = None
circRad1 = .001
circRad2 = .006
circRad3 = .008
schedList = []
schedPtr = 0
tileArray = []
doingLogging = True
doseValue = .2
delay = 0.0
A = 0.1   # Shunting decay term
iThresh = .2 # Threshold for iVal eligibility for complex PTSD
x = 0.001
visThresh = 0.4 # Threshold for visibility on screen
dt = 1.
preLaunch = 0.
t = -preLaunch
lastX = 0.
lastT = 0.
dArray    = deque([0.])
tArray    = deque([0.])
dArrayWht = deque([0.])
dArrayBlk = deque([0.])
dArrayOth = deque([0.])
dArrayNptsd = deque([0.])
plotWidth = 500

agents = []
totInput = 0.

minSep = .0025
rSigma = .3

# Initialize random seed
seed(3)
writelog.init('run.log')


# Codes for four-point Bezier spline
codes = [Path.MOVETO,
         Path.CURVE4,
         Path.CURVE4,
         Path.CURVE4,
         ]

         
#%%########[ probRaceEthncy ]#######
def probRaceEthncy(borough):
#
# Sets 5 thresholds to determine for each borough based on the demographics the proportion
# of the population that falls into 6 categories:
# Non-Hispanic(White, Black, Other), Hispanic(White, Black, Other)
#

    # Manhattan
    if borough == 1:
        t1 = 47.742487
        t2 = 60.763558
        t3 = 74.366567
        t4 = 83.561831
        t5 = 86.056359
    # Brooklyn
    elif borough == 2:
        t1 = 35.676751
        t2 = 67.905354
        t3 = 80.196121
        t4 = 89.087490
        t5 = 91.069430
    # Queens
    elif borough == 3:
        t1 = 27.562720
        t2 = 45.262120
        t3 = 72.521485
        t4 = 87.476018
        t5 = 88.637401
    # Bronx
    elif borough == 4:
        t1 = 10.933492
        t2 = 41.213491
        t3 = 46.482021
        t4 = 58.057408
        t5 = 62.525787
    # Staten Island
    elif borough == 5:
        t1 = 64.176278
        t2 = 73.712461
        t3 = 82.825904
        t4 = 94.408742
        t5 = 95.256355
    else:
        print "ERROR probRaceEthncy illegal borough %d"%borough
        return('White', 'Non-Hispanic')
        
    r = random() * 100.
    if r < t1:
        race   = 'White'
        ethncy = 'Non-Hispanic'
    elif r < t2:
        race   = 'Black'
        ethncy = 'Non-Hispanic'
    elif r < t3:
        race   = 'Other'
        ethncy = 'Non-Hispanic'
    elif r < t4:
        race   = 'White'
        ethncy = 'Hispanic'
    elif r < t5:
        race   = 'Black'
        ethncy = 'Hispanic'
    else:
        race   = 'Other'
        ethncy = 'Hispanic'
        
    return(race, ethncy)
        
#%%# Calculate distribution
def calculate_distribution(isMale, isOld, isBlack, isWhite, isOther, isHisp, hadPrior):
    
    logitCBT = -1.60 +                \
              (-0.2008   * isMale)  + \
              (-0.5828   * isBlack) + \
              (-1.073    * isHisp)  + \
              (-0.35     * isOther) + \
              (0.2449    * isOld)   + \
              (1.8377    * hadPrior)
              
    return np.exp(logitCBT)/(1. + np.exp(logitCBT))


#%%#### Initialize single agent ####
def init_agent(agtId):

    global nEnrolled, schedList, schedPtr, avgInput
    global agents, nAgents, square, circle, avgInput, \
            nAgentsWht, nAgentsBlk, nAgentsOth


    foundSpace = False
    while not foundSpace:
        xLoc = random() * image.aspect + .1*image.aspect
        yLoc = random()
        writelog.write("agtId: % 3d  xLoc, yLoc = (%4.2f, %4.2f)\n"%(agtId, xLoc, yLoc))
        
        inMask  = image.maskImg[image.imgYSize - yLoc * image.imgYSize,
                                 (xLoc-image.xOff)*image.imgXSize/image.aspect + image.xOff][0]
                            
        borough = image.burrIndx[image.imgYSize - yLoc * image.imgYSize,
                                  (xLoc-image.xOff)*image.imgXSize/image.aspect + image.xOff]
        borough -= 1  #<=== KLUDGE! (Don't know why this is necessary)
        writelog.write("agtId: % 3d  xLoc, yLoc = (%4.2f, %4.2f) borough = %3d\n"%(
                        agtId, xLoc, yLoc, borough))
        
        # if inMask > .5 and borough in range(1,6):  # If in the masked area check for collision
        if inMask > .9:  # If in the masked area check for collision
            writelog.write('  In borough %3d\n'%borough)
            collision = False
            for agt in range(len(agents)):
                xLoc1 = agents[agt]['xLoc']
                yLoc1 = agents[agt]['yLoc']
                dx = xLoc1 - xLoc
                dy = yLoc1 - yLoc
                dist = np.sqrt(dx**2 + dy**2)
                if dist < minSep:
                    collision = True
                    writelog.write("  COLLISION !!!\n")
                    break   # Stop going through more agents
            if not collision:
                foundSpace = True
                writelog.write("agtId: % 3d  xLoc, yLoc = (%4.2f, %4.2f) borough = %3d\n"%(
                                agtId, xLoc, yLoc, borough))
                writelog.write("  foundSpace!\n")
                # Otherwise keep searching

        
    # Define agent's race and ethnicity
    (race, ethncy) = probRaceEthncy(borough)
    if race == 'White':
        raceColor = 'w'
        isWhite = 1.
        isBlack = 0.
        isOther = 0.
        nAgentsWht += 1
    elif race == 'Black':
        raceColor = 'k'
        isWhite = 0.
        isBlack = 1.
        isOther = 0.
        nAgentsBlk += 1
    elif race == 'Other':
        raceColor = 'gray'
        isWhite = 0.
        isBlack = 0.
        isOther = 1.
        nAgentsOth += 1
        
    if ethncy == 'Hispanic':
        ethVis = True
        isHisp = 1.
    else:
        ethVis = False
        isHisp = 0.
    
    # Define agent's gender
    if random() > .5:
        gender = 'Male'
        isMale = 1.
    else:
        gender = 'Female'
        isMale = 0.
        
    # Define agent's age
    if random() > .75:
        isOld = 1.
    else:
        isOld = 0.
        
    # Define agent's hadPrior (PTSD)
    if random() > .9:
        hadPrior = 1.
    else:
        hadPrior = 0.
    
    # Define agent's "input value" (natural wellness) and input factor
    # Using probCBT
    if useProbCBT:
        fstr = '  isMale=%1d isOld=%1d isBlack=%1d isWhite=%1d isOther=%1d '\
               'isHisp=%1d hadPrior=%1d\n'
        writelog.write(fstr%(isMale, isOld, isBlack, isWhite,
                                      isOther, isHisp, hadPrior))
        probCBT = calculate_distribution(isMale, isOld, isBlack, isWhite,
                                      isOther, isHisp, hadPrior)
        iVal = 1. - probCBT
        if iVal > 1:
            iVal = 1.
        elif iVal < 0.:
            iVal = 0.
            
        writelog.write('  calculate_distribution: probCBT = %f iVal = %f\n'%(probCBT,iVal))
    # Or using just random
    else:
        iVal = random()
        writelog.write('  calculate_input: iVal = %f\n'%iVal)
            

    if iVal > iThresh:
        iFact = 1.
        isComplex = False
        cmplxColor = 'k'
    else:
        if random() > .5:
            iFact = 1.
            isComplex = False
            cmplxColor = 'k'
        else:
            iFact = 0.7
            isComplex = True
            cmplxColor = 'r'

    # Set xVal to equilibrium value
    xVal = iVal/(A+iVal)
    # totInput += iVal
    r = (1. - xVal)
    g = xVal

    # Define agent's triple circle & wedge
    circle1 = plt.Circle((xLoc, yLoc), circRad1, fc=(r,g,0),
                         ec=cmplxColor)
    '''
    circle2 = plt.Circle((xLoc, yLoc), circRad2, fc=cmplxColor,
                         ec=cmplxColor)
    circle3 = plt.Circle((xLoc, yLoc), circRad3, fc=raceColor,
                         ec=raceColor)
    wedge   = mpatches.Wedge((xLoc, yLoc), circRad3, 180, 0,
                             fc='brown', ec='brown', visible=ethVis)
    
    axes.ax.add_patch(circle3)
    axes.ax.add_patch(wedge)
    axes.ax.add_patch(circle2)
    '''
    if xVal > visThresh:
        circle1.set_visible(False)
    else:
        circle1.set_visible(True)
    axes.ax.add_patch(circle1)
     
    # Define agent's bezier links
    verts = ((axes.provXCtr, axes.provYCtr), # Bezier lnk from prov. to here
             ((axes.provXCtr + xLoc)/2., axes.provYCtr),
             (xLoc, (axes.provYCtr + yLoc)/2.),
             (xLoc, yLoc))
    bezPath = Path(verts, codes)
    bezPatch = mpatches.PathPatch(bezPath, facecolor='none',
                              lw=1, ec='#afafaf', visible=False)
    axes.ax.add_patch(bezPatch)
                              
    '''
    # Define agent's gender symbol
    if gender == 'Male':
        xData = [xLoc + circRad2, 
                 xLoc + 1.5*circRad2, 
                 xLoc + 1.5*circRad2-circRad2/2,
                 xLoc + 1.5*circRad2, 
                 xLoc + 1.5*circRad2] 
        yData = [yLoc + circRad2, 
                 yLoc + 1.5*circRad2, 
                 yLoc + 1.5*circRad2,
                 yLoc + 1.5*circRad2, 
                 yLoc + 1.5*circRad2-circRad2/2] 
    elif gender == 'Female':
        xData = [xLoc, 
                 xLoc, 
                 xLoc,
                 xLoc - .5*circRad2, 
                 xLoc + .5*circRad2] 
        yData = [yLoc - circRad2, 
                 yLoc - 2*circRad2, 
                 yLoc - 1.5*circRad2,
                 yLoc - 1.5*circRad2, 
                 yLoc - 1.5*circRad2] 
    gendSymb = plt.Line2D(xData, yData, color='k')
    axes.ax.add_line(gendSymb)
    '''

    # Agent ID number below circle
    idText = axes.ax.text(xLoc-.004, yLoc-.021, '%d'%agtId, visible=False)
    
    newAgent =    {'id':agtId,
                   'circ1':circle1,
                   'bezPatch':bezPatch,
                   'xLoc':xLoc,
                   'yLoc':yLoc,
                   'xVal':xVal,
                   'iVal':iVal,
                   'iFact':iFact,
                   'isComplex':isComplex,
                   'gender':gender,
                   'race':race,
                   'ethncy':ethncy,
                   'treating':False,
                   'enrolled':False,
                   'treatNo':0,        # current treatment #
                   'idText':idText}
    return newAgent




#%%########[ init agents ]########
def init_agents():
    
    global agents, nAgents, square, circle, avgInput, \
            nAgentsWht, nAgentsBlk, nAgentsOth, avgInput
    
    totInput = 0.
    
    ## for each agent
    for agtId in range(nAgents):
        # 
        writelog.write("agtId = %d\n"%agtId)
        newAgent = init_agent(agtId)
        
        # Append to agents list
        agents.append(newAgent)
        totInput += newAgent['iVal']
        
    
    
    avgInput = totInput/float(nAgents)
    
    # Service provider square and 2 sigma range
    square = plt.Rectangle((axes.provXOrg, axes.provYOrg),
                           axes.provSize, axes.provSize, fc=(0,1,0), ec='k')
    axes.ax.add_patch(square)
    
    # Dist feature sigma radius dashed circle
    circle = plt.Circle((axes.provXOrg, axes.provYOrg), radius=rSigma, ec='r',
                        fc='none', linestyle='dashed', visible=axes.checkDist)
    axes.ax.add_patch(circle)


#%%# function printSched
def printSched():
    for indx, entry in enumerate(schedList):
        outStr=StringIO.StringIO()
        if entry[1]:
            stateStr = 'X'
        else:
            stateStr = ' '
        outStr.write(' %3d: %s ['%(entry[0], stateStr))
        
        # outStr.write(' %3d: %s ['%(entry[0], ststr)) # Duplicate line?
        for tr in range(2,standardSched+2):
            if entry[tr] == None:
                outStr.write('  ~  ')
            else:
                outStr.write('%4.2f '%entry[tr])
        outStr.write(']\n')
        writelog.write(outStr.getvalue())
        outStr.close()

#%%#### Initialize Schedule ####
def initSched(schedList, tileArray):
    
    axes.ax3.set_xticklabels([])
    axes.ax3.set_yticklabels([])
    axes.ax3.set_xticks(range(1, standardSched+2))
    axes.ax3.set_yticks(range(1, maxEnrolled))
    axes.ax3.set_xlim((0, standardSched+2))
    axes.ax3.set_ylim((0, maxEnrolled))
    axes.ax3.grid(True)

    for row in range(maxEnrolled):
        newRow = []
        newRow.append(axes.ax3.text(1, maxEnrolled - 1 - row + .3, "   ", 
                      size=12, family='Monospace', horizontalalignment='right',
                      name='Courier', bbox=dict(fc='w', ec=None, lw=2)))
        newRow.append(False)
        for col in range(2, standardSched+2):
            newTile = plt.Rectangle((col, maxEnrolled - 1 - row), 1, 1, fc='w')
            newRow.append(newTile)
            axes.ax3.add_patch(newTile)
        tileArray.append(newRow)
        


#%%#### Update Schedule ####
def updateSched(schedList, tileArray):
    # print '\nIn UpdateSched():'
    # axes.ax3.clear()

    # vLine1 = plt.Line2D((2,2),(0,6), lw=4, color='g')
    # axes.ax3.add_line(vLine1)
    for indx, entry in enumerate(schedList):
        # print repr(sched)
        if entry[1]:
            ec = 'r'
        else:
            ec = None
        tileArray[indx][0].set_bbox(dict(fc='w', ec=ec, lw=2))
        tileArray[indx][0].set_text("%3d"%entry[0])
        for treatment in range(2, standardSched+2):
            if schedList[indx][treatment]:
                xVal = schedList[indx][treatment]
                r = (1. - xVal)
                g = xVal
                tileArray[indx][treatment].set_facecolor((r,g,0))
            else:
                tileArray[indx][treatment].set_facecolor('w')



#%%#### Update single agent ####
def update_agent(agent):

    global nEnrolled, schedList, schedPtr, avgInput

    # print '  In update_agent agent = %r'%agent
    # writelog.write('In update_agent agent = %r\n'%agent)

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

            # Calculate probability of enrollment based on need (and distance from provider)
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
                # update schedule
                updateSched(schedList, tileArray)
                if doingLogging:
                    printSched()

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
                        agent['iVal'] += doseValue*agent['iFact']/10. # endBen increase iVal
                    else:
                        inputVal = agent['iVal'] + doseValue  * agent['iFact']
                        
                    # Increment treatment number
                    agent['treatNo'] += 1
 
                    if axes.checkStepped and not agent['isComplex']:
                        nTreatLeft = steppedSched + 1
                    else:
                        nTreatLeft = standardSched + 1
                    if agent['treatNo'] >= nTreatLeft:
                        
                        if axes.checkStepped and not agent['isComplex']:
                            writelog.write('  treatNo = %d steppedSched = %d\n'%
                                         (agent['treatNo'], steppedSched))
                        else:
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
                        for indx, sched in enumerate(schedList):
                            if sched[0] == int(agent['id']):
                                schedList[indx][agent['treatNo']+1] = agent['xVal']
                                break
                        if doingLogging: writelog.write('  agent %d treatment %d ON\n'%
                                           (agent['id'], agent['treatNo']+1))

                    # Update schedule
                    updateSched(schedList, tileArray)
                    if doingLogging:
                        printSched()

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
        inputVal = agent['iVal'] * agent['iFact']


    # Shunting equation
    xVal += -A * xVal + (1 - xVal) * inputVal
    if xVal < 0.:
        xVal = 0.
    elif xVal > 1.:
        xVal = 1.
    agent['xVal'] = xVal
    if xVal > visThresh:
        agent['circ1'].set_visible(False)
    else:
        agent['circ1'].set_visible(True)
    r = (1. - xVal)
    g = xVal
    agent['circ1'].set_facecolor((r, g, 0.))

    # Time delay
    if delay > 0.:
        time.sleep(delay)

#%%#### Update each loop ####
def update(num):

    global linetime, linedat
    global x,t,lastX,lastT
    global dArray, tArray, dArrayWht, dArrayBlk, dArrayOth, dArrayNptsd, nAgents
    global lastTime
    # global sumPtsdWht, sumPtsdBlk, sumPtsdOth
    # print '  In update count = %d'%num

    if axes.checkPause:
        return
 
    sumPtsd = sumPtsdWht = sumPtsdBlk = sumPtsdOth = 0.
    nPtsd = 0
    for agnum in range(nAgents):
        update_agent(agents[agnum]) # <====== update_agent()
        if agents[agnum]['xVal'] < visThresh:
            nPtsd += 1
        sumPtsd += agents[agnum]['xVal']
        if agents[agnum]['race'] == 'White':
            sumPtsdWht += agents[agnum]['xVal']
        elif agents[agnum]['race'] == 'Black':
            sumPtsdBlk += agents[agnum]['xVal']
        elif agents[agnum]['race'] == 'Other':
            sumPtsdOth += agents[agnum]['xVal']
    #nPtsd = nPtsd/10

    avgPtsd = sumPtsd / float(nAgents)
    # print '  avgPtsd = %f'%avgPtsd
    avgPtsdWht = sumPtsdWht / float(nAgentsWht)
    avgPtsdBlk = sumPtsdBlk / float(nAgentsBlk)
    avgPtsdOth = sumPtsdOth / float(nAgentsOth)

    x = avgPtsd
    xWht = avgPtsdWht
    xBlk = avgPtsdBlk
    xOth = avgPtsdOth
    lastT = t
    t += dt
    dArray.appendleft(x)
    if len(dArray) > plotWidth / dt:
        dArray.pop()
        
    dArrayWht.appendleft(xWht)
    if len(dArrayWht) > plotWidth / dt:
        dArrayWht.pop()
        
    dArrayBlk.appendleft(xBlk)
    if len(dArrayBlk) > plotWidth / dt:
        dArrayBlk.pop()
        
    dArrayOth.appendleft(xOth)
    if len(dArrayOth) > plotWidth / dt:
        dArrayOth.pop()
        
    dArrayNptsd.appendleft(nPtsd)
    if len(dArrayNptsd) > plotWidth / dt:
        dArrayNptsd.pop()
        
    tArray.appendleft(t)
    if len(tArray) > plotWidth / dt:
        tArray.pop()

    axes.line.set_data(tArray, dArray)
    axes.lineWht.set_data(tArray, dArrayWht)
    axes.lineBlk.set_data(tArray, dArrayBlk)
    axes.lineOth.set_data(tArray, dArrayOth)
    axes.lineNptsd.set_data(tArray, dArrayNptsd)
    axes.ax2.axis((t - plotWidth, t, axes.ax2yMin, axes.ax2yMax))
    
    # Create new PTSD cases after t > 0 
    if t >= 0:
        probNew = 10. * np.exp(-(t/10.))
        for num in range(int(probNew)):
            randId = randint(0,nAgents)
            agents[randId]['iVal'] = random()*visThresh
            agents[randId]['circ1'].set_visible(True)
            agents[randId]['isComplex'] = (agents[randId]['iVal'] < iThresh)
    
    

