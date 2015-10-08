import sys,numpy,matplotlib
import matplotlib.pyplot, scipy.stats
import library

def dataGrapherEpocs(dataStructure,figureLabel):

    resolution=1000
    figureFile='../results/figure_%s.pdf'%figureLabel
    legendWritten=False

    if figureLabel == '300':
        localColor='blue'
    elif figureLabel == '1000':
        localColor='red'
    else:
        print 'error a'
        sys.exit()

    for epocLabel in dataStructure:


        epoc=epocLabel.split('_')[0]
        
        localTime=numpy.array(dataStructure[epocLabel][0])
        shiftedTime=localTime-min(localTime)
        localCells=dataStructure[epocLabel][1]
        highResolutionTime=numpy.linspace(min(shiftedTime),max(shiftedTime),resolution)

        # plotting the data
        if legendWritten == False:
            matplotlib.pyplot.plot(localTime,localCells,'o',color=localColor,markeredgecolor='None',label='%s ppm'%figureLabel)
            legendWritten=True
        else:
            matplotlib.pyplot.plot(localTime,localCells,'o',color=localColor,markeredgecolor='None')

        # plotting the model if there is growth, otherwise plot a best model straight line
        if len(localCells) == 2:
            matplotlib.pyplot.plot([localTime[0],localTime[-1]],[localCells[0],localCells[-1]],'-',color=localColor)
        elif localCells[0] > localCells[-1]:
            slope, intercept, temp0, temp1, temp2 = scipy.stats.linregress(shiftedTime,localCells)
            matplotlib.pyplot.plot([localTime[0],localTime[-1]],[intercept,slope*shiftedTime[-1]+intercept],'-',color=localColor)
        else:
            fittedTrajectory=library.dataFitter(shiftedTime,localCells)
            b=library.peval(highResolutionTime,fittedTrajectory[0])
            matplotlib.pyplot.plot(highResolutionTime+min(localTime),b,'-',color=localColor)
    
    matplotlib.pyplot.xlim([-0.5,19])
    matplotlib.pyplot.ylim([-0.5e5,10e5])
    matplotlib.pyplot.xlabel('time (days)')
    matplotlib.pyplot.ylabel('number of cells (x 1e5)')
    matplotlib.pyplot.yticks((0,1e5,2e5,3e5,4e5,5e5,6e5,7e5,8e5,9e5,10e5),('0','1','2','3','4','5','6','7','8','9','10'))

    matplotlib.pyplot.legend(numpoints=1,loc=1,frameon=False)
    
    matplotlib.pyplot.savefig(figureFile)
    matplotlib.pyplot.clf()


    return None

### MAIN

# 1. data reading
data300=library.dataReader('../data/300ppmSet3.txt')
data1000=library.dataReader('../data/1000ppmSet3.txt')

# 2. fitting the data to sigmoidal function
print 'fitting data for 300 pppm...'
dataGrapherEpocs(data300,'300')

print
print 'fitting data for 1000 ppm...'
dataGrapherEpocs(data1000,'1000')

print '... graphs completed.'
