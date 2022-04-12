#TODO: Kurtosis, KurtosisN, MedianN, 

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
    
    def getShape(self):
        return self.observations.shape
    
    def pop(self):
        popped = self.observations[-1]
        self.setObservations(self.observations[:-1])
        if self.debugger == True:
            print(f"After pop type: {type(popped)}")
        return numpy.array(popped)

    def append(self, x):
        if self.debugger == True:
            #The shapes of an input e.g. [1,1,1] is (1,3), whereas the last observation on 3 cols is (3,)
            #This solution allows for more than one column per append. It simply has to be a matrix of the
            #same column size.
            print(f"x shape: {numpy.array([x]).shape[-1]} \nData[-1] shape: {self.observations[-1].shape[0]}")
        assert numpy.array([x]).shape[-1] == self.observations[-1].shape[0], 'Incompatible shape'
        _temp = self.observations.tolist()
        _temp.append([x])
        self.setObservations(numpy.array(_temp))
        pass
    
    def setObservations(self, x):
        assert type(x) == numpy.ndarray, 'Not a numpy array'
        self.observations = numpy.array(x, dtype=ndarray)
        #Below is deprecated
        #self.observations = numpy.array([numpy.array(n) for n in x]) #This is probably not very efficient for large observations. Will need to research how to numpyify inner arrays
        if self.debugger == True:
            print(f"Set type to: {type(self.observations)}\nRow types:{[type(n) for n in self.observations]}")
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
            plt.plot(self.difference)
            plt.show()

    def meanN(self, N):
        if self.debugger == True:
            print(self.observations[-N:].T)
        return self.observations[-N:].T.mean(axis = 1).T
    
    def stdN(self, N):
        return self.observations[-N:].T.std(axis = 1).T

    def median(self):
        return self.observations.T.median(axis = 1).T

    def medianN(self, N):
        return self.observations[-N:].T.median(axis = 1).T

    
    def transforms(self, transformName: str, lmb = 0):
        if transformName == 'Box-Cox':
            self.boxCox(lmb)
            return self
        elif transformName == 'Custom':
            self.customTransform()
            return self
        elif transformName == 'Standardize':
            self.standardize()
            return self
        elif transformName == 'Normalize':
            self.normalize()
            return self

        else:
            print('Undefined transformation.')

    def normalize(self):
        _temp = self.observations.T
        flag = 0
        for n in _temp:
            try:
                n = numpy.array(n, dtype=float)
                _temp[flag] = (n - n.min()) / (n.max() - n.min())
            except AttributeError:
                continue
            flag += 1

        if self.debugger == True:
            print(f"Post transform: {_temp.T}")
        self.setObservations(_temp.T)
        return self

    def boxCox(self, lmb):
        _temp = self.observations.T
        flag = 0
        for n in _temp:
            if self.debugger == True:
                print(f"n: {numpy.array(n).dtype}")
            try:
                n = numpy.array(n, dtype=float)
                if lmb[flag] == 0:
                    _temp[flag] = numpy.log(n)
                else:
                    _temp[flag] = (n**lmb[flag] - 1) / lmb[flag]
            except AttributeError:
                continue
            flag += 1
        if self.debugger == True:
            print(f"Post transform: {_temp.T}")
        self.setObservations(_temp.T)
        return self

    def standardize(self):
        _temp = numpy.array(self.observations.T)
        flag = 0
        for n in _temp:
            try:
                n = numpy.array(n, dtype=float)
                _temp[flag] = (n - n.mean()) / n.std()
            except AttributeError:
                continue
            flag += 1

        if self.debugger == True:
            print(f"Post transform: {_temp.T}")
        self.setObservations(_temp.T)
        pass

    def difference(self):
        _temp = numpy.insert(self.observations, 0, numpy.zeros(self.observations.shape[1]), axis = 0)[:-1]

        self.difference = (self.observations - _temp)[1:]
        
        if self.debugger == True:
            print(f"Difference shape: {self.difference.shape}")
        return self.difference
    
    def autocorrelation(self, lag: int = 1):
        self.autoArray = numpy.zeros(self.observations.shape[1])

        _temp = numpy.array(self.observations)
        _tempt = self.observations.T

        for l in range(lag): #Could get rid of l, but a while loop damages lag 
                             #and I don't want to instantiate a new var outside the scope of the loop for this
            _temp = numpy.insert(_temp, 0, numpy.zeros(self.observations.shape[1]), axis = 0)[:-1]
        
        _temp = _temp.T

        mean = _tempt.mean(axis = 1)
        for n in range(0,self.observations.shape[1]):
            #Categorical handler still not implemented. 
            self.autoArray[n] += (_temp[n][lag:] - mean[n])@(_tempt[n][lag:] - mean[n]) / ((_temp[n][lag:] - mean[n])@(_temp[n][lag:] - mean[n]))

        return self.autoArray

    def customTransform(self):
        pass

    def kurtosis(self):
        return

    def kurtosisN(self):
        return

    def moment(self):

        return _moment