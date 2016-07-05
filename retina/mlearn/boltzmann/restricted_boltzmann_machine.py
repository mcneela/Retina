import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

class RBM(object):
    def __init__(self, num_visible, num_hidden, learning_rate=0.05):
        """
        Initializes a new Restricted Boltzmann Machine having
        num_visible neurons in the visible layer and num_hidden
        self.num_visible = num_visible
        self.num_hidden = num_hidden
        self.learning_rate = learning_rate

        # Set the network's weight matrix to all zeros, initially
        self.weights = np.zeros(self.num_hidden, self.num_visible)  
        
        # Initialize the network's visible (binary) states
        self.visible = np.zeros(self.num_visible, 1)

        # Initialize the network's hidden (binary) states
        self.hidden = np.zeros(self.num_hidden, 1)

        # Bias weights for the visible layer
        self.visible_bias = np.random.randn(size=(self.num_visible, 1))

        # Bias weights for the hidden layer
        self.hidden_bias = np.random.randn(size=(self.num_hidden, 1))

        # Vectorize the network's activation function
        self.vectorized_activation = np.vectorize(self.activation_fn)

    def activation_fn(self, value):
        if sigmoid(value) > 0.5:
            return 1
        return 0

    def energy(self):
        """
        Returns the energy value associated with the network's current configuration.
        """
        minus_E = np.dot(self.visible_bias.T, self.visible) \
                + np.dot(self.hidden_bias.T, self.hidden) \
                + np.dot(self.hidden.T, np.multiply(self.weights, self.visible))
        return -minus_E

    def h_given_v(self):
        """
        Calculates and returns the total probability

            p(h | v)
        
        and the individual probabilities

            p(h_i | v)
        """
        prob_product = 1
        individual_probs = []
        for j in range(self.num_hidden):
            p_hj = sigmoid(self.hidden_bias[j] + np.dot(self.weights[j, :], self.visible))
            individual_probs.append(p_hj)
            prob_product *= p_hj
        return prob_product, individual_probs

    def v_given_h(self):
        """
        Calculates and returns the total probability

            p(v | h)
        
        and the individual probabilities

            p(v_i | h)
        """
        prob_product = 1
        individual_probs = []
        for k in range(self.num_visible):
            p_vk = sigmoid(self.visible_bias[k] + np.dot(self.hidden.T, self.weights[:, k]))
            individual_probs.append(p_vk)
            prob_product *= p_vk
        return prob_product, individual_probs

    def free_energy(self):
        """
        Calculates the Gibbs Free Energy value
        associated with the network's current
        configuration.
        """
        energy_sum = 0
        for j in range(self.num_hidden):
            energy_sum += 1 + np.exp(self.hidden_bias[j] + 
                                     np.dot(self.weights[j, :],
                                            self.visible))
        arg = np.dot(self.visible_bias.T, self.visible) + energy_sum
        free_energy = np.exp(arg)
        return free_energy

    def train(self, training_set, error_threshold=.08, max_epochs=500):
        """
        Trains the network on a list of training vectors passed
        as training_set. Converges either when the total sum squared
        error falls below the provided error_threshold or after
        max_epochs number of iterations of the contrastive divergence
        algorithm have been executed.
        """
        for epoch in range(max_epochs):
            total_error = 0
            for sample in training_set:
                self.visible = sample
                hidden_total_prob, hidden_individual_probs = self.h_given_v()
                self.hidden = self.vectorized_activation(hidden_individual_probs)
                positive_gradient = np.outer(self.hidden, self.visible)
                visible_total_prob, visible_individual_probs = self.v_given_h()
                self.visible = self.vectorized_activation(visible_individual_probs)
                self.negative_gradient = np.outer(self.hidden, self.visible)
                self.weights += learning_rate * (positive_gradient - negative_gradient)
                
                sample_error = np.sum(sample - visible_individual_probs)
                total_error += sample_error

            if total_error ** 2 < error_threshold:
                break





    """
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
    """
