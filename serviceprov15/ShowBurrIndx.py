# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 16:39:57 2015

@author: slehar
"""

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

fig = plt.Figure()
ax = fig.add_subplot(111)


burrImg = Image.open('BurroughsIndex.png')
    
burrIndx = np.array(burrImg.convert('P'))

(ySize, xSize) = burrIndx.shape

for y in range(ySize):
    for x in range(xSize):
        if burrIndx[y,x] not in (0, 1, 2, 3, 4, 5):
            burrIndx[y,x] = 0


plt.imshow(burrImg)


