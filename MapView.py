# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 13:14:39 2015

@author: slehar
"""

import matplotlib.pyplot as plt

# Parameters
winXInches = 8
winYInches = 9.5
axXLim = (0, 7)
axYLim = (0, 8.5)

# Open figure and set axes 1 for drawing Artists
plt.close('all')
# fig = plt.figure(figsize=(winXInches, winYInches))
fig = plt.figure(figsize=(8, 9.5))
fig.canvas.set_window_title('MapView')
ax = fig.add_axes([.1, .1, .8, .8])
# ax.set_xlim(axXLim)
# ax.set_ylim(axYLim)
ax.set_xticklabels([])
ax.set_yticklabels([])
ax.set_xticks([])
ax.set_yticks([])



mapImg = plt.imread('UHF42EdMap.png')
plt.imshow(mapImg)

# Show plot
plt.show()
figmgr = plt.get_current_fig_manager()
figmgr.canvas.manager.window.raise_()
geom = figmgr.window.geometry()
xLoc, yLoc, dxWidth, dyHeight = geom.getRect()
figmgr.window.setGeometry(10, 10, dxWidth, dyHeight)
