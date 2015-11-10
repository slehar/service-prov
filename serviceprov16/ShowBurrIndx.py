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


burrImg = Image.open('BurroughsIndx.png')
    
burrIndx = np.array(burrImg.convert('P'))

(ySize, xSize) = burrIndx.shape


plt.imshow(burrImg)


