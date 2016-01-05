# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 11:03:20 2015

@author: slehar
"""

import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons
import numpy as np
# import math
from collections import deque
import writelog

# Global Variables
x = 0.001
t = 0.
lastX = 0.
lastT = 0.
dt = 10
dArray = deque([0.])
tArray = deque([0.])
plotWidth = 500
isMale = 0
isOld = 1
isBlack = 0.
race = 'white'
ethn = 'hispanic'
# income = 'lowrange'
hadPrior = 0
logitCBT = 0
probCBT = 0

writelog.init('PTSD_Logistic.log')
writelog.write('sex \t age \t race \t ethn \t\t nPrior \t logitCBT \t probCBT \n')
writelog.write('=== \t === \t ==== \t ==== \t\t ====== \t ======   \t ======= \n\n')

plt.close('all')
fig = plt.figure(figsize=(12,6))
fig.canvas.set_window_title('PTSD_LogisticCombo.py')

# Create axes boxes in a linspace xorg line
xorg = np.linspace(.05,.9,5)
axSex    = plt.axes([xorg[0],.6,.08,.2]); axSex.set_title('Sex')
axAge    = plt.axes([xorg[1],.6,.08,.2]); axAge.set_title('Age')
axRace   = plt.axes([xorg[2],.6,.08,.2]); axRace.set_title('Race')
axEthn   = plt.axes([xorg[3],.6,.08,.2]); axEthn.set_title('Ethn')
axPrior  = plt.axes([xorg[4],.6,.08,.2]); axPrior.set_title('Prior CBT')

# Create axes for text output
axText = plt.axes([.32, .4, .4, .1]); axText.set_title('PTSD logitCBT')

# Create axes for time trace
axTime = plt.axes([.32, .1, .4, .2]); axTime.set_title('Trace')
axTime.set_ylim(0,1)
axTime.set_xlim(0, plotWidth)
axTime.grid(True)

# Set up plot line in axes 2
line, = axTime.plot(t, x, color='blue', linewidth=1, 
                 linestyle='-', alpha=1.0)  
line2, = axTime.plot(t, x, color='red', linewidth=1, 
                 linestyle='-', alpha=1.0)  


# Remove ticks and labels from all the axes
axSex.set_xticklabels([])
axSex.set_yticklabels([])
axSex.set_xticks([])
axSex.set_yticks([])

axAge.set_xticklabels([])
axAge.set_yticklabels([])
axAge.set_xticks([])
axAge.set_yticks([])

axRace.set_xticklabels([])
axRace.set_yticklabels([])
axRace.set_xticks([])
axRace.set_yticks([])

axEthn.set_xticklabels([])
axEthn.set_yticklabels([])
axEthn.set_xticks([])
axEthn.set_yticks([])

#axIncome.set_xticklabels([])
#axIncome.set_yticklabels([])
#axIncome.set_xticks([])
#axIncome.set_yticks([])

#axStress.set_xticklabels([])
#axStress.set_yticklabels([])
#axStress.set_xticks([])
#axStress.set_yticks([])

#axTrauma.set_xticklabels([])
#axTrauma.set_yticklabels([])
#axTrauma.set_xticks([])
#axTrauma.set_yticks([])

axPrior.set_xticklabels([])
axPrior.set_yticklabels([])
axPrior.set_xticks([])
axPrior.set_yticks([])

axText.set_xticklabels([])
axText.set_yticklabels([])
axText.set_xticks([])
axText.set_yticks([])


# Calculate distribution
def calculate_distribution():
    
    global isMale, isOld, isBlack, isHisp, isOther, hadPrior, \
           logitCBT, probCBT, x, t, lastX, lastT, dArray, tArray

    # print 'In calculate_distribution()'
    

    '''               
    print '\n====[ calculate distribution ]===='
    print '  isMale = %d'%isMale
    print '  isOld  = %d'%isOld
    print '  isOld    = %d'%isOld
    print '  isWhiteHispanic = %d'%isWhiteHispanic
    print '  isBlackHispanic = %d'%isBlackHispanic
    print '  isOtherHispanic = %d'%isOtherHispanic
    print '  isWhiteNonHisp  = %d'%isWhiteNonHisp
    print '  isBlackNonHisp  = %d'%isBlackNonHisp
    print '  isOtherNonHisp  = %d'%isOtherNonHisp
    print '  hasIncome1 = %d'%hasIncome1
    print '  hasIncome2 = %d'%hasIncome2
    print '  hasIncome3 = %d'%hasIncome3
    print '  hadStressors  = %d'%hadStressors
    print '  nSandyTraumas = %d'%nSandyTraumas
    '''

    
    logitCBT = -1.60 +                \
              (-0.2008   * isMale)  + \
              (-0.5828   * isBlack) + \
              (-1.073    * isHisp)  + \
              (-0.35     * isOther) + \
              (0.2449    * isOld)   + \
              (1.8377    * hadPrior)
              
    probCBT = np.exp(logitCBT)/(1. + np.exp(logitCBT))

              
    print 'logitCBT      = %f'%logitCBT
    print 'probCBT       = %f'%probCBT
    axText.clear()
    axText.set_title('PTSD Symptom Distribution')
    axText.set_xticklabels([])
    axText.set_yticklabels([])
    axText.set_xticks([])
    axText.set_yticks([])
    axText.text(.3, .6, 'logitCBT = %f'%logitCBT, size=14)    
    axText.text(.3, .2, 'probCBT  = %f'%probCBT,  size=14)    
    
    x = np.exp(logitCBT)/(1. + np.exp(logitCBT))
    lastT = t
    t += dt
    dArray.appendleft(x)
    if len(dArray) >= plotWidth:
        dArray.pop()
    tArray.appendleft(t)
    if len(tArray) >= plotWidth:
        tArray.pop()
    line.set_data(tArray,dArray)
    axTime.axis((t - plotWidth, t, 0., 1.))

# Radio buttons in each axes
radioSex    = RadioButtons(axSex,    ('Male', 'Female'))
radioAge    = RadioButtons(axAge,    ('< 45', '45+'))
radioRace   = RadioButtons(axRace,   ('White', 'Black', 'Other'))
radioEthn   = RadioButtons(axEthn,   ('Hispanic', 'Non-Hisp'))
#radioIncome = RadioButtons(axIncome, ('< 40K', '40-80K ', '80-150k'))
#radioStress = RadioButtons(axStress, ('no stress', 'stress'))
#radioTrauma = RadioButtons(axTrauma, ('0', '1', '2'))
radioPrior = RadioButtons(axPrior, ('Yes', 'No'))

def sexfunc(label):
    global isMale
    
    sexdict = {'Male': 1, 'Female': 0}
    isMale = sexdict[label]
    calculate_distribution()
radioSex.on_clicked(sexfunc)

def agefunc(label):
    global isOld
    
    agedict = {'< 45': 0, '45+': 1}
    isOld = agedict[label]
    print 'isOld = %r'%isOld
    calculate_distribution()
radioAge.on_clicked(agefunc)

def racefunc(label):
    global isBlack, isOther
    
    isBlack = isHisp = isOther = 0.
    racedict = {'White':'white', 'Black':'black', 'Other':'other'}
    race = racedict[label]
    if race == 'black':
        isBlack = 1.
    elif race == 'other':
        isOther = 1.
    print 'race = %r'%race
    calculate_distribution()
radioRace.on_clicked(racefunc)

def ethnfunc(label):
    global isHisp
    
    isHisp = 0.
    ethndict = {'Hispanic':'hispanic', 'Non-Hisp':'non-hisp'}
    ethn = ethndict[label]
    if ethn == 'hispanic':
        isHisp = 1.
    print 'Ethnicity = %r'%ethn
    calculate_distribution()
radioEthn.on_clicked(ethnfunc)


def priorfunc(label):
    global hadPrior
    
    traumadict = {'Yes':1., 'No':0.,}
    hadPrior = traumadict[label]
    print 'hadPrior = %r'%hadPrior
    calculate_distribution()
radioPrior.on_clicked(priorfunc)

'''
for sexKey in ('Male', 'Female'):
    for ageKey in ('< 45', '45+'):
        for raceKey in ('White', 'Black', 'Other'):
            for ethnKey in ('Hispanic', 'Non-Hisp'):
                for hadPriorKey in ('Yes', 'No'):
                    sexfunc(sexKey)
                    agefunc(ageKey)
                    racefunc(raceKey)
                    ethnfunc(ethnKey)
                    priorfunc(hadPriorKey)
                    print('sex = %s  '
                          'age = %s  '
                          'race = %s  '
                          'ethn = %s  '
                          'nPriors = %r\n'%(
                          sexKey, ageKey, raceKey, ethnKey, hadPriorKey))
                    calculate_distribution()
                    writelog.write(
                    '%s \t %s \t %s \t %s \t %r '%(
        sexKey, ageKey, raceKey, ethnKey, hadPriorKey))
                    writelog.write('\t\t%5.2f \t'%logitCBT)
                    writelog.write('\t\t%5.2f \n\n'%probCBT)
'''


calculate_distribution()


plt.show()
figmgr = plt.get_current_fig_manager()
figmgr.canvas.manager.window.raise_()
geom = figmgr.window.geometry()
xLoc, yLoc, dxWidth, dyHeight = geom.getRect()
figmgr.window.setGeometry(10, 10, dxWidth, dyHeight)

