# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 13:14:39 2015

@author: slehar
"""

import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

# onclick event handler
def onclick(event):
    global burrIndx
    x = int(event.x)
    y = int(event.y)
    print 'x=%d, y=%d, pixel=%d'%(x, y, burrIndx[x,y])


# Open figure and set axes 1 for drawing Artists
plt.close('all')


fig = plt.figure()
fig.canvas.set_window_title('MapView')
ax = fig.add_axes([.1, .1, .8, .8])
ax.set_xlim([0, 871])
ax.set_ylim([0, 1052])

burrImg = Image.open('serviceprov15/BurroughsIndxNoBg.png')
(imgXSize, imgYSize) = burrImg.size

burrIndx = np.array(burrImg.convert('P'))

# cid = fig.canvas.mpl_connect('button_press_event', onclick)
cid = fig.canvas.mpl_connect('motion_notify_event', onclick)

'''
for y in range(1052):
    for x in range(871):
        if burrIndx[y,x] > 0:
            print "(%3d, %3d) = %d"%(y,x,burrIndx[y,x])
'''
            
ax.imshow(burrImg, origin='lower')

# Show plot
plt.show()
figmgr = plt.get_current_fig_manager()
figmgr.canvas.manager.window.raise_()
geom = figmgr.window.geometry()
xLoc, yLoc, dxWidth, dyHeight = geom.getRect()
figmgr.window.setGeometry(10, 10, dxWidth, dyHeight)
