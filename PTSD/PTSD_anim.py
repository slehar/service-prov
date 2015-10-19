# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import matplotlib.pyplot as plt
import numpy as np

# Parameters
rampUp = .7
onset = 1.
duration = 3.
offset = onset + rampUp + duration

# Open figure and set axes 1 for drawing Artists
plt.close('all')
fig = plt.figure(figsize=(10,8))
fig.canvas.set_window_title('PTSD Animation')
ax = fig.add_axes([.1, .1, .8, .8])
ax.set_xlim([-1, 12])
ax.set_ylim([-.5, 1.5])
ax.set_xticks(range(13))

t = np.arange(-1, 12.0, 0.1)
s1 = 1./(1. + np.exp(-10.*(t - rampUp - onset)))
s2 = 1./(1. + np.exp(-10.*(t - offset)))
s3 = s1 - s2
# s3[s3<0] - 0.
# plt.plot(t, s1)
# plt.plot(t, s2)
plt.plot(t, s3)

plt.xlabel('time since trauma (months)')
plt.ylabel('PTSD symptoms')
plt.title('PTSD Time Course')
plt.grid(True)
plt.annotate('Trauma event', xy=(0,0), xytext=(0, -.25),
             arrowprops=dict(facecolor='black', shrink=0.1))
plt.annotate('Onset', xy=(onset,-.25), xytext=(onset, -.45),
             arrowprops=dict(facecolor='black', shrink=0.05))
plt.annotate('Offset', xy=(offset,-.25), xytext=(offset, -.45),
             arrowprops=dict(facecolor='black', shrink=0.05))


# Show plot
plt.show()
figmgr=plt.get_current_fig_manager()
figmgr.canvas.manager.window.raise_()
geom=figmgr.window.geometry()
xLoc,yLoc,dxWidth,dyHeight=geom.getRect()
figmgr.window.setGeometry(10,10,dxWidth,dyHeight)
