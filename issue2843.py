# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 11:03:20 2015

@author: slehar
"""

import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons

fig = plt.figure()
ax = plt.axes([.4, .4, .2, .3])
plt.title('Sex')

    
# Radio buttons in ax
radioSex    = RadioButtons(ax, ['Male', 'Female'])

def sexfunc(label):
    print 'In sexfunc()'
    sexdict = {'Male':'M', 'Female':'F'}
    sex = sexdict[label]
    print '  sex = %r'%sex
radioSex.on_clicked(sexfunc)

plt.show()
