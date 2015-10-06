# ServiceProv4.py
#
# Model of service provision
# Add therapy supply-side

import numpy as np
# from matplotlib.patches import Circle, Rectangle
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import CheckButtons, Slider
from collections import deque
import time

# Global Variables
flow = False
valveOpen = False
xx = 0.001
t = 0.
lastX = 0.
lastT = 0.
dt = .5
A = .01
delay = 0.1     # sec per cycle
refill = 0.001
darray = deque(np.arange(0., 9., .1))
tarray = deque(np.arange(0., 9., .1))
flevel = 1.0
lastflevel = 1.0
empty = False

# Open figure and set axes 1 for drawing Artists
plt.close('all')
fig = plt.figure(figsize=(10,8))
fig.canvas.set_window_title('ServiceProv4')
ax = fig.add_axes([.2, .6, .5, .3])
ax.set_xlim([0, 8])
ax.set_ylim([0, 4])
ax.set_xticklabels([])
ax.set_yticklabels([])
ax.set_xticks([])
ax.set_yticks([])

# Add Artists to axes 1 (circle, square, arrow)
square = plt.Rectangle((1, 1), 2, 2, fc=(1, 1, 1), ec='k')
ax.add_patch(square)
fluid = plt.Rectangle((1, 1), 2, 2*flevel, fc=(0, 1, 0))
ax.add_patch(fluid)
circle = plt.Circle((6, 2), 1, fc='r', ec='k')
ax.add_patch(circle)
arrow = plt.Arrow(3, 2, 2, 0, ec='k', fc=(1, 1, 1))
ax.add_patch(arrow)

# Add Input checkbox as axes Ch
axCh = fig.add_axes([.6, .4, .1, .1])
check = CheckButtons(axCh, ['Input'], [False])


# Checkbox callback function
def func(label):
    global valveOpen, empty
    '''
    if not empty:
        flow = True
        arrow.set_facecolor((0, 1, 0))
    else:
        arrow.set_facecolor((1, 1, 1))
        flow = False

    plt.draw()
    '''
    valveOpen = True
    if not empty:
        arrow.set_facecolor((0, 1, 0))
        plt.draw()


check.on_clicked(func)

# Add axes 2 for plot trace
ax2 = fig.add_axes([.1, .1, .8, .2])
ax2.set_ylim(0, 1)
ax2.set_xlim(0, 10)

# Set up plot line in axes 2
line, = ax2.plot(t, xx, color='blue', linewidth=1,
                 linestyle='-', alpha=1.0)

# Add Input slider
axSl = fig.add_axes([.2, .4, .3, .1])
axSl.set_xticklabels([])
axSl.set_yticklabels([])
axSl.set_xticks([])
axSl.set_yticks([])
sl = Slider(axSl, 'Mag', 0., 1., valinit=0.5, valfmt=u'%1.2f', fc=(0, 1, 0))


# Update each loop
def update(num):
    global xx, flevel, empty, t, lastX, lastT, flow, valveOpen, refill, delay
    global darray, tarray
    
    if valveOpen and not empty:
        I = 0.1 * sl.val
        flevel -= 0.1
        if flevel < 0.1:
            flevel = 0.
            empty = True
            flow = False
    else:
        I = 0.
        #flow = False
    fluid.set_height(flevel*2.)
    
    if flow:
        arrow.set_facecolor((0, 1, 0))
    else:
        arrow.set_facecolor((1, 1, 1))
    

    # Update dynamic equations
    lastX = xx
    xx += -A*xx + (1-xx)*I  # Grossberg shunting equation
    if xx < 0.:
        xx = 0.
    elif xx > 1.:
        xx = 1.
    r = (1.-xx)
    g = xx
    circle.set_facecolor((r, g, 0.))
    lastT = t
    t += dt
    darray.appendleft(xx)
    darray.pop()
    tarray.appendleft(t)
    tarray.pop()
    ax2.set_xlim(tarray[0], tarray[len(tarray)-1])
    # line.set_data([.1,0], [lastX,x])
    line.set_data(tarray, darray)
    # CurrentXAxis=np.arange(len(values)-100,len(values),1)
    ax2.axis()
    
    valveOpen = False  # Shut valve after treatment
    check.lines[0][0].set_visible(False)
    check.lines[0][1].set_visible(False)
    flevel += refill
    if flevel > .1:
        empty = False
    if flevel > 1.:
        flevel = 1

    time.sleep(delay)


# Run the animation
ani = animation.FuncAnimation(fig, update, frames=10,
                              interval=10, repeat=True)

# Show plot
plt.show()
figmgr=plt.get_current_fig_manager()
figmgr.canvas.manager.window.raise_()
geom=figmgr.window.geometry()
xLoc,yLoc,dxWidth,dyHeight=geom.getRect()
figmgr.window.setGeometry(10,10,dxWidth,dyHeight)
