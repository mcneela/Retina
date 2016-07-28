class MPNeuron(object):
    def __init__(self, threshold, num_excite, num_inhib):
        self.threshold = threshold
        self.num_excite = num_excite
        self.num_inhib = num_inhib

    def activate(self, excites, inhibs):
        assert(len(excites) == self.num_excite and
               len(inhibs) == self.num_inhib)
        return sum(excites) >= self.threshold and (not sum(inhibs)) 

class Decoder(object):
    def __init__(self, vectors):
        self.vectors = vectors
        self.vec_length = len(self.vectors[0])
        assert(len(vec) == self.vec_length for vec in vectors)

    def decode(self):
        decoder_units = []
        for vector in self.vectors:
            threshold = sum(vector)
            num_excites = threshold
            num_inhibs = len(vector) - num_excites
            gate = MPNeuron(threshold, num_excites, num_inhibs)
            decoder_units.append(gate)
        
        gen_func = lambda *args: args
        for neuron in decoder_units:
            gen_func = lambda *args: OR(gen_func(*args), neuron.activate)

        return gen_func

def AND(x1, x2):
    gate = MPNeuron(2, 2, 0)
    return gate.activate([x1, x2], [])

def OR(x1, x2):
    gate = MPNeuron(1, 2, 0)
    return gate.activate([x1, x2], [])

def NOT(x):
    gate = MPNeuron(0, 0, 1)
    return gate.activate([], [x])

def XOR(x1, x2):
    return AND(OR(x1, x2), 
               NOT(AND(x1, x2)))
