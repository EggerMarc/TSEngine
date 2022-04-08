from timeseries import *
import csv

PATH = './Data/cmort'

def run():
    values = timeseries(path = PATH, debugger = False)
    #print(values.meanN(2))
    #values.head(10)
    values.append(numpy.NaN)
    values.pop()

    values.visualize()
    values.transforms('Box-Cox', [4,2])
    values.visualize()
    return

if __name__ == '__main__':
    run()

