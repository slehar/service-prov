# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 12:00:32 2015

@author: slehar
"""

from random import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches

import axes
import agents

########[ init agents ]########
def init_agents():
    
    # global agents, nAgents, square, circle, avgInput
    
    totInput = 0.
    agentId = 0
    
    ## for each agent
    for agtId in range(agents.nAgents):
        # writelog.write("agtId = %d\n"%agtId)
        foundSpace = False
        while not foundSpace:
            xLoc = random() * 8. + 1.
            yLoc = random() * 7. + 1.
            # writelog.write("  xLoc, yLoc = (%4.2f, %4.2f)\n"%(xLoc, yLoc))
            collision = False
            for agt in range(len(agents.agents)):
                xLoc1 = agents.agents[agt]['xLoc']
                yLoc1 = agents.agents[agt]['yLoc']
                dx = xLoc1 - xLoc
                dy = yLoc1 - yLoc
                dist = np.sqrt(dx**2 + dy**2)
                if dist < agents.minSep:
                    collision = True
                    # writelog.write("  COLLISION !!!\n")
                    break   # Stop going through more agents
            if not collision:
                foundSpace = True
                # Otherwise keep searching
    
        # Define agent's circle
        agents.circle = plt.Circle((xLoc, yLoc), .1, fc='r', ec='k')
        axes.ax.add_patch(agents.circle)
    
        # Define agent's bezier links
        iVal = random()  # Random input value (natural wellness)
        # xVal = iVal * 10.
        xVal = .75
        totInput += iVal
        verts = ((axes.provXCtr, axes.provYCtr), # Bezier lnk from prov. to here
                 ((axes.provXCtr + xLoc)/2., axes.provYCtr),
                 (xLoc, (axes.provYCtr + yLoc)/2.),
                 (xLoc, yLoc))
        bezPath = Path(verts, agents.codes)
        bezPatch = patches.PathPatch(bezPath, facecolor='none',
                                  lw=1, ec='#afafaf', visible=False)
    
        # Agent ID number below circle
        idText = axes.ax.text(xLoc-.04, yLoc-.21, '%d'%agtId, visible=False)
    
        # Append to agents list
        agents.agents.append({'id':agtId,
                       'circ':agents.circle,
                       'bezPatch':bezPatch,
                       'xLoc':xLoc,
                       'yLoc':yLoc,
                       'xVal':xVal,
                       'iVal':iVal,
                       'treating':False,
                       'enrolled':False,
                       'treatNo':0,        # current treatment #
                       'idText':idText})
        axes.ax.add_patch(bezPatch)
        agents.bezLines.append(bezPatch)
        agentId += 1
    
    
    
    agents.avgInput = totInput/float(agents.nAgents)
    
    # Service provider square and 2 sigma range
    agents.square = plt.Rectangle((axes.provXOrg, axes.provYOrg),
                           axes.provSize, axes.provSize, fc=(0,1,0), ec='k')
    axes.ax.add_patch(agents.square)
    circle = plt.Circle((axes.provXOrg, axes.provYOrg), radius=agents.rSigma, ec='r',
                        fc='none', linestyle='dashed', visible=False )
    axes.ax.add_patch(circle)

