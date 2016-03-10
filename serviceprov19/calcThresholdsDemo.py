# calcThresholdsDemo.py
#
# Calculates thresholds for various demographics. Updated version of calcThresholds.py which is
# superseded by new numbers that do income, age, sex, and race/ethnicity from 
# Demos by borough 022416.xlsx (email from Laura 2016/02/24 as seen in companion script calcThresholdsDemo.py
# in this same directory
#

# Data copied direct from spreadsheet:
# Note: Boroughs re-ordered to our order 
# [Manhattan, Brooklyn, Queens, Bronx, StatenIsl]

####[ Income ]####
print '\n####[ Income ]####'
# Borough          %0-59k         %60-99k         %100k+
ManhattanIncome = [ 45.51753009, 17.33676001, 37.14570991 ]
BrooklynIncome  = [ 60.92281208, 19.17740777, 19.89978015 ]
QueensIncome    = [ 52.46724573, 23.33845585, 24.19429842 ]
BronxIncome     = [ 71.57544883, 16.89207891, 11.53247225 ] 
StatenIslIncome = [ 41.54757904, 24.08309149, 34.36932946 ]

sum = 0
print '#### Manhattan Income ####'
for entry in range(3):
    sum += ManhattanIncome[entry]
    print 't[%1d] = %f'%(entry+1, sum)

sum = 0
print '#### Brooklyn Income ####'
for entry in range(3):
    sum += BrooklynIncome[entry]
    print 't[%1d] = %f'%(entry+1, sum)

sum = 0
print '#### Queens Income ####'
for entry in range(3):
    sum += QueensIncome[entry]
    print 't[%1d] = %f'%(entry+1, sum)

sum = 0
print '#### Bronx Income ####'
for entry in range(3):
    sum += BronxIncome[entry]
    print 't[%1d] = %f'%(entry+1, sum)

sum = 0
print '#### StatenIsl Income ####'
for entry in range(3):
    sum += StatenIslIncome[entry]
    print 't[%1d] = %f'%(entry+1, sum)

####[ Age ]####
print '\n####[ Age ]####'
# Borough           %18-34          %35-64      %65+
ManhattanAge    = [ 38.45179879, 45.65711724, 15.89108397 ]
BrooklynAge     = [ 36.06193501, 48.76640921, 15.17165578 ]
QueensAge       = [ 32.62666042, 51.07078406, 16.30255552 ]
BronxAge        = [ 35.83114759, 49.71441099, 14.45444143 ]
StatenIslAge    = [ 28.89014222, 54.36211031, 16.74774747 ]

sum = 0
print '#### Manhattan Age ####'
for entry in range(3):
    sum += ManhattanAge[entry]
    print 't[%1d] = %f'%(entry+1, sum)

sum = 0
print '#### Brooklyn Age ####'
for entry in range(3):
    sum += BrooklynAge[entry]
    print 't[%1d] = %f'%(entry+1, sum)

sum = 0
print '#### Queens Age ####'
for entry in range(3):
    sum += QueensAge[entry]
    print 't[%1d] = %f'%(entry+1, sum)

sum = 0
print '#### Bronx Age ####'
for entry in range(3):
    sum += BronxAge[entry]
    print 't[%1d] = %f'%(entry+1, sum)

sum = 0
print '#### StatenIsl Age ####'
for entry in range(3):
    sum += StatenIslAge[entry]
    print 't[%1d] = %f'%(entry+1, sum)

####[ Sex ]####
print '\n####[ Sex ]####'
# Borough          %female
ManhattanSex = 52.95124113
BrooklynSex  = 52.79404156
BronxSex     = 53.06225493
QueensSex    = 51.57413307
StatenIslSex = 51.53936811

sum = 0
print '#### Manhattan Sex ####'
print '%f'%ManhattanSex
print '#### Brooklyn Sex ####'
print '%f'%BrooklynSex
print '#### Queens Sex ####'
print '%f'%QueensSex
print '#### Bronx Sex ####'
print '%f'%BronxSex
print '#### StatenIsland Sex ####'
print '%f'%StatenIslSex

####[ Race / Ethnicity ]####
print '\n####[ Race / Ethnicity ]####'
# Borough         
ManhattanRaceEthcy = [ 47.74248701, 13.02107112, 13.60300864, 9.195264086, 2.494527896, 13.94364124 ]
BrooklynRaceEthcy  = [ 35.67675128, 32.22860304, 12.29076626, 8.891369581, 1.981940034, 8.930569816 ]
QueensRaceEthcy    = [ 27.56272013, 17.69939973, 27.25936551, 14.9545326,  1.161382868, 11.36259915 ]
BronxRaceEthcy     = [ 10.93349221, 0.27999862, 5.268529766, 11.57538713, 4.468379156, 37.47421312 ]
StatenIslRaceEthcy = [ 64.17627793, 9.536182623, 9.11344353,  11.58283765, 0.847613232, 4.743645036 ]

sum = 0
print '#### Manhattan RaceEthcy ####'
for entry in range(6):
    sum += ManhattanRaceEthcy[entry]
    print 't[%1d] = %f'%(entry+1, sum)

sum = 0
print '#### Brooklyn RaceEthcy ####'
for entry in range(6):
    sum += BrooklynRaceEthcy[entry]
    print 't[%1d] = %f'%(entry+1, sum)

sum = 0
print '#### Queens RaceEthcy ####'
for entry in range(6):
    sum += QueensRaceEthcy[entry]
    print 't[%1d] = %f'%(entry+1, sum)

sum = 0
print '#### Bronx RaceEthcy ####'
for entry in range(6):
    sum += BronxRaceEthcy[entry]
    print 't[%1d] = %f'%(entry+1, sum)

sum = 0
print '#### StatenIsl RaceEthcy ####'
for entry in range(6):
    sum += StatenIslRaceEthcy[entry]
    print 't[%1d] = %f'%(entry+1, sum)


