# ServiceProv1.py
# 
# Model of service provision
# Added slider

import numpy as np
from matplotlib.patches import Circle, Rectangle
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import CheckButtons, Slider

# Global Variables
flow = False
x = 0.001
A = .1

# Figure 1 8x4"
plt.close('all')
fig, ax = plt.subplots(1,figsize=(16,8))
fig.canvas.set_window_title('ServiceProv1')
ax=plt.gca()
ax.set_xlim([0,8]) # X Axis 1-100
ax.set_ylim([0,4]) # Y Axis 1-100
ax.set_xticklabels([])
ax.set_yticklabels([])
ax.set_xticks([])
ax.set_yticks([])

# Add Artists (circle, square, arrow)
square = plt.Rectangle((1,1),2,2,fc=(0,1,0),ec='k')
ax.add_patch(square)
circle = plt.Circle((6,2), 1,fc='r',ec='k')
ax.add_patch(circle)
arrow = plt.Arrow(3,2,2,0,ec='k',fc=(1,1,1))
ax.add_patch(arrow)

# Add Input checkbox
axCh = plt.axes([.5,.15,.1,.2])
axCh.spines['bottom'].set_color('none')
axCh.spines['top'   ].set_color('none')
axCh.spines['left'  ].set_color('none')
axCh.spines['right' ].set_color('none')
check = CheckButtons(axCh, ['Input'], [False])

# Attach to callback function
def func(label):
    global flow
    flow = not flow
    if flow:
        arrow.set_facecolor((0,1,0))
    else:
        arrow.set_facecolor((1,1,1))
            
    plt.draw()
check.on_clicked(func)

# Add Input slider
axSl = plt.axes([0.15, 0.15, 0.3, 0.1])
axSl.set_xticklabels([])
axSl.set_yticklabels([])
axSl.set_xticks([])
axSl.set_yticks([])
sl = Slider(axSl, 'Mag', 0., 1., valinit=0.5, valfmt=u'%1.2f', fc=(0,1,0))

# Update each loop
def update(num):
    global x
    if flow:
        #I = sl.val*0.01
        I = 0.1 * sl.val
    else:
         I = 0.
    x += -A*x + (1-x)*I
    if x<0.:
        x = 0.
    elif x > 1.:
        x = 1.
    r = (1.-x)
    g = x
    circle.set_facecolor((r,g,0.))
  
# Run the animation
ani = animation.FuncAnimation(fig, update, frames=10, \
                                interval=10, repeat=True)

# Show plot
plt.show()
figmgr=plt.get_current_fig_manager()
figmgr.canvas.manager.window.raise_()
geom=figmgr.window.geometry()
x,y,dx,dy=geom.getRect()
figmgr.window.setGeometry(10,10,dx,dy)
