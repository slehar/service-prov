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
import re
import os

# Local modules
import axes
import agencies
import image
import writelog

# Global variables
avgPtsd = 0.
nPtsd = 0
# nAgents = 150
nAgents = 500
nAgentsWht = 0
nAgentsBlk = 0
nAgentsOth = 0
nEnrolled = 0
maxEnrolled = 6
useProbCBTnSymptoms  = False
useProbCBTprobEnroll = False
useCalcNSymptoms = True
if useCalcNSymptoms:
    iThresh   = .2  # Set threshold for iVal eligibility for complex PTSD
    visThresh = .4  # Set threshold for visibility on screen
    needFactor = 1.
    boost = 0.
else:
    iThresh   = .2
    visThresh = .4
    needFactor = 1.
    boost = 0.
standardSched = 10
steppedSched = 5
avgInput = 0.
square = None
circle = None
circRad1 = .001
circRad2 = .006
circRad3 = .008
doingLogging = False
doseValue = .2
delay = 0.001
A = 0.1   # Shunting decay term
x = 0.001
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
totInput = [0.]

minSep = .0025
rSigma = .3

dataFileName = ''


# Initialize random seed
seed(3)
if doingLogging:
    writelog.init('run.log')


# Codes for four-point Bezier spline
codes = [Path.MOVETO,
         Path.CURVE4,
         Path.CURVE4,
         Path.CURVE4,
         ]

#%%########[ probRaceEthncy ]#######
def probDemographics(boroIndx):
#
# For each demographic category [Income, Age, Sex, Race-Ethnicity]
# establish thresholds such that a random % variable rand()*100. is
# likely to fall into the appropriate category matching demographics
# for the given borough.5

    ######## Income ########
    # Manhattan
    if boroIndx == 1:
        t1 = 45.517530
        t2 = 62.854290
    # Brooklyn
    elif boroIndx == 2:
        t1 = 60.922812
        t2 = 80.100220
    # Queens
    elif boroIndx == 3:
        t1 = 52.467246
        t2 = 75.805702
    # Bronx
    elif boroIndx == 4:
        t1 = 71.575449
        t2 = 88.467528
    # Staten Island
    elif boroIndx == 5:
        t1 = 41.547579
        t2 = 65.630671
        
    r = random() * 100.
    if r < t1:
        income   = 'Low'
        incomeLow = 1.
        incomeMed = 0.
    elif r < t2:
        income   = 'Medium'
        incomeLow = 0.
        incomeMed = 1.
    else:
        income   = 'High'
        incomeLow = 0.
        incomeMed = 0.
        incomeHigh = 1.
    
    ######## Age ########
    # Manhattan
    if boroIndx == 1:
        t1 = 38.451799
        t2 = 84.108916
    # Brooklyn
    elif boroIndx == 2:
        t1 = 36.061935
        t2 = 84.828344
    # Queens
    elif boroIndx == 3:
        t1 = 32.626660
        t2 = 83.697444
    # Bronx
    elif boroIndx == 4:
        t1 = 35.831148
        t2 = 85.545559
    # Staten Island
    elif boroIndx == 5:
        t1 = 28.890142
        t2 = 83.252253
        
    r = random() * 100.
    if r < t1:
        age = 'Young'
    elif r < t2:
        age = 'Middle'
    else:
        age = 'Old'
    
    ######## Sex ########
    # Manhattan
    if boroIndx == 1:
        t = 52.951241
    # Brooklyn
    elif boroIndx == 2:
        t = 52.794042
    # Queens
    elif boroIndx == 3:
        t = 51.574133
    # Bronx
    elif boroIndx == 4:
        t = 53.062255
    # Staten Island
    elif boroIndx == 5:
        t = 51.539368
    
    r = random() * 100.
    if r < t:
        sex = 'Female'
    else:
        sex = 'Male'
    
    ######## Race / Ethnicity ########

    # Manhattan
    if boroIndx == 1:
        t1 = 47.742487
        t2 = 60.763558
        t3 = 74.366567
        t4 = 83.561831
        t5 = 86.056359
    # Brooklyn
    elif boroIndx == 2:
        t1 = 35.676751
        t2 = 67.905354
        t3 = 80.196121
        t4 = 89.087490
        t5 = 91.069430
    # Queens
    elif boroIndx == 3:
        t1 = 27.562720
        t2 = 45.262120
        t3 = 72.521485
        t4 = 87.476018
        t5 = 88.637401
    # Bronx
    elif boroIndx == 4:
        t1 = 10.933492
        t2 = 41.213491
        t3 = 46.482021
        t4 = 58.057408
        t5 = 62.525787
    # Staten Island
    elif boroIndx == 5:
        t1 = 64.176278
        t2 = 73.712461
        t3 = 82.825904
        t4 = 94.408742
        t5 = 95.256355
    else:
        print "ERROR probRaceEthncy illegal borough %d"%boroIndx
        return('Medium', 'Middle', 'Female', 'White', 'Non-Hispanic')
        
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

    return(income, age, sex, race, ethncy)

         
