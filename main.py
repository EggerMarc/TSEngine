from timeseries import *
import csv

PATH = './Data/cmort'

def run():
    values = timeseries(path = PATH, debugger = False)
    #print(values.meanN(2))
    #values.head(10)
    values.append(400)
    values.pop()

    values.visualize()
    values.transforms('Standardize')
    values.visualize()
    return

if __name__ == '__main__':
    run()

