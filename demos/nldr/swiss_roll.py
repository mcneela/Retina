"""
===================================
Swiss Roll reduction with LLE
===================================

An illustration of Swiss Roll reduction
with locally linear embedding
"""

# Author: Fabian Pedregosa -- <fabian.pedregosa@inria.fr>
# License: BSD 3 clause (C) INRIA 2011

print(__doc__)

from mapping import *
import matplotlib.pyplot as plt

# This import is needed to modify the way figure behaves
from mpl_toolkits.mplot3d import Axes3D
Axes3D

#----------------------------------------------------------------------
# Locally linear embedding of the swiss roll

from sklearn import manifold, datasets
X, color = datasets.samples_generator.make_swiss_roll(n_samples=1500)
print(X)
print("Computing LLE embedding")
X_r, err = manifold.locally_linear_embedding(X, n_neighbors=12,
                                             n_components=2)
print("Done. Reconstruction error: %g" % err)

#----------------------------------------------------------------------
# Plot result

fig = plt.figure()
try:
    # compatibility matplotlib < 1.0
    ax = fig.add_subplot(611, projection='3d')
    ax.scatter(X[:, 0], X[:, 1], X[:, 2], c=color, cmap=plt.cm.Spectral)
except:
    ax = fig.add_subplot(611)
    ax.scatter(X[:, 0], X[:, 2], c=color, cmap=plt.cm.Spectral)

ax.set_title("Original data")
num_sections = 5
sections = section(X, num_sections, axis='z')
print(sections)
for i, sec in zip(range(num_sections), sections):
    ax = fig.add_subplot(612 + i)
    X_r, err = manifold.locally_linear_embedding(sec, n_neighbors=12,
                                                 n_components=2)
    ax.scatter(X_r[:, 0], X_r[:, 1], c='r', cmap=plt.cm.Spectral)
#ax = fig.add_subplot(212)
#ax.scatter(X_r[:, 0], X_r[:, 1], c=color, cmap=plt.cm.Spectral)
plt.axis('tight')
plt.xticks([]), plt.yticks([])
plt.title('Projected data')
plt.show()