#%%########[ probRaceEthncy ]#######
def probRaceEthncy(boroIndx):
#
# Sets 5 thresholds to determine for each borough based on the demographics the proportion
# of the population that falls into 6 categories:
# Non-Hispanic(White, Black, Other), Hispanic(White, Black, Other)
#

    # Manhattan
    if boroIndx == 1:
        t1 = 47.742487
        t2 = 60.763558
        t3 = 74.366567
        t4 = 83.561831
        t5 = 86.056359
    # Brooklyn
    elif boroIndx == 2:
        t1 = 35.676751
        t2 = 67.905354
        t3 = 80.196121
        t4 = 89.087490
        t5 = 91.069430
    # Queens
    elif boroIndx == 3:
        t1 = 27.562720
        t2 = 45.262120
        t3 = 72.521485
        t4 = 87.476018
        t5 = 88.637401
    # Bronx
    elif boroIndx == 4:
        t1 = 10.933492
        t2 = 41.213491
        t3 = 46.482021
        t4 = 58.057408
        t5 = 62.525787
    # Staten Island
    elif boroIndx == 5:
        t1 = 64.176278
        t2 = 73.712461
        t3 = 82.825904
        t4 = 94.408742
        t5 = 95.256355
    else:
        print "ERROR probRaceEthncy illegal borough %d"%boroIndx
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

#%%# Calculate nSymptoms
def calculate_nSymptoms(isFemale, isYoung, isOld, isWhiteHisp, 
                        isBlackNonHisp, isBlackHisp, isOtherNonHisp, 
                        isOtherHisp, isIncomeLow, isIncomeMed,
                        hadStressors, hadTraumas):
    
    logitCBT = -1.536132  +                    \
              (-.2957174  * isFemale)        + \
              ( 1.102366  * isYoung)         + \
              ( 0.6681121 * isOld)           + \
              (-0.0381056 * isWhiteHisp)     + \
              ( 0.4762033 * isBlackNonHisp)  + \
              ( 0.2499723 * isBlackHisp)     + \
              ( 0.095978  * isOtherNonHisp)  + \
              ( 0.8636088 * isOtherHisp)     + \
              ( 0.7940866 * isIncomeLow)     + \
              ( 0.5072571 * isIncomeMed)     + \
              ( 1.050227  * hadStressors)    + \
              ( 0.5165622 * hadTraumas)
                            
    return np.exp(logitCBT)/(1. + np.exp(logitCBT))

