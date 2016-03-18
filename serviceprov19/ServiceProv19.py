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
import time

print '====[ Initialize ]===='
print time.ctime()
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
# ani = animation.FuncAnimation(axes.fig, agents.update, frames=35, repeat=False)

nCycles = 35
print '====[ Starting Animation nCycles = %d nAgents = %d stepped = %r outfile = %s ]===='%(
                    nCycles, agents.nAgents, axes.checkStepped, agents.dataFileName) 
print time.ctime()
start = time.time()
cycle = 0
while True:
    print '  Cycle: %03d nPtsd: %d %s'%(cycle, agents.nPtsd, time.ctime())
    nZeros = 0
    zerosFound = False
    for count, agent in enumerate(agents.agents):
        print '    update(%3d) nPtsd = %d'%(count, agents.nPtsd)
        agents.update(count)
        if agents.nPtsd == 0:
            nZeros += 1
            #print  '    nZeros += %1d'%nZeros
            if nZeros >= 3:
                print '  NPTSD = zero Break!'
                zerosFound = True
                break
        else:
            nZeros = 0
            #print  '    nZeros 0= %1d'%nZeros
        
    #plt.show(block=False)
    if zerosFound:
        break
    else:
        cycle += 1
        
print '====[ Animation Done! ]===='
print time.ctime()
end = time.time()
elapsed = end - start
(min_, sec) = divmod(elapsed, 60)
(hr, min_)  = divmod(min_, 60)
print 'elapsed time = %02d:%02d:%02d'%(hr, min_, sec)



# Show plot
plt.show()
figmgr = plt.get_current_fig_manager()
figmgr.canvas.manager.window.raise_()
geom = figmgr.window.geometry()
xLoc, yLoc, dxWidth, dyHeight = geom.getRect()
figmgr.window.setGeometry(10, 10, dxWidth, dyHeight)



