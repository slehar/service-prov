# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation

import axes
import agents

axes.init_ax()
axes.init_ax2()
axes.init_ax3()
axes.init_ax4()

agents.init_agents()

# Run the animation
ani = animation.FuncAnimation(axes.fig, agents.update, interval=100., repeat=True)



# Show plot
plt.show()
figmgr = plt.get_current_fig_manager()
figmgr.canvas.manager.window.raise_()
geom = figmgr.window.geometry()
xLoc, yLoc, dxWidth, dyHeight = geom.getRect()
figmgr.window.setGeometry(10, 10, dxWidth, dyHeight)


