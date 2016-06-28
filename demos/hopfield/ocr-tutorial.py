from retina.mlearn.hopfield.alphabet import *
import retina.mlearn.hopfield.visuals as visuals
import numpy as np

def to_state(letter):
    return np.array([1 if char == 'X' else -1 for char in letter.replace('\n','')])

myNet = visuals.VisualHopfield(25)
alphabet = [A, B, C, D, E, F, G, H, I, J, K, L, M, 
        N, O, P, Q, R, S, T, U, V, W, X, Y, Z]
training_data = [to_state(B), to_state(I)]
shift_I = """
XXXXX
...X.
...X.
...X.
XXXXX
"""
learning_data = [to_state(shift_I)]
myNet.run_visualization(training_data, learning_data)
