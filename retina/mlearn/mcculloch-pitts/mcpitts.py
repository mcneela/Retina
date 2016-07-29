class MPNeuron(object):
    def __init__(self, threshold, inputs):
        self.threshold = threshold
        self.inputs = inputs

    def activate(self):
        excitations = 0 
        for trigger in self.inputs:
            if trigger.excitatory:
                excitations += trigger.value
            else:
                if trigger.value:
                    return 0
        if excitations >= self.threshold:
            return 1 
        return 0 

class MPInput(object):
    def __init__(self, excitatory):
        self.excitatory = excitatory
        self.value = 0 

    def trigger(self, value):
        self.value = value 

class Decoder(object):
    def __init__(self, vectors):
        self.vectors = vectors
        self.vec_length = len(self.vectors[0])
        assert(len(vec) == self.vec_length for vec in vectors)

    def decode(self):
        decoder_units = []
        for vector in self.vectors:
            threshold = sum(vector)
            inputs = []
            for i in range(self.vec_length):
                if vector[i] == 1:
                    inputs.append(MPInput(True))
                else:
                    inputs.append(MPInput(False))
            gate = MPNeuron(threshold, inputs)
            decoder_units.append(gate)
        
        def decoder(*args):
            for i in range(self.vec_length):
                inputs[i].trigger(args[i])
            decoder_units.reverse()
            or_arg = decoder_units[0].activate()
            for unit in decoder_units:
                for i in range(self.vec_length):
                    unit.inputs[i].trigger(args[i])
                val = unit.activate()
                or_arg = OR(or_arg, val)
            return or_arg

        return decoder

def AND(x1, x2):
    inputs = [MPInput(True), MPInput(True)]
    gate = MPNeuron(2, inputs)
    inputs[0].trigger(x1)
    inputs[1].trigger(x2)
    return gate.activate()

def OR(x1, x2):
    inputs = [MPInput(True), MPInput(True)]
    gate = MPNeuron(1, inputs)
    inputs[0].trigger(x1)
    inputs[1].trigger(x2)
    return gate.activate()

def NOT(x):
    inputs = [MPInput(False)]
    gate = MPNeuron(0, inputs)
    inputs[0].trigger(x)
    return gate.activate()

def XOR(x1, x2):
    return AND(OR(x1, x2), 
               NOT(AND(x1, x2)))