#%%# Calculate distribution
# Calculate the probability that agent will accept CBT if offered CBT
def calculate_probAcceptCBT(isMale, isOld, isBlack, isWhite, isOther, isHisp, hadPrior):
    
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

    global nEnrolled, schedList, schedPtr
    global agents, nAgents, square, circle, \
            nAgentsWht, nAgentsBlk, nAgentsOth
    global agencyList, nAgencies
    
    if doingLogging:
        writelog.write('In init_agent(%3d)'%agtId)

    foundSpace = False
    while not foundSpace:
        xLoc = random() * image.aspect + .1*image.aspect
        yLoc = random()
        #writelog.write("agtId: % 3d  xLoc, yLoc = (%4.2f, %4.2f)\n"%(agtId, xLoc, yLoc))
        
        inMask  = image.maskImg[image.imgYSize - yLoc * image.imgYSize,
                                 (xLoc-image.xOff)*image.imgXSize/image.aspect + image.xOff][0]
                            
        boroIndx = int(image.burrIndx[image.imgYSize - yLoc * image.imgYSize,
                                  (xLoc-image.xOff)*image.imgXSize/image.aspect + image.xOff])
        if boroIndx > 0:
            boroIndx -= 1
        #print 'agent %3d loc (%4.2f, %4.2f) boroIndex %3d'%(agtId, xLoc, yLoc, boroIndx)
        #print 'boro[boroindx] = %s'%agencies.boroughsList[boroIndx-1]
        boroName = agencies.boroughsList[boroIndx-1]
        
        
        if doingLogging:
            writelog.write("  agtId: % 3d  xLoc, yLoc = (%4.2f, %4.2f) boro %s boroIndx = %3d\n"%(
                        agtId, xLoc, yLoc, boroName, boroIndx))
        
        # if inMask > .5 and boroIndx in range(1,6):  # If in the masked area check for collision
        if inMask > .9:  # If in the masked area check for collision
            if doingLogging:
                writelog.write('  In boroIndx %3d\n'%boroIndx)
            collision = False
            for agt in range(len(agents)):
                xLoc1 = agents[agt]['xLoc']
                yLoc1 = agents[agt]['yLoc']
                dx = xLoc1 - xLoc
                dy = yLoc1 - yLoc
                dist = np.sqrt(dx**2 + dy**2)
                if dist < minSep:
                    collision = True
                    if doingLogging:
                        writelog.write("  COLLISION !!!\n")
                    break   # Stop going through more agents
            if not collision:
                foundSpace = True
                if doingLogging:
                    writelog.write("  foundSpace!\n")
                    writelog.write("  agtId: % 3d  xLoc, yLoc = (%4.2f, %4.2f) boro %s boroIndx = %3d\n"%(
                                agtId, xLoc, yLoc, boroName, boroIndx))
                # Otherwise keep searching

        
    # Define agent's race and ethnicity
    (income, age, sex, race, ethncy) = probDemographics(boroIndx)
    #print 'boroIndx = %d, income = %s, age = %s, sex = %s, race = %s, ethncy = %s'%(boroIndx, income, age, sex, race, ethncy)
    #(race, ethncy) = probRaceEthncy(boroIndx)
    if race == 'White':
        #raceColor = 'w'
        isWhite = 1.
        isBlack = 0.
        isOther = 0.
        nAgentsWht += 1
    elif race == 'Black':
        #raceColor = 'k'
        isWhite = 0.
        isBlack = 1.
        isOther = 0.
        nAgentsBlk += 1
    elif race == 'Other':
        #raceColor = 'gray'
        isWhite = 0.
        isBlack = 0.
        isOther = 1.
        nAgentsOth += 1
        
    if ethncy == 'Hispanic':
        #ethVis = True
        isHisp = 1.
    else:
        #ethVis = False
        isHisp = 0.
    
    # Define agent's gender
    if sex == 'Female':
        gender = 'Female'
        isFemale = 1.
        isMale = 0.
    else:
        gender = 'Male'
        isMale = 1.
        isFemale = 0.
        
    # Define agent's age
    if age == 'Old':
        isOld = 1.
        isYoung = 0.
    else:
        isOld = 0.
        isYoung = 1.
        
    # Define agent's hadPrior (PTSD)
    if random() > .9:
        hadPrior = 1.
    else:
        hadPrior = 0.

    # Define agent's hadStressors (from Hurricane Sandy)
    if random() > .9:
        hadStressors = 1.
    else:
        hadStressors = 0.

    # Define agent's hadTrauma (from Hurricane Sandy)
    if random() > .9:
        hadTrauma = 1.
    else:
        hadTrauma = 0.

    # Additional coefficients for calculate_nSymptoms()
    isWhiteHisp    = 0.
    isBlackNonHisp = 0.
    isBlackHisp    = 0.
    isOtherNonHisp = 0.
    isOtherHisp    = 0.
    if race == 'White' and ethncy == 'Hispanic':
        isWhiteHisp = 1.
    elif race == 'Black':
        if ethncy == 'NonHisp':
            isBlackNonHisp = 1.
        elif ethncy == 'Hisp':
            isBlackHisp = 1.
    elif race == 'Other':
        if ethncy == 'NonHisp':
            isOtherNonHisp = 1.
        elif ethncy == 'Hisp':
            isOtherHisp = 1.
    if income == 'Low':
        isIncomeLow = 1.
        isIncomeMed = 0.
    elif income == 'Medium':
        isIncomeLow = 0.
        isIncomeMed = 1.
    elif income == 'High':
        isIncomeLow = 0.
        isIncomeMed = 0.
        
    # Define agent's number of PTSD symptoms
    nSymptoms = calculate_nSymptoms(isFemale, isYoung, isOld, isWhiteHisp, 
                        isBlackNonHisp, isBlackHisp, isOtherNonHisp, 
                        isOtherHisp, isIncomeLow, isIncomeMed,
                        hadStressors, hadTrauma)
                        
    # Calculate random value
    randVal = random()
    
    #print '    randVal: %5.2f nSymptoms: %5.2f'%(randVal, nSymptoms)

    # Define agent's "input value" (natural wellness) and input factor
    if useCalcNSymptoms:
        iVal = (1. - nSymptoms) ** boost #<===KLUDGE! 
        if doingLogging:
            writelog.write('  iVal = nSymptoms = %f\n'%iVal)
    else:
        iVal = randVal
        if doingLogging:
            writelog.write('  iVal = random() = %f\n'%iVal)
            
    print '  agent(%3d) iVal: %5.2f nSymptoms: %5.2f'%(agtId, randVal, nSymptoms)

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
            

    # Define agent's probability of accepting CBT if offered CBT
    acceptCBT = calculate_probAcceptCBT(isMale, isOld, isBlack, isWhite, 
                                        isOther, isHisp, hadPrior)


            

    # Set xVal to equilibrium value
    xVal = iVal/(A+iVal)
    # totInput += iVal
    r = (1. - xVal)
    g = xVal

    # Define agent's triple circle
    circle1 = plt.Circle((xLoc, yLoc), circRad1, fc=(r,g,0),
                         ec=cmplxColor)

    if xVal > visThresh:
        circle1.set_visible(False)
    else:
        circle1.set_visible(True)
    axes.ax.add_patch(circle1)
     
    # Define agent's bezier links
    bezPatch = None
    '''
    for agcy in agencies.agenciesList[agencies.boroughsList[boroIndx-1]]:
        (provXCtr, provYCtr) = agcy['loc']
        
         # Define agent's bezier links to that agency
        verts = ((provXCtr, provYCtr), # Bezier lnk from prov. to here
                 ((provXCtr + xLoc)/2., provYCtr),
                 (xLoc, (provYCtr + yLoc)/2.),
                 (xLoc, yLoc))
        bezPath = Path(verts, codes)
        bezPatch = mpatches.PathPatch(bezPath, facecolor='none',
                                  lw=1, ec='#afafaf', visible=True)
        axes.ax.add_patch(bezPatch)
        bezList.append(bezPatch)
    '''
                          
                              
    # Agent ID number below circle
    idText = axes.ax.text(xLoc-.004, yLoc-.021, '%d'%agtId, visible=False)
    
    newAgent =    {'id':agtId,
                   'circ1':circle1,
                   'boroName':boroName,
                   'boroIndx':boroIndx,
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
                   'acceptCBT':acceptCBT,
                   'nSymptoms':nSymptoms,
                   'treating':False,
                   'enrolled':False,
                   'agency':None,
                   'treatNo':0,        # current treatment #
                   'idText':idText}
    return newAgent


