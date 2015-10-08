import scipy,numpy
from scipy.optimize import leastsq
from scipy.stats import linregress

def dataReader(inputFile):

    dataStructure={} # this dictionary has a label for each epoc. For each epoc you will have a list of two lists for time and number of cells

    with open(inputFile,'r') as f:
        # formating the excell format
        data=f.readlines()
        lines=data[0].split('\r')

        for line in lines:
            vector=line.split('\t')
            if vector[1] != 'Hours':
                
                epoc=vector[0]
                time=float(vector[1])/24.
                cells=float(vector[2])
                
                # filling up the variable
                if epoc not in dataStructure:
                    dataStructure[epoc]=[[time],[cells]]
                else:
                    dataStructure[epoc][0].append(time)
                    dataStructure[epoc][1].append(cells)

    return dataStructure

def dataFitter(time,values):

    p0 = [1e6, 1e5, 1e0, 50e3]
    fitted = scipy.optimize.leastsq(residuals,p0,args=(values,time),maxfev=int(1e9),ftol=1e-20)

    print fitted[0]

    return fitted

def logistic(x, A, B, C, D):
    
    """
    modification of the  logistic equation from grofit, journal of statistical software 2010
    A is the carrying capacity
    B, or mu is the max growth rate
    C, or lambda, length of the lag phase
    D, extra parameter, not for the publication, to account for extra flexibility at t=0
    """
    
    num=A
    expfun=numpy.exp(4*B/A*(C-x)+2)
    deno=1+expfun
    
    return D+num/deno

def peval(x, p):
    """Evaluated value at x with current parameters."""

    A,B,C,D = p

    return logistic(x, A, B, C, D)

def residuals(p, y, x):
    """Deviations of data from fitted 4PL curve"""

    A,B,C,D = p
    err = y-logistic(x, A, B, C, D)

    return err
