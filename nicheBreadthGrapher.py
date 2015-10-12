### this script plots the niche breadth increase due to max growth and UV

import sys, numpy, scipy, matplotlib
import matplotlib.pyplot
import library

### MAIN

# 1. data reading
data300=library.dataReader('../data/300ppmSet3.txt')
data1000=library.dataReader('../data/1000ppmSet3.txt')

# 2. calculating the max growth rates
print 'fitting data for 300 pppm...'
maxGrowthRates300, uvValues300, growthLag300 = library.characteristicParameterFinder(data300)

print
print 'fitting data for 1,000 pppm...'
maxGrowthRates1000, uvValues1000, growthLag1000 = library.characteristicParameterFinder(data1000)

# 3. plotting
print
print 'plotting the figure...'
figureFile = '../results/figureNB.pdf'

# 300
matplotlib.pyplot.plot(uvValues300, maxGrowthRates300, 'o', color='blue', mec='blue', mfc='None', ms=8, mew=1)

slope, intercept, temp0, temp1, temp2 = scipy.stats.linregress(uvValues300, maxGrowthRates300)
y = slope*numpy.array(uvValues300) + intercept
matplotlib.pyplot.plot(uvValues300, y, color='blue', lw=1, label='300 ppm')

# 1,000
matplotlib.pyplot.plot(uvValues1000, maxGrowthRates1000, 'o', color='red', mec='red', mfc='None', ms=8, mew=1)

slope, intercept, temp0, temp1, temp2 = scipy.stats.linregress(uvValues1000, maxGrowthRates1000)
y = slope*numpy.array(uvValues1000) + intercept
matplotlib.pyplot.plot(uvValues1000, y, color='red', lw=1, label='1,000 ppm')

matplotlib.pyplot.xlim(-0.1,1.6)
matplotlib.pyplot.xlabel('UV (ru)')
matplotlib.pyplot.ylabel('max growth (cells x 1e5/day)')
matplotlib.pyplot.yticks((-2e5, 0, 2e5, 4e5, 6e5, 8e5, 10e5, 12e5),('-2','0','2','4','6','8','10','12'))
matplotlib.pyplot.legend(loc=1,frameon=False)
matplotlib.pyplot.savefig(figureFile)

print '... graphs completed.'