#%%########[ init agents ]########
def init_agents():
    
    global agents, nAgents, square, circle, \
            agencyList, nAgencies, \
            nAgentsWht, nAgentsBlk, nAgentsOth, avgInput
    global dataFileName
            
    print '*****[ In init_agents() ]*****'
    
    
    totInput = 0.
    ## for each agent
    for agtId in range(nAgents):
        # 
        if doingLogging:
            writelog.write("agtId = %d\n"%agtId)
        # start = time.time()
        #print '  init_agent(%d) '%agtId
        newAgent = init_agent(agtId)
#        end = time.time()
#        elapsed = end - start
#        (min_, sec) = divmod(elapsed, 60)
#        (hr, min_)  = divmod(min_, 60)
#        print '  elapsed time = %02d:%02d:%02d'%(hr, min_, sec)
        
        
        
        # Append to agents list
        agents.append(newAgent)
        totInput += newAgent['iVal']
        
    avgInput = totInput/float(nAgents)
    
    if axes.checkStepped:
        dataFileName = 'Sp19Stepped.dat'
    else:
        dataFileName = 'Sp19.dat'
        
    if os.path.exists(dataFileName):
        os.remove(dataFileName)


#%%# function printSched
def printSched(agcy):
    schedList = agcy['schedList']
    name   = agcy['name']
    abbrev = agcy['abbrev']
    boro   = agcy['boro']
    writelog.write('========[ '+name+' ('+abbrev+') in '+boro+' ]========\n')
    for indx, entry in enumerate(schedList):
        outStr=StringIO.StringIO()
        if entry[1]:
            stateStr = 'X'
        else:
            stateStr = ' '
        outStr.write(' %3d: %s ['%(entry[0], stateStr))
        
        for tr in range(2,standardSched+2):
            if entry[tr] == None:
                outStr.write('  ~  ')
            else:
                outStr.write('%4.2f '%entry[tr])
        outStr.write(']\n')
        writelog.write(outStr.getvalue())
        outStr.close()

