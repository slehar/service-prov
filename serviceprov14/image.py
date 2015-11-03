# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 12:24:52 2015

@author: slehar
"""

import matplotlib.pyplot as plt
import axes

imgXSize = None
imgYSize = None
imgZSize = None
aspect = 1.0
xOff = None
mapImg = None
maskImg = None




#########[ init map ]########
def init_map():
    
    global aspect, mapImg, maskImg, imgXSize, imgYSize, imgZSize, xOff
    
    # Display Background Map
    mapImg = plt.imread('UHF42EdMapOverlay.png')
    (imgYSize, imgXSize, imgZSize) = mapImg.shape
    
    aspect = float(imgXSize)/float(imgYSize)
    (xScale, yScale) = (imgXSize * aspect / imgXSize, 1.)
    xOff = (1. - xScale)/2.
    axes.ax.imshow(mapImg, extent=[xOff, xOff+xScale, 0, yScale])
    
    # Load mask map
    maskImg = plt.imread('UHF42EdMapOverlayReverse.png')
    axes.ax.imshow(maskImg, extent=[xOff, xOff+xScale, 0, yScale], alpha=.5)

