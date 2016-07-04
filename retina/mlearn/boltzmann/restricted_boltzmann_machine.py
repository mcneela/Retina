import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

class RBM(object):
    def __init__(self, num_visible, num_hidden):
        self.num_visible = num_visible
        self.num_hidden = num_hidden

        # Set the network's weight matrix to all zeros, initially
        self.weights = np.zeros(self.num_visible, self.num_hidden)  
        
        # Initialize the network's visible (binary) states
        self.visible = np.zeros(self.num_visible, 1)

        # Initialize the network's hidden (binary) states
        self.hidden = np.zeros(self.num_hidden, 1)

        # Bias weights for the visible layer
        self.visible_bias = np.random.bernoulli(size=(self.num_visible, 1))

        # Bias weights for the hidden layer
        self.hidden_bias = np.random.bernoulli(size=(self.num_hidden, 1))

    def energy(self):
        E = -np.dot(self.visible_bias.T, self.visible) \
            -np.dot(self.hidden_bias.T, self.hidden) \
            -np.dot(self.visible.T, np.multiply(self.weights, self.hidden))
        return E

    def v_cond_h(self):
        visible = []
        for i in range(self.num_visible):
            arg = self.visible[i] + np.dot(self.hidden, self.weights[i, :])
            visible.append(sigmoid(arg))
        return visible

    def h_cond_v(self):
        hidden = []
        for j in range(self.num_hidden):
            arg = self.hidden[j] + np.dot(self.visible, self.weights[:, j])
            hidden.append(sigmoid(arg))
        return hidden

    def gibbs_sampling(self, num_iters):
        for iter_num in num_iters:
            self.hidden = self.h_cond_v()
            self.visible = self.v_cond_h()
    

        