#%%#### Initialize Schedule ####
def initTileArray(agency):
        
    tileArray = agency['tileArray']

    for row in range(agency['maxEnrolled']):
        newRow = []
        newRow.append(axes.ax3.text(1, maxEnrolled - 1 - row + .3, "   ", 
                      size=12, family='Monospace', horizontalalignment='right',
                      name='Courier', bbox=dict(fc='w', ec=None, lw=2)))
        newRow.append(False)
        for col in range(2, standardSched+2):
            newTile = plt.Rectangle((col, agency['maxEnrolled'] - 1 - row), 1, 1, fc='w')
            newRow.append(newTile)
            axes.ax3.add_patch(newTile)
        tileArray.append(newRow)
            
        

#%%#### Update Schedule ####
def updateTileArray(agcy):

    schedList = agcy['schedList']
    tileArray = agcy['tileArray']
    #print '\n\n**** In updateTileArray ****'
    #print '  Borough: %s: agency = %s %s'%(agcy['boro'], agcy['abbrev'],agcy['name'])
    for indx, entry in enumerate(schedList): # Fill existing entries
        #print '  index %1d entry %r'%(indx,entry)
        if entry[1]:
            ec = 'r'
        else:
            ec = None
        tileArray[indx][0].set_bbox(dict(fc='w', ec=ec, lw=2))
        tileArray[indx][0].set_text("%3d"%entry[0])
        tileArray[indx][0].set_color('black')
        for treatment in range(2, standardSched+2):
            if schedList[indx][treatment]:
                xVal = schedList[indx][treatment]
                r = (1. - xVal)
                g = xVal
                tileArray[indx][treatment].set_facecolor((r,g,0))
            else:
                tileArray[indx][treatment].set_facecolor('w')
    indx += 1
    if indx < agcy['maxEnrolled']: # Fill blank entries
        for ix in range(indx, agcy['maxEnrolled']):
            tileArray[ix][0].set_bbox({'fc':'w', 'ec':'w', 'lw':2})
            tileArray[ix][0].set_text('XXX') # set_text('   ') doesn't work (blank text)
            tileArray[ix][0].set_color('w')  # so just print XXX in white
            for treatment in range(2, standardSched+2):
                tileArray[indx][treatment].set_facecolor('w')
                



#%%#### Update single agent ####
def update_agent(agent):

    global nEnrolled, schedList, schedPtr

    # print '  In update_agent agent = %r'%agent
    if doingLogging:
        writelog.write('In update_agent %3d\n'%agent['id'])
        writelog.write(re.sub(r',', '\n', '%r\n'%agent))

    xVal = agent['xVal']
    inputVal = agent['iVal']

    # If service is on, service the agents
    if axes.checkService:
        #square.set_fc('#00ff00')

        ########[ Enrollment Test ]#########
        # If not scheduled for treatment consider enrolling
        if not agent['enrolled']:
  

            # Shuffle agency list every time
            boroName = agent['boroName']
            if doingLogging:
                writelog.write('  Searching through agencies in '+boroName+'\n')
            #shuffledList = sample(agencies.agenciesList[boroName], listLen)

