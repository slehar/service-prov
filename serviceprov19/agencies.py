# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 11:18:40 2016

@author: slehar
"""

import matplotlib.pyplot as plt
import axes
import csv
import re



nAgencies = 0

# Borough List
boroughsList = ('Bronx', 'Brooklyn', 'Manhattan', 'StatenIsl', 'Queens')

fp = open('agenciesDat.txt', 'rb')
csvReader = csv.reader(fp, delimiter='\t')

bronxList     = []
brooklynList  = []
manhattanList = []
statenList    = []
queensList    = []

# Read in the data
for row in csvReader:
    # print row
    name   = row[0]
    abbrev = row[1]
    boro   = row[2]    
    matchObj = re.match('\(([0-9]+),\s([0-9]+)\)', row[3])
    if matchObj is not None:
        (xstr, ystr) = matchObj.group(1,2)
        loc    = (int(xstr), int(ystr))
    maxenrolled = int(row[4])
    entry = {'name':name, 'abbrev':abbrev, 'boro':boro, 'loc':loc, 'maxenrolled':maxenrolled}
    if boro == 'Bronx':
        bronxList.append(entry)
    elif boro == 'Brooklyn':
        brooklynList.append(entry)
    elif boro == 'Manhattan':
        manhattanList.append(entry)
    elif boro == 'StatenIsl':
        statenList.append(entry)
    elif boro == 'Queens':
        queensList.append(entry)
    print '%s %s %s (%d, %d) %d'%(name.ljust(60), abbrev.ljust(6),
                                    boro.ljust(10), loc[0], loc[1], maxenrolled)
        
    
fp.close()





#%%########[ init agencies ]########
def init_agencies():
    
    global nAgencies
    for borough in boroughsList:
        print '====[ %s ]===='%borough
        print repr(borough)
        nAgencies += len(agenciesList[borough])
        print 'nAgencies = %d'%len(agenciesList[borough])


    '''
    agencyList = []
     
    (agcId, agcName, xLoc, yLoc) = (0, 'Agc0', 0.48, 0.93)
    square = plt.rectangle(xLoc, yLoc, axes.provSize, axes.provSize, fc=(0,1,0), ec='k')
    circle = plt.Circle(  (xLoc, yLoc), radius=rSigma, ec='r', fc='none', linestyle='dashed', visible=axes.checkDist)                   
    agencyList.append(dict(('agcId',     agcId),
                           ('agcName', agcName),
                           ('xLoc',       xLoc),
                           ('yLoc',       yLoc),
                           ('square',   square),
                           ('circle',   circle)))
    axes.ax.add_patch(square)
    axes.ax.add_patch(circle)
    return agencyList
    '''



