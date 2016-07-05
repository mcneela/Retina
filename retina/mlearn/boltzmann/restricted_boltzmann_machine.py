import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

class RBM(object):
    def __init__(self, num_visible, num_hidden, learning_rate=0.05):
        """
        Initializes a new Restricted Boltzmann Machine having
        num_visible neurons in the visible layer and num_hidden
        neurons in the hidden layer. By default, the learning
        rate is set to 0.05, but this can be altered to adjust
        the speed (and granularity) of training adjustments.
        """
        self.num_visible = num_visible
        self.num_hidden = num_hidden
        self.learning_rate = learning_rate

        # Set the network's weight matrix to all zeros, initially
        self.weights = np.zeros((self.num_hidden, self.num_visible))  
        
        # Initialize the network's visible (binary) states
        self.visible = np.zeros((self.num_visible, 1))

        # Initialize the network's hidden (binary) states
        self.hidden = np.zeros((self.num_hidden, 1))

        # Bias weights for the visible layer
        self.visible_bias = np.random.randn(self.num_visible)

        # Bias weights for the hidden layer
        self.hidden_bias = np.random.randn(self.num_hidden, 1)
        print(self.hidden_bias)
        # Vectorize the network's activation function
        self.vectorized_activation = np.vectorize(self.activation_fn)

        # Vectorize the boolean activation function
        self.vec_bool_activation = np.vectorize(self.bool_activation)

    def activation_fn(self, value):
        if sigmoid(value) > 0.5:
            return 1
        return 0

    def bool_activation(self, value):
        if value is True:
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
        return prob_product, np.array(individual_probs)

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
        return prob_product, np.array(individual_probs)

    def gen_v_given_h(self, hidden):
        """
        Does the same thing as v_given_h except
        in this case the hidden layer is passed
        as an argument rather than generated from
        the internal hidden layer.
        """
        prob_product = 1
        individual_probs = []
        for k in range(self.num_visible):
            p_vk = sigmoid(self.visible_bias[k] + np.dot(hidden.T, self.weights[:, k]))
            individual_probs.append(p_vk)
            prob_product *= p_vk
        return prob_product, np.array(individual_probs)

    def gen_h_given_v(self, visible):
        """
        Does the same thing as h_given_v except
        in this case the visible layer is passed
        as an argument rather than generated from
        the internal visible layer.
        """
        prob_product = 1
        individual_probs = []
        for j in range(self.num_hidden):
            p_hj = sigmoid(self.hidden_bias[j] + np.dot(self.weights[j, :], visible))
            individual_probs.append(p_hj)
            prob_product *= p_hj
        return prob_product, np.array(individual_probs)
    
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
                self.visible = np.array(sample).T
                hidden_total_prob, hidden_individual_probs = self.h_given_v()
                self.hidden = self.vectorized_activation(hidden_individual_probs)
                positive_gradient = np.outer(self.hidden, self.visible)
                visible_total_prob, visible_individual_probs = self.v_given_h()
                self.visible = self.vectorized_activation(visible_individual_probs).T
                negative_gradient = np.outer(self.hidden, self.visible)
                self.weights += self.learning_rate * (positive_gradient - negative_gradient)
                
                sample_error = np.sum(sample - visible_individual_probs)
                total_error += sample_error ** 2

                self.hbias_arg = np.dot(sample, self.hidden_bias)[0]
                hbias_probs = [sigmoid(self.hbias_arg) for i in range(self.num_hidden)]
                self.hidden_bias = self.vec_bool_activation(hbias_probs > np.random.randn(self.num_hidden))
                self.hidden_bias = self.hidden_bias.reshape((self.num_hidden, 1))

                self.vbias_arg = np.dot(self.visible_bias, self.hidden_bias)[0]
                vbias_probs = np.array([sigmoid(self.vbias_arg) for j in range(self.num_visible)])
                self.visible_bias = self.vec_bool_activation(vbias_probs > np.random.randn(self.num_visible))
                
            if total_error < error_threshold:
                break

    def generate_visible(self, hidden_samples):
        """
        Assuming the network's been trained, given a list of hidden states,
        return the set of visible states generated by those layers.
        """
        visible_states = []
        for hidden_vec in hidden_samples:
            hidden_vec = np.array(hidden_vec)
            prob, visible_probs = self.gen_v_given_h(hidden_vec)
            visible = self.vectorized_activation(visible_probs)
            visible_states.append(visible)
        return visible_states

    def generate_hidden(self, visible_samples):
        """
        Assuming the network's been trained, given a list of visible states,
        return the set of hidden states generated by those layers.
        """
        hidden_states = []
        for visible_vec in visible_samples:
            visible_vec = np.array(visible_vec)
            prob, hidden_probs = self.gen_h_given_v(visible_vec)
            hidden = self.vectorized_activation(hidden_probs)
            hidden_states.append(hidden)
        return hidden_states
