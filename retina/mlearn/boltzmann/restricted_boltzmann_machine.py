import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

class RBM(object):
    def __init__(self, num_visible, num_hidden):
        self.num_visible = num_visible
        self.num_hidden = num_hidden
        self.weights = np.zeros(self.num_visible, self.num_hidden)  
        
        # Bias weights for the visible layer
        self.a = np.random.logistic(size=(1, self.num_visible))

        # Bias weights for the hidden layer
        self.b = np.random.logistic(size=(1, self.num_hidden))

    def energy(self):
        E = -np.dot(a.T, 
