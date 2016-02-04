# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 11:18:40 2016

@author: slehar
"""

import matplotlib.pyplot as plt
import axes
import csv
import re


# Global Variables
agenciesList = None
nAgencies = 0
squareSize = .02
hafSquareSize = .01
squareSep = .03

# Borough List
boroughsList = ('Bronx', 'Brooklyn', 'Manhattan', 'StatenIsl', 'Queens')





#%%########[ init agencies ]########
def init_agencies():
    
    global agenciesList, nAgencies
    
    fp = open('agenciesDat.txt', 'rb')
    csvReader = csv.reader(fp, delimiter='\t')
    
    print 'agenciesList = %r'%agenciesList    
    
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
        nAgencies += 1
                                        
    agenciesList = {'Bronx':bronxList,
                    'Brooklyn':brooklynList, 
                    'Manhattan':manhattanList,
                    'StatenIsl':statenList,
                    'Queens':queensList}
                    
    boroOrgs = {    'Bronx':(.78, .9),
                 'Brooklyn':(.88,  .82),
                'Manhattan':(.4, .9,),
                'StatenIsl':(.11, .48),
                   'Queens':(.3, .75)}
    
    for boro in boroughsList:
        nAgcsInBoro = len(agenciesList[boro])
        dx, dy = 0., 0.
        print 'Boro %s Org (%3.2f, %3.2f)'%(boro, boroOrgs[boro][0], boroOrgs[boro][1])
        for agcy in range(nAgcsInBoro):
            (x, y) = (boroOrgs[boro][0]+dx, boroOrgs[boro][1]+dy)
            print '  Agc %2d loc (%3.2f, %3.2f)'%(agcy, x, y)
            agenciesList[boro][agcy]['loc'] = (x,y)
            square = plt.Rectangle((x-hafSquareSize,y-hafSquareSize),
                                   squareSize, squareSize,
                                   fc=(0,1,0), ec='k')
            agenciesList[boro][agcy]['square'] = square
            axes.ax.add_patch(square)
            dy -= squareSep
                    
    fp.close()
    



