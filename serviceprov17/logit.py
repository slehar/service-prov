# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 12:42:08 2015

@author: slehar
"""

import numpy as np

# Calculate distribution
def logit(isMale, isOld, isBlack, isHisp, isOther, hadPrior):
    

    # print 'In logit()'
    

    '''               
    print '\n====[ calculate distribution ]===='
    print '  isMale = %d'%isMale
    print '  isOld  = %d'%isOld
    print '  isOld    = %d'%isOld
    print '  isWhiteHispanic = %d'%isWhiteHispanic
    print '  isBlackHispanic = %d'%isBlackHispanic
    print '  isOtherHispanic = %d'%isOtherHispanic
    print '  isWhiteNonHisp  = %d'%isWhiteNonHisp
    print '  isBlackNonHisp  = %d'%isBlackNonHisp
    print '  isOtherNonHisp  = %d'%isOtherNonHisp
    print '  hasIncome1 = %d'%hasIncome1
    print '  hasIncome2 = %d'%hasIncome2
    print '  hasIncome3 = %d'%hasIncome3
    print '  hadStressors  = %d'%hadStressors
    print '  nSandyTraumas = %d'%nSandyTraumas
    '''

    
    logitCBT = -1.60 +                \
              (-0.2008   * isMale)  + \
              (-0.5828   * isBlack) + \
              (-1.073    * isHisp)  + \
              (-0.35     * isOther) + \
              (0.2449    * isOld)   + \
              (1.8377    * hadPrior)
              
    probCBT = np.exp(logitCBT)/(1. + np.exp(logitCBT))

              
    print 'logitCBT      = %f'%logitCBT
    print 'probCBT       = %f'%probCBT
    
    return probCBT
