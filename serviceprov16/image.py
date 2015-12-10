# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 12:24:52 2015

@author: slehar
"""

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import axes

imgXSize = None
imgYSize = None
imgZSize = None
aspect = 1.0
xOff = None
mapImg = None
maskImg = None
burrImg = None
burrIndx = None


#########[ init map ]########
def init_map():
    
    global aspect, mapImg, maskImg, burrImg, burrIndx, imgXSize, imgYSize, imgZSize, xOff
    
    # Display Boroughs Index Map
    burrImg = Image.open('BurroughsIndxNoBg.png')
    (imgXSize, imgYSize) = burrImg.size
        
    burrIndx = np.array(burrImg.convert('P'))
    
    # Clean up partial-surface pixels
    for y in range(imgYSize):
        for x in range(imgXSize):
            if burrIndx[y,x] not in (0, 1, 2, 3, 4, 5):
                burrIndx[y,x] = 0
    
    
    aspect = float(imgXSize)/float(imgYSize)
    (xScale, yScale) = (imgXSize * aspect / imgXSize, 1.)
    xOff = (1. - xScale)/2.
    # axes.ax.imshow(burrImg, extent=[xOff, xOff+xScale, 0, yScale])
    
    # Load Background Image
    backImg = plt.imread('UHF42EdMap.png')
    axes.ax.imshow(backImg, extent=[xOff, xOff+xScale, 0, yScale], alpha=1)
    
    # Display Boroughs Index Map
    axes.ax.imshow(burrImg, extent=[xOff, xOff+xScale, 0, yScale])
    
    
    # Load mask map
    maskImg = plt.imread('BurroughsMask.png')
    axes.ax.imshow(maskImg, extent=[xOff, xOff+xScale, 0, yScale], alpha=.5)

    # Load Key Legend Image
    keyImg = plt.imread('DemoKey1.png')
    axes.ax5.imshow(keyImg)
