# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider
from vertslider import VertSlider
# import matplotlib.animation as animation

# Parameters
rampUp = .7
onset = 0.
duration = 0.
offset = onset + rampUp + duration
magnitude = 1.

# Open figure
plt.close('all')
fig = plt.figure(figsize=(10,8))
fig.canvas.set_window_title('PTSD Animation')

# Add axes
ax = fig.add_axes([.1, .2, .8, .7])
ax.set_xlim([-1, 12])
# ax.set_ylim([-.5, 1.5])
ax.set_ylim([-8.5, 25.5])
ax.set_xticks(range(13))

t = np.arange(-1, 12.0, 0.1)
s1 = 1./(1. + np.exp(-10.*(t - rampUp - onset)))
s2 = 1./(1. + np.exp(-10.*(t - offset)))
s3 = (s1 - s2)*magnitude
line, = ax.plot(t, s3)
# plt.plot(t, s3)

plt.xlabel('time since trauma (months)')
plt.ylabel('PTSD symptoms')
plt.title('PTSD Time Course')
plt.grid(True)
plt.annotate('Trauma event', xy=(0,0), xytext=(0, -4.25),
             arrowprops=dict(facecolor='black', shrink=0.1))
arrow1 = plt.annotate('Onset', xy=(onset,-4.25), xytext=(onset, -7.65),
             arrowprops=dict(facecolor='black', shrink=0.05))
arrow2 = plt.annotate('Offset', xy=(offset,-4.25), xytext=(offset, -7.65),
             arrowprops=dict(facecolor='black', shrink=0.05))
arrow3 = plt.annotate('', xy=(onset, -5.1),  xytext=(offset, -5.1), 
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
slOnset = Slider(axOn, 'Onset', 0., 10., valinit=0.)

# Add axDur duration slider axes
axDur = fig.add_axes((.6, .05, .3, .07))
axDur.set_xticklabels([])
axDur.set_yticklabels([])
axDur.set_xticks([])
axDur.set_yticks([])

# Duration slider
slDur   = Slider(axDur, 'Duration', 0., 6., valinit=1.)

# Add axMag magnitude slider axes
axMag = fig.add_axes((.92, .37, .06, .355))
axMag.set_xticklabels([])
axMag.set_yticklabels([])
axMag.set_xticks([])
axMag.set_yticks([])

# Duration slider
slMag = VertSlider(axMag, 'Magnitude', 0., 17., valinit=17.)

# Add state text & magnitude text
plt.sca(ax)
stateText = plt.text(2, 20, 'PTSD', fontsize=24, visible=False)
magText   = plt.text(4, 20, 'Acute', fontsize=24, visible=False)
durText   = plt.text((offset - onset)/2 + 1, -.25, '< %5.2d >'%duration, fontsize=10,
                     backgroundcolor='w')
delText   = plt.text(7, 20, 'Delayed Onset', fontsize=24, visible=False)

def update(val):
    global onset, duration, s1, s2, s3, magnitude, stateText
    onset = slOnset.val
    duration = slDur.val + rampUp
    offset = onset + duration
    magnitude = slMag.val
    # print 'onset = %5.2f \tduration = %5.2f'%(onset, duration) 
    s1 = 1./(1. + np.exp(-10.*(t - rampUp - onset)))
    s2 = 1./(1. + np.exp(-10.*(t - offset)))
    s3 = (s1 - s2)*magnitude
    line.set_data(t, s3)
    arrow1.xy = (onset, -4.25)
    arrow1.set_x(onset)
    arrow2.xy = (offset - rampUp, -4.25)
    arrow2.set_x(offset - rampUp)
    arrow3.xy = (onset, -5.1)
    arrow3.xytext=(offset - rampUp, -5.1)
    durText.set_x((offset - onset)/2 + onset - .5)
    durText.set_y(-5.44)
    durText.set_text(' < %5.2f >'%(duration - rampUp))
    
    stateText.set_visible(duration >= 1)
    magText.set_visible(stateText.get_visible())
    if (duration - rampUp >= .5) and magnitude >= 6.:
        stateText.set_visible(True)
        magText.set_visible(True)
        if ((duration - rampUp) >= 1. and duration <= 3.):
            magText.set_text('Acute')
        elif ((duration - rampUp) > 3):
            magText.set_text('Chronic')
        if (onset >= 6. and stateText.get_visible()):
            delText.set_visible(True)
        else:
            delText.set_visible(False)
            
    else:
        stateText.set_visible(False)
        magText.set_visible(False)
        delText.set_visible(False)
            
    
    
slOnset.on_changed(update)
slDur.on_changed(update)
slMag.on_changed(update)


# Show plot
plt.show()
figmgr=plt.get_current_fig_manager()
figmgr.canvas.manager.window.raise_()
geom=figmgr.window.geometry()
xLoc,yLoc,dxWidth,dyHeight=geom.getRect()
figmgr.window.setGeometry(10,10,dxWidth,dyHeight)
