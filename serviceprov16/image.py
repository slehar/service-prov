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
    
    # Display Background Map
    # burrImg = plt.imread('BurroughsIndex.png')
    # (imgYSize, imgXSize, imgZSize) = burrImg.shape
    burrImg = Image.open('BurroughsIndx.png')
    (imgXSize, imgYSize) = burrImg.size
        
    burrIndx = np.array(burrImg.convert('P'))
    
    # Clean up partial-surface pixels
    for y in range(imgYSize):
        for x in range(imgXSize):
            if burrIndx[y,x] not in range(6):
                burrIndx[y,x] = 0
    
    
    aspect = float(imgXSize)/float(imgYSize)
    (xScale, yScale) = (aspect, 1.)
    xOff = (1. - xScale)/2.
    axes.ax.imshow(burrImg, extent=[xOff, xOff+xScale, 0, yScale])
    
    # Load mask map
    maskImg = plt.imread('BurroughsMask.png')
    axes.ax.imshow(maskImg, extent=[xOff, xOff+xScale, 0, yScale], alpha=.5)


