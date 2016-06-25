from retina.mlearn.hopfield.alphabet import *
import retina.mlearn.hopfield.visuals as visuals
import numpy as np
from pylab import *

def to_state(letter):
    return array([1 if char == 'X' else -1 for char in letter.replace('\n','')])

def show_state(state):
    state = state.reshape((5, 5))
    imshow(state, cmap=cm.binary, interpolation='nearest')
    show()

myNet = visuals.VisualHopfield(25)
alphabet = [A, B, C, D, E, F, G, H, I, J, K, L, M, 
        N, O, P, Q, R, S, T, U, V, W, X, Y, Z]
training_data = [to_state(letter) for letter in alphabet]
learning_data = [to_state(l1)]
myNet.run_visualization(training_data, learning_data)
