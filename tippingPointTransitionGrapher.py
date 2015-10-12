### this script plots the tipping point transition based on max growth and growth lag

import matplotlib, sys
import matplotlib.pyplot
import library

def colorDefiner(c):

    if c == 0.:
        theColor = 'blue'
    elif c == 0.5:
        theColor = 'green'
    elif c == 1.:
        theColor = 'orange'
    elif c == 1.5:
        theColor = 'red'
    else:
        print 'error trying to assign colors. exiting...'
        sys.exit()

    return theColor

### MAIN

# 1. data reading
data300 = library.dataReader('../data/300ppmSet3.txt')
data1000 = library.dataReader('../data/1000ppmSet3.txt')

# 2. calculating the max growth rates
print 'fitting data for 300 pppm...'
maxGrowthRates300, uvValues300, growthLag300 = library.characteristicParameterFinder(data300)

print
print 'fitting data for 1,000 pppm...'
maxGrowthRates1000, uvValues1000, growthLag1000 = library.characteristicParameterFinder(data1000)


# 3. plotting
print
print 'plotting the figure...'
figureFile = '../results/figureTPT.pdf'

# 4.1 plotting for 300 ppms
print 'plotting for 300 ppms...'
for i in range(len(maxGrowthRates300)):
    x=growthLag300[i]
    y=maxGrowthRates300[i]
    c=uvValues300[i]

    if x != None:
        theColor = colorDefiner(c)
        matplotlib.pyplot.plot(x, y, 'o', color=theColor, mec='None', mfc=theColor, ms=8, mew=1)

# 4.2 plotting for 1,000 ppms
print 'plotting for 1,000 ppms...'
for i in range(len(maxGrowthRates1000)):
    x=growthLag1000[i]
    y=maxGrowthRates1000[i]
    c=uvValues1000[i]

    if x != None:
        theColor = colorDefiner(c)
        matplotlib.pyplot.plot(x, y, 's', color=theColor, mec='None', mfc=theColor, ms=8, mew=1)

matplotlib.pyplot.xlim(0,9)
matplotlib.pyplot.xlabel('Max Growth Time Lag (day)')


matplotlib.pyplot.ylabel('Max Growth (cells x 1e5/day)')
matplotlib.pyplot.yticks((0, 2e5, 4e5, 6e5, 8e5, 10e5, 12e5),('0','2','4','6','8','10','12'))
matplotlib.pyplot.ylim(0,12e5)

matplotlib.pyplot.plot(-1,-1,'o', color='black', mec='None', mfc='black', ms=8, mew=1,label='300 ppm')
matplotlib.pyplot.plot(-1,-1,'s', color='black', mec='None', mfc='black', ms=8, mew=1,label='1,000 ppm')
matplotlib.pyplot.legend(loc=1,frameon=False,numpoints=1)
matplotlib.pyplot.text(2.5,8e5,'0.0 r.u. UV',color='blue')
matplotlib.pyplot.text(3,3e5,'0.5 r.u. UV',color='green')
matplotlib.pyplot.text(6.8,3e5,'1.0 r.u. UV',color='orange')

print 'message 3'

matplotlib.pyplot.savefig(figureFile)

print '... graphs completed.'
