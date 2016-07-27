class MPNeuron:
    def __init__(self, threshold, num_excite, num_inhib):
        self.threshold = threshold
        self.num_excite = num_excite
        self.num_inhib = num_inhib

    def activate(self, excites, inhibs):
        assert(len(excites) == self.num_excite and
               len(inhibs) == self.num_inhib)
        return sum(excites) >= self.threshold and (not sum(inhibs)) 

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
