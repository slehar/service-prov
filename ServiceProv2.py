# ServiceProv2.py
# 
# Model of service provision
# Added time trace

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import CheckButtons, Slider
from collections import deque
# import time

# Global Variables
flow = False
x = 0.001
t = 0.
lastX = 0.
lastT = 0.
dt = .5
A = .1
dArray = deque([0.])
tArray = deque([0.])
plotWidth = 500

# Open figure and set axes 1 for drawing Artists
plt.close('all')
fig = plt.figure(figsize=(10,8))
fig.canvas.set_window_title('ServiceProv2')
ax=fig.add_axes([.2,.65,.5,.3])
ax.set_xlim([0,8]) 
ax.set_ylim([0,4])
ax.set_xticklabels([])
ax.set_yticklabels([])
ax.set_xticks([])
ax.set_yticks([])


# Add Artists to axes 1 (circle, square, arrow) 
square = plt.Rectangle((1,1),2,2,fc=(0,1,0),ec='k')
ax.add_patch(square)
circle = plt.Circle((6,2), 1,fc='r',ec='k')
ax.add_patch(circle)
arrow = plt.Arrow(3,2,2,0,ec='k',fc=(1,1,1))
ax.add_patch(arrow)

# ax.text(1.8,3.5, 'Grossberg Shunting Neuron', fontsize=14, weight='bold')
ax.set_title('Grossberg Shunting Neuron')
ax.text(1.9, .3, 'I', fontsize=16, weight='bold', style='italic')
ax.text(6,   .3, 'x', fontsize=16, weight='bold', style='oblique')

# Add axes for equation
axEq = fig.add_axes([.2, .54, .5, .08])
axEq.set_xticklabels([])
axEq.set_yticklabels([])
axEq.set_xticks([])
axEq.set_yticks([])
axEq.axes.axesPatch.set_facecolor([.75,.75,.75])
axEq.spines['top'].set_color([.75,.75,.75])
axEq.spines['bottom'].set_color([.75,.75,.75])
axEq.spines['left'].set_color([.75,.75,.75])
axEq.spines['right'].set_color([.75,.75,.75])
axEq.text(.1,.3,r'$\frac{dx}{dt}$ = -Ax + (1-x)I', 
          family='serif', style='italic', size=36)



# Add Input checkbox as axes Ch
axCh = fig.add_axes([.6,.4,.1,.1])
check = CheckButtons(axCh, ['Input'], [False])

# Checkbox callback function
def func(label):
    global flow
    flow = not flow
    if flow:
        arrow.set_facecolor((0,1,0))
    else:
        arrow.set_facecolor((1,1,1))
            
    plt.draw()
check.on_clicked(func)

# Add axes 2 for plot trace
axTime = fig.add_axes([.1,.1,.8,.2])
axTime.set_ylim(0, 1)
axTime.set_xlim(0, plotWidth)

# Set up plot line in axes 2
line, = axTime.plot(t, x, color='blue', linewidth=1, 
                 linestyle='-', alpha=1.0)  

# Add Input slider
axSlI = fig.add_axes([.2,.45,.3,.05])
axSlI.set_xticklabels([])
axSlI.set_yticklabels([])
axSlI.set_xticks([])
axSlI.set_yticks([])
axSlI.set_title('Input')
slI = Slider(axSlI, 'I', 0., 10., valinit=1., valfmt=u'%1.2f', fc=(0,1,0))

# Add Decay slider
axSlA = fig.add_axes([.2,.35,.3,.05])
axSlA.set_xticklabels([])
axSlA.set_yticklabels([])
axSlA.set_xticks([])
axSlA.set_yticks([])
axSlA.set_title('Decay')
slA = Slider(axSlA, 'A', 0., 1., valinit=.1, valfmt=u'%1.2f', fc=(1,0,0))

# Update each loop
def update(num):
    global x,t,lastX,lastT
    global darray, tarray
    if flow:
        #I = sl.val*0.01
        I = 0.1 * slI.val
    else:
         I = 0.
    lastX = x
    x += -slA.val*x + (1-x)*I
    if x < 0.:
        x = 0.
    elif x > 1.:
        x = 1.
    r = (1.-x)
    g = x
    circle.set_facecolor((r,g,0.))
    lastT = t
    t += dt
    dArray.appendleft(x)
    if len(dArray) >= plotWidth/dt:
        dArray.pop()
    tArray.appendleft(t)
    if len(tArray) >= plotWidth/dt:
        tArray.pop()
    # axTime.set_xlim(tarray[0],tarray[len(tarray)-1])
    #line.set_data([.1,0],[lastX,x])
    line.set_data(tArray,dArray)
    #CurrentXAxis=np.arange(len(values)-100,len(values),1)
    axTime.axis((t - plotWidth, t, 0., 1.))
    # time.sleep(.1)
        
        
# Run the animation
ani = animation.FuncAnimation(fig, update, frames=10, \
                                interval=10, repeat=True)

# Show plot
plt.show()
figmgr=plt.get_current_fig_manager()
figmgr.canvas.manager.window.raise_()
geom=figmgr.window.geometry()
xLoc,yLoc,dxWidth,dyHeight=geom.getRect()
figmgr.window.setGeometry(10,10,dxWidth,dyHeight)
