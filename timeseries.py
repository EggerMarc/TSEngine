#TODO: Kurtosis, KurtosisN, MedianN, Transforms (Box-Cox)
from distutils.log import debug
from header import *

class timeseries:
    def __init__(self, observations = None, measures = None, path: str = None, debugger = False):
        self.debugger = debugger
        if path != None:
            self.observations = numpy.array(pandas.read_csv(path, sep = ',', index_col=0))
            if debugger == True:
                print(f"Imported from: {path}")
        else:
            self.observations = observations

        self.measures = measures
        self.path = path
    
    def getObservations(self):
        return self.observations
    
    def pop(self):
        popped = self.observations[-1]
        self.setObservations(self.observations[:-1])
        return popped

    def append(self, x):
        if self.debugger == True:
            print(f"x shape: {numpy.array([x]).shape} \nData[-1] shape: {self.observations[-1].shape}")
        assert numpy.array([x]).shape == self.observations[-1].shape, 'Incompatible shape'
        temp = self.observations.tolist()
        temp.append([x])
        self.setObservations(numpy.array(temp))
        pass
    
    def setObservations(self, x):
        assert type(x) == numpy.ndarray, 'Not a numpy array'
        self.observations = x
        pass

    def head(self, N = 5):
        print(self.observations[:N])
        return self.observations[:N]

    def mean(self):
        return self.observations.mean(axis = 1)

    def std(self):
        return self.observations.std(axis = 1)

    def visualize(self): #Temporary use, just to ease
        if self.debugger == True:
            print(f"TS Shape: {self.observations.shape}")

        if len(self.observations.shape) > 2:
            flag = 0
            for obs in self.observations:
                plt.subplot(flag)
                plt.plot(obs)
        
        else:
            plt.figure()
            plt.plot(self.observations)
            plt.show()

    def meanN(self, N):
        if self.debugger == True:
            print(self.observations[:N].T)
        return self.observations[:N].T.mean(axis = 1).T
    
    def stdN(self, N):
        return self.observations[:N].T.std(axis = 1).T

    def median(self):
        return self.observations.T.median(axis = 1).T

    def medianN(self, N):
        return self.observations[:N].T.median(axis = 1).T

    
    def transforms(self, transformName: str, lmb = 0):
        
        match transformName:
            case 'Box-Cox':
                self.boxCox(lmb)
            case 'Custom':
                self.customTransform()
            case 'Standardize':
                self.standardize()
            case 'Normalize':
                self.normalize()
        pass

    def normalize(self):
        _temp = self.observations.T
        flag = 0
        for n in _temp:
            _temp[flag] = (n - n.min()) / (n.max() - n.min())
            flag += 1

        if self.debugger == True:
            print(f"Post transform: {_temp.T}")
        self.setObservations(_temp.T)
        pass

    def boxCox(self, lmb):
        _temp = self.observations.T
        if lmb == 0:
            _temp = numpy.log(_temp)
        else:
            _temp = (_temp**lmb - 1) / lmb
        if self.debugger == True:
            print(f"Post transform: {_temp.T}")
        self.setObservations(_temp.T)
        pass

    def standardize(self):
        _temp = self.observations.T
        flag = 0
        for n in _temp:
            _temp[flag] = (n - n.mean()) / n.std()
            flag += 1

        if self.debugger == True:
            print(f"Post transform: {_temp.T}")
        self.setObservations(_temp.T)
        pass

    def customTransform(self):
        pass

    def kurtosis(self):
        return

    def kurtosisN(self):
        return