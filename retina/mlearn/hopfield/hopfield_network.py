import numpy as np
import random

class HopfieldNetwork:
    """
    (C) Daniel McNeela, 2016

    Implements the Hopfield Network, a recurrent neural network developed by John Hopfield
    circa 1982.

    c.f. https://en.wikipedia.org/wiki/Hopfield_Network
    """
    def __init__(self, num_neurons, activation_fn=None):
        """
        Instantiates a Hopfield Network comprised of "num_neurons" neurons.
        
        num_neurons         The number of neurons in the network.
        _weights            The network's weight matrix.
        _trainers           A dictionary containing the methods available for 
                            training the network.
        _vec_activation     A vectorized version of the network's activation function.
        """
        self.num_neurons = num_neurons
        self._weights = np.zeros((self.num_neurons, self.num_neurons), dtype=np.int_)
        self._trainers = {"hebbian": self._hebbian, "storkey": self._storkey}
        self._learn_modes = {"synchronous": self._synchronous, "asynchronous": self._asynchronous}
        self._vec_activation = np.vectorize(self._activation)
        self._train_act = np.vectorize(self._train_activation)

    def weights(self):
        """
        Getter method for the network's weight matrix.
        """
        return self._weights

    def reset(self):
        """
        Resets the network's weight matrix to the matrix which is identically zero.

        Useful for retraining the network from scratch after an initial round
        of training has already been completed.
        """
        self._weights = np.zeros((self.num_neurons, self.num_neurons), dtype=np.int_)

    def train(self, patterns, method="hebbian", threshold=0, inject = lambda x, y: None):
        """
        The wrapper method for the network's various training algorithms stored in
        self._trainers.

        patterns        A list of the on which to train the network. Patterns are
                        bipolar vectors of the form 

                        [random.choice([-1, 1]) for i in range(self.num_neurons)].

                        Example of properly formatted input for a Hopfield Network
                        containing three neurons:

                            [[-1, 1, 1], [1, -1, 1]]

        method          The training algorithm to be used. Defaults to "hebbian".
                        Look to self._trainers for a list of the available options.
        threshold       The threshold value for the network's activation function.
                        Defaults to 0.
        """
        try:
            return self._trainers[method](patterns, threshold, inject)
        except KeyError:
            print(method + " is not a valid training method.")

    def learn(self, patterns, steps=None, mode="asynchronous", inject = lambda x: None):
        """
        Wrapper method for self._synchronous and self._asynchronous.

        To be used after training the network.

        patterns        The input vectors to learn

        steps           Number of steps to compute. Defaults to None.

        Given 'patterns', learn(patterns) classifies these patterns based on those
        which the network has already seen.
        """
        try:
            return self._learn_modes[mode](patterns, steps, inject)
        except KeyError:
            print(mode + " is not a valid learning mode.")

    def energy(self, state):
        """
        Returns the energy for any input to the network.
        """
        return -0.5 * np.sum(np.multiply(np.outer(state, state), self._weights))

    def _synchronous(self, patterns, steps=10):
        """
        Updates all network neurons simultaneously during each iteration of the
        learning process.

        Faster than asynchronous updating, but convergence of the learning method
        is not guaranteed.
        """
        if steps:
            for i in range(steps):
                patterns = np.dot(patterns, self._weights)
            return self._vec_activation(patterns)
        else:
            while True:
                post_learn = self._vec_activation(np.dot(patterns, self._weights))
                if np.array_equal(patterns, post_learn):
                    return self._vec_activation(post_learn)
                patterns = post_learn

    def _asynchronous(self, patterns, steps=None, inject=lambda x:None):
        """
        Updates a single, randomly selected neuron during each iteration of the learning
        process.

        Convergence is guaranteed, but the learning is slower than when neurons are updated
        in synchrony.
        """
        patterns = np.array(patterns)
        if steps:
            for i in range(steps):
                index = random.randrange(self.num_neurons)
                patterns[:,index] = np.dot(self._weights[index,:], np.transpose(patterns))
            return self._vec_activation(patterns)
        else:
            post_learn = patterns.copy()
            inject(post_learn, 0)
            indicies = set()
            i = 1
            while True:
                index = random.randrange(self.num_neurons)
                indicies.add(index)
                post_learn[:,index] = np.dot(self._weights[index,:], np.transpose(patterns))
                post_learn = self._vec_activation(post_learn)
                inject(post_learn, i)
                if np.array_equal(patterns, post_learn) and len(indicies) == self.num_neurons:
                    return self._vec_activation(post_learn)
                patterns = post_learn.copy()
                i += 1

    def _activation(self, value, threshold=0):
        """
        The network's activation function.

        Defaults to the sign function.
        """
        if value < threshold:
            return -1
        return 1

    def _train_activation(self, value, threshold=0):
        if value == threshold:
            return value
        elif value < threshold:
            return -1
        return 1

    def _hebbian(self, patterns, threshold=0, inject= lambda x, y: None):
        """
        Implements Hebbian learning.
        """
        i = 1
        for pattern in patterns:
            prev = self._weights.copy()
            self._weights += np.outer(pattern, pattern)
            inject(prev, i)
            i += 1
        np.fill_diagonal(self._weights, 0)
        self._weights = self._weights / len(patterns)

    def _storkey(self, patterns):
        """
        Implements Storkey learning.
        """
        pass
