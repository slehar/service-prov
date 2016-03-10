#!/Users/slehar/anaconda/bin/python
#
# Calculates thresholds
#
# Starting with %percentages of race/ethnicity by borough, calculate a set of thresholds between 0% 
# and 100% such that a random variable rand()*100 will have the same probability of falling within a
# race/ethnicity bin as the populations of the respective boroughs.
#
# These numbers are superceded by new numbers that do income, age, sex, and race/ethnicity from 
# Demos by borough 022416.xlsx (email from Laura 2016/02/24 as seen in companion script calcThresholdsDemo.py
# in this same directory
#
#              %white          %black         %other     %white-hisp    %black-hisp    %other-hisp
Bronx =     [ 10.93349221,   30.27999862,  5.268529766,  11.57538713,   4.468379156,   37.47421312 ]
Brooklyn =  [ 35.67675128,   32.22860304,  12.29076626,  8.891369581,   1.981940034,   8.930569816 ]
Manhattan = [ 47.74248701,   13.02107112,  13.60300864,  9.195264086,   2.494527896,   13.94364124 ]
Queens =    [ 27.56272013,   17.69939973,  27.25936551,  14.9545326,    1.161382868,   11.36259915 ]
Staten =    [ 64.17627793,   9.536182623,   9.11344353,  11.58283765,   0.847613232,   4.743645036 ]

sum = 0
print "\nBronx"
for entry in range(6):
    sum += Bronx[entry]
    print "t[%1d] = %f"%(entry+1, sum)

sum = 0
print "\nBrooklyn"
for entry in range(6):
    sum += Brooklyn[entry]
    print "t[%1d] = %f"%(entry+1, sum)

sum = 0
print "\nManhattan"
for entry in range(6):
    sum += Manhattan[entry]
    print "t[%1d] = %f"%(entry+1, sum)

sum = 0
print "\nQueens"
for entry in range(6):
    sum += Queens[entry]
    print "t[%1d] = %f"%(entry+1, sum)

sum = 0
print "\nStaten"
for entry in range(6):
    sum += Staten[entry]
    print "t[%1d] = %f"%(entry+1, sum)

