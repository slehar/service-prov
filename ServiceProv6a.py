# -*- coding: utf-8 -*-
# ServiceProv6a.py
#
# Model of service provision
# Kludge demo for Sarah Lowe

import numpy as np
# from matplotlib.patches import Circle, Rectangle
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
from matplotlib.widgets import CheckButtons, Slider
from collections import deque
import time
from matplotlib.path import Path
"""
Created on Wed Jun 24 11:09:21 2015

@author: slehar
"""

# Parameters
provXCtr = 3.
provYCtr = .7
provSize = .2
provXOrg = provXCtr - (provSize/2.)
provYOrg = provYCtr - (provSize/2.)
delay = .1
agents = []


# Open figure and set axes 1 for drawing Artists
plt.close('all')
fig = plt.figure(figsize=(15,5))
fig.canvas.set_window_title('ServiceProv6')
#ax = fig.add_axes([.2, .6, .5, .3])
ax = fig.add_axes([.1, .5, .8, .4])
ax.set_xlim([0, 6])
ax.set_ylim([0, 1])
ax.set_xticklabels([])
ax.set_yticklabels([])
ax.set_xticks([])
ax.set_yticks([])

"""
fluid = plt.Rectangle((1, 1), 2, 2*flevel, fc=(0, 1, 0))
ax.add_patch(fluid)
circle = plt.Circle((6, 2), 1, fc='r', ec='k')
ax.add_patch(circle)
arrow = plt.Arrow(3, 2, 2, 0, ec='k', fc=(1, 1, 1))
ax.add_patch(arrow)
Elight = ax.text(.7, 1, r"E", fontsize=16, color='r', visible=False)
"""

xCoords = np.linspace(.5,5.5,num=10)
arrows = []
codes = [Path.MOVETO,
         Path.CURVE4,
         Path.CURVE4,
         Path.CURVE4,
         ]

id = 0
for xCoord in xCoords:
    circle = plt.Circle((xCoord, .2), .1, fc='r', ec='k')
    ax.add_patch(circle)
    dx = 3 - xCoord
    px = xCoord
    verts = ((provXCtr, provYCtr), 
             ((provXCtr + xCoord)/2., provYCtr),
             (xCoord, provYCtr),
             (xCoord, .2))
    path = Path(verts, codes)
    patch = patches.PathPatch(path, facecolor='none', 
                              lw=1, ec='#afafaf', visible=False)
    ax.add_patch(patch)
    arrows.append(patch)
    agents.append({'id':(id), 'circ':circle, 'path':patch, 'x':0.0})
    id += 1
    
# for agent in range(len(agents)):
#     print 'id: %d'%id

square = plt.Rectangle((provXOrg, provYOrg), 
                       provSize, provSize, fc=(0,1,0), ec='k')
ax.add_patch(square)

# Update each loop
def update(num):
    print 'num = %d'%num
    if num >= 5:
        # print 'num >= 5'
        arrows[2].set_visible(True)
    if num >= 10:
        arrows[2].set_ec('#00ff00')
        arrows[2].set_lw(2)
    if num >= 11:
        if num%2 == 0:
            arrows[2].set_ec('#afafaf')
            arrows[2].set_lw(1)
        else:
            arrows[2].set_ec('#00ff00')
            arrows[2].set_lw(2)
    if num >= 15:
        arrows[6].set_visible(True)
    if num >= 17:
        if num%2 == 0:
            arrows[6].set_ec('#00ff00')
            arrows[6].set_lw(2)
        else:
            arrows[6].set_ec('#afafaf')
            arrows[6].set_lw(1)
    if num >= 20:
        arrows[0].set_visible(True)
    if num >= 22:
        if num%2 == 0:
            arrows[0].set_ec('#00ff00')
            arrows[0].set_lw(2)
        else:
            arrows[0].set_ec('#afafaf')
            arrows[0].set_lw(1)
    if num >= 25:
        arrows[8].set_visible(True)
    if num >= 27:
        if num%2 == 0:
            arrows[8].set_ec('#afafaf')
            arrows[8].set_lw(1)
        else:
            arrows[8].set_ec('#00ff00')
            arrows[8].set_lw(2)
    

    time.sleep(delay)

# Run the animation
ani = animation.FuncAnimation(fig, update, frames=100,
                              interval=1000, repeat=True)

# Show plot
plt.show()
figmgr = plt.get_current_fig_manager()
figmgr.canvas.manager.window.raise_()
geom = figmgr.window.geometry()
xLoc, yLoc, dxWidth, dyHeight = geom.getRect()
figmgr.window.setGeometry(10, 10, dxWidth, dyHeight)
