import matplotlib.pyplot as plt
import retina.core.axes
import numpy as np
from itertools import product, combinations

fig = plt.figure(figsize=(20, 20))
ax = plt.subplot('111', projection='Fovea3D')
#x = [0, 0, 0, 0, 1, 1, 1, 1]
#y = [0, 1, 0, 1, 0, 1, 0, 1]
#z = [0, 0, 1, 1, 0, 0, 1, 1]

r = [-1, 1]
for s, e in combinations(np.array(list(product(r, r, r))), 2):
    if np.sum(np.abs(s - e)) == r[1] - r[0]:
        ax.plot(*zip(s, e), color='b')
