# -*- coding: utf-8 -*-
"""
plotDat.py
Created on Tue Mar  1 12:55:48 2016

@author: slehar
"""

import matplotlib.pyplot as plt
import numpy as np
import csv

winXSizeInches = 12.
winYSizeInches = 5.
axX = .1
axY = .1
axXSize = .8
axYSize = .8

#### Original series ####

#filename1 = 'Sp19500.dat'
#filename2 = 'Sp19500Stepped.dat'

#filename1 = 'Sp191k.dat'
#filename2 = 'Sp191kStepped.dat'

#filename1 = 'Sp1910k.dat'
#filename2 = 'Sp1910kStepped.dat'

filename1 = 'Sp1920k.dat'
filename2 = 'Sp1920kStepped.dat'

#### A series ####

#filename1 = 'Sp19500A.dat'
#filename2 = 'Sp19500AStepped.dat'

#filename1 = 'Sp191kA.dat'
#filename2 = 'Sp191kAStepped.dat'

#filename1 = 'Sp1910kA.dat'
#filename2 = 'Sp1910kAStepped.dat'

#filename1 = 'Sp1920kA.dat'
#filename2 = 'Sp1920kAStepped.dat'

#### B series ####

#filename1 = 'Sp19500B.dat'
#filename2 = 'Sp19500BStepped.dat'

#### Demo Series ####

#filename1 = 'Sp19Demo.dat'
#filename2 = 'Sp19SteppedDemo.dat'

#### Default Files ####

#filename1 = 'Sp19.dat'
#filename2 = 'Sp19Stepped.dat'

plt.close('all')
fig = plt.figure(figsize=(winXSizeInches, winYSizeInches))
fig.canvas.set_window_title('plotDat')
ax = fig.add_axes([axX, axY, axXSize, axYSize])


fdat1 = []
fp1 = open(filename1, 'rb')
csvDat = csv.reader(fp1, delimiter=' ')
fdat1 = []
for dat1 in csvDat:
    #print 'dat %s'%dat1
    for item in dat1:
        if item != '':
            fdat1.append(float(item))
fp1.close()
fp2 = open(filename2, 'rb')
csvDat = csv.reader(fp2, delimiter=' ')
fdat2 = []
for dat2 in csvDat:
    for item in dat2:
        if item != '':
            fdat2.append(float(item))
fp2.close()

maxmaxX = max(len(fdat1), len(fdat2))
maxmaxY = max(np.max(fdat1), np.max(fdat2))
textX = maxmaxX * .6
textY1 = maxmaxY * 0.55
textY2 = maxmaxY * 0.35
ax.text(textX, textY1, filename1, color='r', fontsize=24)
ax.text(textX, textY2, filename2, color='b', fontsize=24)



plt.plot(fdat1, color='r', label='NotStepped')
plt.hold
plt.plot(fdat2, color='b', label='Stepped')
plt.legend()
plt.title('PTSD Recovery After Hurricane Sandy')
plt.xlabel('Days since Hurricane Sandy')
plt.ylabel('Number pf PTSD cases')
plt.show()


figmgr=plt.get_current_fig_manager()
figmgr.canvas.manager.window.raise_()
geom=figmgr.window.geometry()
xOrg,yOrg,xSize,ySize = geom.getRect()
figmgr.window.setGeometry(10,10,xSize,ySize)


