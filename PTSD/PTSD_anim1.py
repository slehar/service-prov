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
arrow3 = plt.annotate('', xy=(onset, -.25),  xytext=(offset, -.25), 
                      arrowprops=dict(arrowstyle='<->'))

# Add axOn onset slider axes
axOn = fig.add_axes([.1, .05, .3, .07])
axOn.set_xlim(0, 6)
axOn.grid(True)
axOn.set_xticklabels(str(range(7)))
axOn.set_yticklabels([])
axOn.set_xticks([])
# axOn.set_yticks([])

# Onset slider
slOnset = Slider(axOn, 'Onset', 0., 6., valinit=0.)

# Add axDur duration slider axes
axDur = fig.add_axes((.6, .05, .3, .07))
axDur.set_xticklabels([])
axDur.set_yticklabels([])
axDur.set_xticks([])
axDur.set_yticks([])

# Duration slider
slDur   = Slider(axDur, 'Duration', 0., 6., valinit=1.)

# Add state text & magnitude text
plt.sca(ax)
stateText = plt.text(4, 1.25, 'PTSD', fontsize=24, visible=False)
magText   = plt.text(6, 1.25, 'Acute', fontsize=24, visible=False)
durText   = plt.text((offset - onset)/2 + 1, -.25, '< %5.2d >'%duration, fontsize=10,
                     backgroundcolor='w')

def update(val):
    global onset, duration, s1, s2, s3, stateText
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
    arrow2.xy = (offset - rampUp, -0.25)
    arrow2.set_x(offset - rampUp)
    '''
    arrow3 = plt.annotate('', xy=(onset, -.25),  xytext=(offset, -.25), 
                          arrowprops = dict(arrowstyle='<->'))
    '''
    arrow3.xy = (onset, -.3)
    arrow3.xytext=(offset - rampUp, -.3)
    durText.set_x((offset - onset)/2 + onset - .5)
    durText.set_y(-.32)
    durText.set_text(' < %5.2f >'%(duration - rampUp))
    
    stateText.set_visible(duration >= 1)
    magText.set_visible(stateText.get_visible())
    if (onset <= 4. and duration - rampUp <= 4.):
        stateText.set_text('ASD')
        magText.set_visible(False)
    else:
        stateText.set_text('PTSD')
        magText.set_visible(True)
        if (duration >= 1. and duration <= 3.):
            magText.set_text('Acute')
        elif (duration > 3):
            magText.set_text('Chronic')
        
    # plt.show()
    
    
    
slOnset.on_changed(update)
slDur.on_changed(update)


# Show plot
plt.show()
figmgr=plt.get_current_fig_manager()
figmgr.canvas.manager.window.raise_()
geom=figmgr.window.geometry()
xLoc,yLoc,dxWidth,dyHeight=geom.getRect()
figmgr.window.setGeometry(10,10,dxWidth,dyHeight)
