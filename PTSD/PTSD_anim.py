# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider
# import matplotlib.animation as animation

# Parameters
rampUp = .7
onset = 0.
duration = 0.
offset = onset + rampUp + duration

# Open figure
plt.close('all')
fig = plt.figure(figsize=(10,8))
fig.canvas.set_window_title('PTSD Animation')

# Add axes
ax = fig.add_axes([.1, .2, .8, .7])
ax.set_xlim([-1, 12])
ax.set_ylim([-.5, 1.5])
ax.set_xticks(range(13))



t = np.arange(-1, 12.0, 0.1)
s1 = 1./(1. + np.exp(-10.*(t - rampUp - onset)))
s2 = 1./(1. + np.exp(-10.*(t - offset)))
s3 = s1 - s2
line, = ax.plot(t, s3)
# plt.plot(t, s3)

plt.xlabel('time since trauma (months)')
plt.ylabel('PTSD symptoms')
plt.title('PTSD Time Course')
plt.grid(True)
plt.annotate('Trauma event', xy=(0,0), xytext=(0, -.25),
             arrowprops=dict(facecolor='black', shrink=0.1))
arrow1 = plt.annotate('Onset', xy=(onset,-.25), xytext=(onset, -.45),
             arrowprops=dict(facecolor='black', shrink=0.05))
arrow2 = plt.annotate('Offset', xy=(offset,-.25), xytext=(offset, -.45),
             arrowprops=dict(facecolor='black', shrink=0.05))

axOn = fig.add_axes((.1, .05, .3, .07))
axOn.set_xlim(0, 6)
axOn.set_xticklabels(range(7))
# axOn.set_yticklabels([])
axOn.set_xticks([])
# axOn.set_yticks([])

slOnset = Slider(axOn, 'Onset', 0., 6., valinit=0.)

axDur = fig.add_axes((.6, .05, .3, .07))
axDur.set_xticklabels([])
axDur.set_yticklabels([])
axDur.set_xticks([])
axDur.set_yticks([])

slDur   = Slider(axDur, 'Duration', 0., 6., valinit=1.)

def update(val):
    global onset, duration, s1, s2, s3
    onset = slOnset.val
    duration = slDur.val + rampUp
    offset = onset + duration
    # print 'onset = %5.2f \tduration = %5.2f'%(onset, duration) 
    s1 = 1./(1. + np.exp(-10.*(t - rampUp - onset)))
    s2 = 1./(1. + np.exp(-10.*(t - offset)))
    s3 = s1 - s2
    line.set_data(t, s3)
    arrow1.xy = (onset, -0.25)
    arrow1.set_x(onset)
    arrow2.xy = (offset, -0.25)
    arrow2.set_x(offset)
    
    
slOnset.on_changed(update)
slDur.on_changed(update)


# Show plot
plt.show()
figmgr=plt.get_current_fig_manager()
figmgr.canvas.manager.window.raise_()
geom=figmgr.window.geometry()
xLoc,yLoc,dxWidth,dyHeight=geom.getRect()
figmgr.window.setGeometry(10,10,dxWidth,dyHeight)