############# Loop through agencies in borough here ######################

            #### For each agency in this borough
            for agcy in agencies.agenciesList[boroName]:
                
                abbrev = agcy['abbrev']
                (agcyXLoc, agcyYLoc) = agcy['loc']
                (xLoc, yLoc) = (agent['xLoc'], agent['yLoc'])


                # Calculate probability of enrollment based on need 
                need = max(( avgInput - xVal),0.) * needFactor
                probEnroll = need * (agcy['maxEnrolled'] - agcy['numEnrolled'])
                if useProbCBTprobEnroll:
                    print 'WARNING: useProbCBTprobEnroll TRUE but not implemented.'
                if doingLogging:
                    writelog.write('  agt %3d need = %4.2f numEnrolled = %4.2f probEnroll["%s"] = %5.2f xVal = %5.2f\n'%(
                                agent['id'], need, agcy['numEnrolled'], abbrev.ljust(8), probEnroll, xVal))
    
                ########[ Need Test ]########
                # If enroll probability exceeds random threshold then enroll
                if probEnroll > random():
                    if doingLogging:
                        writelog.write('  probEnroll > random: Enroll!\n')
                    agent['enrolled'] = True
                    agent['agency'] = agcy
                    agcy['numEnrolled'] += 1                    
                    
                    # Define agent's bezier links to that agency
                    if axes.checkGraphics:
                        verts = ((agcyXLoc, agcyYLoc), # Bezier lnk from prov. to here
                                 ((agcyXLoc + xLoc)/2., agcyYLoc),
                                 (xLoc, (agcyYLoc + yLoc)/2.),
                                 (xLoc, yLoc))
                        bezPath = Path(verts, codes)
                        bezPatch = mpatches.PathPatch(bezPath, facecolor='none',
                                                  lw=1, ec='#afafaf', visible=True)
                        axes.ax.add_patch(bezPatch)
                        agent['bezPatch'] = bezPatch
                        agent['idText'].set_visible(True)
                    inputVal = agent['iVal']
    
                    # Register in schedList[]
                    if doingLogging:
                        writelog.write('About to register in schedList\n')
                        writelog.write('  Enrolling agent %d in agency %s\n'%(agent['id'], agcy['abbrev']))
                    treatList = [None for i in range(standardSched)]
                    treatList[agent['treatNo']] = agent['xVal']
                    treatList.insert(0, agent['isComplex'])
                    treatList.insert(0,agent['id'])
                    agcy['schedList'].append(treatList)
                    #agcy['schedList'] = treatList
                    #schedNo = len(agcy['schedList']) -1
                    
                    # update schedule
                    if axes.checkGraphics and agcy is agencies.selected:                    
                        updateTileArray(agcy)
                    if doingLogging:
                        printSched(agcy)
                        
                    break

 ############# End Loop through agencies in borough ######################

   
        # Otherwise if already enrolled compute input treatment
        else:
            
            # If agent not accepting of CBT then un-enroll
            if agent['acceptCBT'] < random():
                agent['treating'] = False;
                if axes.checkGraphics:
                    agent['bezPatch'].set_lw(1)
                    agent['bezPatch'].set_ec('#afafaf')
                inputVal = agent['iVal']

                if doingLogging: writelog.write('  agent %d acceptCBT < random() treatment %d OFF\n'%
                                    (agent['id'], agent['treatNo']))
                                    
            # Otherwise if accepting
            elif random() > .25: # Randomize every other time to break sync

                # If agent not being treated do next treatment
                if agent['treating'] == False:
                    if doingLogging:
                        writelog.write('  agent %d treatment %d ON\n'%(agent['id'], 
                                                                          agent['treatNo']))
                    agent['treating'] = True
                    (provXCtr, provYCtr) = agent['agency']['loc']
                    if axes.checkGraphics:
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
                        
                    ########[ COMPLETION TEST ]#######
                    # If treatment done then un-enroll
                    if agent['treatNo'] >= nTreatLeft:
                        
                        if doingLogging:
                            if axes.checkStepped and not agent['isComplex']:
                                writelog.write('  treatNo = %d steppedSched = %d\n'%
                                             (agent['treatNo'], steppedSched))
                            else:
                                writelog.write('  treatNo = %d standardSched = %d\n'%
                                             (agent['treatNo'], standardSched))
                            writelog.write('Un-enroll agent %d treatment done\n'% 
                                                            agent['id'])
                                                            
                        agent['enrolled'] = False
                        agent['treatNo'] = 0
                        agent['agency']['numEnrolled'] -= 1
                        if axes.checkGraphics:
                            agent['bezPatch'].remove()
                            agent['idText'].set_visible(False)
                        for entry in agent['agency']['schedList']:
                            if entry[0] == int(agent['id']):
                                agent['agency']['schedList'].remove(entry)
                                #break

                    # Else if already treating turn treatment off, pipeline gray
                    
                    else:
                        for indx, sched in enumerate(agent['agency']['schedList']):
                            if sched[0] == int(agent['id']):
                                agent['agency']['schedList'][indx][agent['treatNo']+1] = agent['xVal']
                                #break
                        if doingLogging: writelog.write('  agent %d treatment %d ON\n'%
                                           (agent['id'], agent['treatNo']+1))
                    
 
                # Otherwise if patient being treated turn it off
                else:
                    agent['treating'] = False;
                    if axes.checkGraphics:
                        agent['bezPatch'].set_lw(1)
                        agent['bezPatch'].set_ec('#afafaf')
                    inputVal = agent['iVal']

                    if doingLogging: writelog.write('  agent %d treatment %d OFF\n'%
                                        (agent['id'], agent['treatNo']))

            # Update schedule
            #schedNo = len(agcy['schedList']) -1
            #print '#### schedNo = %d'%schedNo
            if agent['agency']: 
                if axes.checkGraphics and agent['agency'] is agencies.selected:
                    updateTileArray(agent['agency'])
                if doingLogging:
                    printSched(agent['agency'])
    
               # schedList = [x for x in schedList if x[0] != agent['id']]
    


    # Else if service is off, shut off treatment
    else:
        if agent['bezPatch']:
            if axes.checkGraphics:
                agent['bezPatch'].set_visible(False)
        inputVal = agent['iVal'] * agent['iFact']


    # Shunting equation
    xVal += -A * xVal + (1 - xVal) * inputVal
    if xVal < 0.:
        xVal = 0.
    elif xVal > 1.:
        xVal = 1.
    agent['xVal'] = xVal
    if axes.checkGraphics:
        if xVal > visThresh:
            agent['circ1'].set_visible(False)
        else:
            agent['circ1'].set_visible(True)
    r = (1. - xVal)
    g = xVal
    if axes.checkGraphics:
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
    global nPtsd
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
        '''
        if random() > .2:
            nPtsd += 1
        '''
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
    if num == 0:
        axes.ax2yMax = 1.2*float(nPtsd)        
    '''
    avgPtsdWht = sumPtsdWht / float(nAgentsWht)
    avgPtsdBlk = sumPtsdBlk / float(nAgentsBlk)
    avgPtsdOth = sumPtsdOth / float(nAgentsOth)
    '''
    x = avgPtsd
    '''
    xWht = avgPtsdWht
    xBlk = avgPtsdBlk
    xOth = avgPtsdOth
    '''
    lastT = t
    t += dt
    '''
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
    '''
    fp = open(dataFileName, 'a')
    fp.write('%4.2f '%float(nPtsd)) # Write data to file
    fp.close()
    
    
    dArrayNptsd.appendleft(nPtsd)
    if len(dArrayNptsd) > plotWidth / dt:
        dArrayNptsd.pop()
        
    tArray.appendleft(t)
    if len(tArray) > plotWidth / dt:
        tArray.pop()

    '''
    axes.line.set_data(tArray, dArray)
    axes.lineWht.set_data(tArray, dArrayWht)
    axes.lineBlk.set_data(tArray, dArrayBlk)
    axes.lineOth.set_data(tArray, dArrayOth)
    '''

    if nPtsd > axes.ax2yMax:
        axes.ax2yMax = 1.2*float(nPtsd)        
    axes.lineNptsd.set_data(tArray, dArrayNptsd)
    axes.ax2.axis((t - plotWidth, t, axes.ax2yMin, axes.ax2yMax))
    
    # Create new PTSD cases after t > 0 
    if t >= 0:
        probNew = 10. * np.exp(-(t/10.))
        for num in range(int(probNew)):
            randId = randint(0,nAgents-1)
            agents[randId]['iVal'] = random()*visThresh
            agents[randId]['circ1'].set_visible(True)
            agents[randId]['isComplex'] = (agents[randId]['iVal'] < iThresh)
            
    
    

