# -*- coding: utf-8 -*-
"""
Spyder Editor

ServiceProv19.py
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation

import axes
import agents
import image
import agencies
import writelog

axes.init_axes()
image.init_map()
agencies.init_agencies()
agents.init_agents()

# Pick agency square to make it the 'selected' agency
def on_pick(event):
    for boro in agencies.agenciesList:
        found = False
        for agcy in agencies.agenciesList[boro]:
            if agcy['square'] is event.artist:
                found = True
                agencies.selected['square'].set_lw(1)
                agencies.selected['square'].set_ec('k')
                agencies.selected = agcy
                agcy['square'].set_lw(4)
                agcy['square'].set_ec('r')
                if agencies.selected['tileArray'] == []:
                    agents.initTileArray(agencies.selected)
                agents.updateTileArray(agencies.selected)
                axes.schedTitle.set_text(boro+': '+agcy['abbrev']+' '+agcy['name'])
                axes.fig.canvas.draw()
                break
        if found == True:
            break
        
    if agents.doingLogging:
        writelog.write('In on_pick(): selected is now %s %s %s\n'%(
        agencies.selected['boro'], agencies.selected['abbrev'], agencies.selected['name']))

# bind pick events to our on_pick function
cid = axes.fig.canvas.mpl_connect('pick_event', on_pick)


# Run the animation
ani = animation.FuncAnimation(axes.fig, agents.update, frames=35, repeat=False)

# Show plot
plt.show()
figmgr = plt.get_current_fig_manager()
figmgr.canvas.manager.window.raise_()
geom = figmgr.window.geometry()
xLoc, yLoc, dxWidth, dyHeight = geom.getRect()
figmgr.window.setGeometry(10, 10, dxWidth, dyHeight)



