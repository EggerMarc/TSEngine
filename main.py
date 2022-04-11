from timeseries import *
import csv

PATH = './Data/cmort'

def run():
    xx = numpy.random.rand(10,3)
    values = timeseries(observations=xx, debugger = False)

    
    #print(values.meanN(2))
    #values.head(10)
    #values.append(numpy.array([2,2,2]))
    #values.pop()

    values.setObservations(xx)

    #values.visualize()
    values.transforms('Box-Cox', [10000,1,1])
    #print(values.getObservations())
    #print(values.autocorrelation(lag  = 5))
    print(values.difference())
    #values.visualize()
    return

if __name__ == '__main__':
    run()

