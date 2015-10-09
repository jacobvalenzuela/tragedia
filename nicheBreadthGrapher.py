### this script plots the niche breadth increase due to max growth and UV

import sys, numpy, scipy, matplotlib
import matplotlib.pyplot
import library

def maxGrowthCalculator(dataStructure):

    resolution = 1000
    maxGrowthRates = []
    uvValues = []

    for epocLabel in dataStructure:

        epoc=epocLabel.split('_')[0]
        uvValue=float(epoc)

        print epocLabel,
                
        localTime=numpy.array(dataStructure[epocLabel][0])
        shiftedTime=localTime-min(localTime)
        localCells=dataStructure[epocLabel][1]
        highResolutionTime=numpy.linspace(min(shiftedTime),max(shiftedTime),resolution)

        # if there are two values, give the difference
        if len(localCells) == 2:
            maxGrowthRate=(localCells[1]-localCells[0])/(localTime[-1]-localTime[0])
            print 'calculating max growth rate based on two values',maxGrowthRate

        # if the last value is lower than the first, provide with the slope of a regression
        elif localCells[0] > localCells[-1]:
            slope, intercept, temp0, temp1, temp2 = scipy.stats.linregress(shiftedTime,localCells)
            maxGrowthRate=slope
            print 'calculating max growth rate based on a decreasing time series',maxGrowthRate

        # calculate the fitted and the manual max growth. Give the manual if the difference is larger than 5 percent
        else:
            fittedTrajectory = library.dataFitter(shiftedTime,localCells)
            fittedMaxGrowthRate = fittedTrajectory[0][1]
            
            manualMaxGrowthRate = library.manualGrowthCalculator(shiftedTime, localCells)

            ratio = fittedMaxGrowthRate/manualMaxGrowthRate
            if ratio > 2.:
                maxGrowthRate = manualMaxGrowthRate
                print 'correcting max growth rate to point differences based on large discrepancies.\n'
            else:
                maxGrowthRate = fittedMaxGrowthRate
                            
        #print
        uvValues.append(uvValue)
        maxGrowthRates.append(maxGrowthRate)
 
    return maxGrowthRates,uvValues

### MAIN

# 1. data reading
data300=library.dataReader('../data/300ppmSet3.txt')
data1000=library.dataReader('../data/1000ppmSet3.txt')

# 2. calculating the max growth rates
print 'fitting data for 300 pppm...'
maxGrowthRates300,uvValues300=maxGrowthCalculator(data300)

print
print 'fitting data for 1,000 pppm...'
maxGrowthRates1000,uvValues1000=maxGrowthCalculator(data1000)

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
