# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 11:03:20 2015

@author: slehar
"""

import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons
import numpy as np
import math
from collections import deque

# Global Variables
x = 0.001
t = 0.
lastX = 0.
lastT = 0.
dt = 5
dArray = deque([0.])
tArray = deque([0.])
plotWidth = 500

plt.close('all')
fig = plt.figure(figsize=(12,6))
fig.canvas.set_window_title('PTSD_Distribution.py')

# Create axes boxes in a linspace xorg line
xorg = np.linspace(.05,.9,7)
axSex    = plt.axes([xorg[0],.6,.08,.2]); axSex.set_title('Sex')
axAge    = plt.axes([xorg[1],.6,.08,.2]); axAge.set_title('Age')
axRace   = plt.axes([xorg[2],.6,.08,.2]); axRace.set_title('Race')
axEthn   = plt.axes([xorg[3],.6,.08,.2]); axEthn.set_title('Ethn')
axIncome = plt.axes([xorg[4],.6,.08,.2]); axIncome.set_title('Income')
axStress = plt.axes([xorg[5],.6,.08,.2]); axStress.set_title('Stress')
axTrauma = plt.axes([xorg[6],.6,.08,.2]); axTrauma.set_title('Trauma')

# Create axes for text output
axText = plt.axes([.32, .4, .4, .1]); axText.set_title('PTSD Symptom Distribution')

# Create axes for time trace
axTime = plt.axes([.32, .1, .4, .2]); axTime.set_title('Trace')
axTime.set_ylim(0,20)
axTime.set_xlim(0, plotWidth)
axTime.grid(True)

# Set up plot line in axes 2
line, = axTime.plot(t, x, color='blue', linewidth=1, 
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

axIncome.set_xticklabels([])
axIncome.set_yticklabels([])
axIncome.set_xticks([])
axIncome.set_yticks([])

axStress.set_xticklabels([])
axStress.set_yticklabels([])
axStress.set_xticks([])
axStress.set_yticks([])

axTrauma.set_xticklabels([])
axTrauma.set_yticklabels([])
axTrauma.set_xticks([])
axTrauma.set_yticks([])

axText.set_xticklabels([])
axText.set_yticklabels([])
axText.set_xticks([])
axText.set_yticks([])




# Global variables
isFemale = 0
isYoung = 1
race = 'white'
ethn = 'hispanic'
income = 'lowrange'
hadStressors = 0
nSandyTraumas = 0
PTSD_sx = 0
dArray = deque([0.])
tArray = deque([0.])


# Calculate distribution
def calculate_distribution():
    
    global isFemale, isYoung, race, ethn, income, hadStressors, nSandyTraumas,\
           PTSD_sx, x, t, lastX, lastT, dArray, tArray

    # print 'In calculate_distribution()'
    isWhiteHispanic = isBlackHispanic = isOtherHispanic = 0
    isWhiteNonHisp  = isBlackNonHisp  = isOtherNonHisp  = 0
    hasIncome1 = hasIncome2 = hasIncome3 = 0
    
    if isYoung == 0:
        isOld = 1
    elif isYoung == 1:
        isOld = 0
    
    if race == 'white':
        if ethn == 'hispanic':
            isWhiteHispanic = 1
        elif ethn == 'non-hisp':
            isWhiteNonHisp = 1
    elif race == 'black':
        if ethn == 'hispanic':
            isBlackHispanic = 1
        elif ethn == 'non-hisp':
            isBlackNonHisp  = 1
    elif race == 'other':
        if ethn == 'hispanic':
            isOtherHispanic = 1
        elif ethn == 'non-hisp':
            isOtherNonHisp  = 1
    
    if income == 'lowrange':
        hasIncome1 = 1
    elif income == 'midrange':
        hasIncome2 = 1
    elif income == 'highrange':
        hasIncome3 = 1
                
    print '\n====[ calculate distribution ]===='
    print '  isFemale = %d'%isFemale
    print '  isYoung  = %d'%isYoung
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
    PTSD_sx = -2.0308 +                    \
              (-0.1583 * isFemale) +       \
              (1.0157 * isYoung) +         \
              (0.6613 * isOld) +           \
              (0.0719 * isWhiteHispanic) + \
              (0.5761 * isBlackNonHisp) +  \
              (0.3153 * isBlackHispanic) + \
              (0.1706 * isOtherNonHisp) +  \
              (0.0730 * isOtherHispanic) + \
              (1.2863 * hasIncome1) +      \
              (1.3235 * hasIncome2) +      \
              (0.6926 * hasIncome3) +      \
              (0.9615 * hadStressors) +    \
              (0.3389 * nSandyTraumas)
    '''
              
    PTSD_sx = .1312 +                    \
              (.8536 * isFemale) +       \
              (2.7613 * isYoung) +         \
              (1.9373 * isOld) +           \
              (1.0746 * isWhiteHispanic) + \
              (1.7791 * isBlackNonHisp) +  \
              (1.3707 * isBlackHispanic) + \
              (0.1860 * isOtherNonHisp) +  \
              (0.0757 * isOtherHispanic) + \
              (3.6194 * hasIncome1) +      \
              (3.7564 * hasIncome2) +      \
              (1.9989 * hasIncome3) +      \
              (2.6156 * hadStressors) +    \
              (1.4035 * nSandyTraumas)
              
    print 'PTSD_sx      = %f'%PTSD_sx
    axText.clear()
    axText.set_title('PTSD Symptom Distribution')
    axText.set_xticklabels([])
    axText.set_yticklabels([])
    axText.set_xticks([])
    axText.set_yticks([])
    axText.text(.3, .4, 'PTSD_sx = %f'%PTSD_sx, size=14)    
    
    x = PTSD_sx
    lastT = t
    t += dt
    dArray.appendleft(x)
    if len(dArray) >= plotWidth:
        dArray.pop()
    tArray.appendleft(t)
    if len(tArray) >= plotWidth:
        tArray.pop()
    line.set_data(tArray,dArray)
    axTime.axis((t - plotWidth, t, 0., 20))

# Radio buttons in each axes
radioSex    = RadioButtons(axSex,    ('Male', 'Female'))
radioAge    = RadioButtons(axAge,    ('35-65', '65+'))
radioRace   = RadioButtons(axRace,   ('White', 'Black', 'Other'))
radioEthn   = RadioButtons(axEthn,   ('Hispanic', 'Non-Hisp'))
radioIncome = RadioButtons(axIncome, ('< 40K', '40-80K', '80-150k'))
radioStress = RadioButtons(axStress, ('no stress', 'stress'))
radioTrauma = RadioButtons(axTrauma, ('0', '1', '2', '3'))

def sexfunc(label):
    global isFemale
    
    sexdict = {'Male': 0, 'Female': 1}
    isFemale = sexdict[label]
    calculate_distribution()
radioSex.on_clicked(sexfunc)

def agefunc(label):
    global isYoung
    
    agedict = {'35-65': 1, '65+': 0}
    isYoung = agedict[label]
    # print 'isYoung = %r'%isYoung
    calculate_distribution()
radioAge.on_clicked(agefunc)

def racefunc(label):
    global race
    
    racedict = {'White':'white', 'Black':'black', 'Other':'other'}
    race = racedict[label]
    # print 'race = %r'%race
    calculate_distribution()
radioRace.on_clicked(racefunc)

def ethnfunc(label):
    global ethn
    
    ethndict = {'Hispanic':'hispanic', 'Non-Hisp':'non-hisp'}
    ethn = ethndict[label]
    # print 'Ethnicity = %r'%ethn
    calculate_distribution()
radioEthn.on_clicked(ethnfunc)

def incomefunc(label):
    global income
    
    incomedict = {'< 40K':'lowrange', '40-80K':'midrange', '80-150k':'highrange'}
    income = incomedict[label]
    # print 'income = %r'%income
    calculate_distribution()
radioIncome.on_clicked(incomefunc)

def stressfunc(label):
    global hadStressors
    
    stressdict = {'no stress':0, 'stress':1}
    hadStressors = stressdict[label]
    # print 'hadStressors = %r'%hadStressors
    calculate_distribution()
radioStress.on_clicked(stressfunc)

def traumafunc(label):
    global nSandyTraumas
    
    traumadict = {'0':0, '1':1, '2':2, '3':3}
    nSandyTraumas = traumadict[label]
    # print 'nSandyTraumas = %r'%nSandyTraumas
    calculate_distribution()
radioTrauma.on_clicked(traumafunc)

calculate_distribution()


plt.show()
figmgr = plt.get_current_fig_manager()
figmgr.canvas.manager.window.raise_()
geom = figmgr.window.geometry()
xLoc, yLoc, dxWidth, dyHeight = geom.getRect()
figmgr.window.setGeometry(10, 10, dxWidth, dyHeight)

