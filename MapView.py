# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 13:14:39 2015

@author: slehar
"""

import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

# onclick event handler
def onmotion(event):
    global burrIndx
    screenX = int(event.x)
    screenY = int(event.y)
    inv = ax.transData.inverted()
    (imgX, imgY) = inv.transform((screenX, screenY))
    print '(%3d, %3d) %3d'%(imgX, imgY, burrIndx[int(imgY), int(imgX)])


# Open figure and set axes 1 for drawing Artists
plt.close('all')


fig = plt.figure()
fig.canvas.set_window_title('MapView')
ax = fig.add_axes([.1, .1, .8, .8])
ax.set_xlim([0, 871])
ax.set_ylim([0, 1052])

burrImg = Image.open('serviceprov16/BurroughsIndxNoBg.png')
# (imgXSize, imgYSize) = burrImg.size
(imgXSize, imgYSize) = (burrImg.width, burrImg.height)

burrIndx = np.array(burrImg.convert('P'))

# cid = fig.canvas.mpl_connect('button_press_event', onclick)
cid = fig.canvas.mpl_connect('motion_notify_event', onmotion)

'''
for y in range(1052):
    for x in range(871):
        if burrIndx[y,x] > 0:
            print "(%3d, %3d) = %d"%(y,x,burrIndx[y,x])
'''

print '00 (%3d, %3d) = %r'%(230,360,int(burrImg.getpixel((230,360))))
print 'MH (%3d, %3d) = %r'%(438,446,int(burrImg.getpixel((438,446))))
print 'BK (%3d, %3d) = %r'%(468,705,int(burrImg.getpixel((468,705))))
print 'QN (%3d, %3d) = %r'%(667,567,int(burrImg.getpixel((667,567))))
print 'BX (%3d, %3d) = %r'%(590,306,int(burrImg.getpixel((590,306))))
print 'SI (%3d, %3d) = %r'%(180,824,int(burrImg.getpixel((180,824))))
print
print '00 [%3d, %3d] = %r'%(230,360,int(burrImg.getpixel((360,230))))
print 'MH [%3d, %3d] = %r'%(438,446,int(burrImg.getpixel((446,438))))
print 'BK [%3d, %3d] = %r'%(468,705,int(burrImg.getpixel((705,468))))
print 'QN [%3d, %3d] = %r'%(667,567,int(burrImg.getpixel((567,667))))
print 'BX [%3d, %3d] = %r'%(590,306,int(burrImg.getpixel((306,590))))
print 'SI [%3d, %3d] = %r'%(180,824,int(burrImg.getpixel((824,180))))


         
ax.imshow(burrImg, origin='lower')

# Show plot
plt.show()
figmgr = plt.get_current_fig_manager()
figmgr.canvas.manager.window.raise_()
geom = figmgr.window.geometry()
xLoc, yLoc, dxWidth, dyHeight = geom.getRect()
figmgr.window.setGeometry(10, 10, dxWidth, dyHeight)
