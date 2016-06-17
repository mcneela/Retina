"""
Adopted from the swiss_roll.py example
packaged with Scikit-Learn.
"""
import mapping
import matplotlib.pyplot as plt
import retina.core.axes
from matplotlib import gridspec
from sklearn import manifold, datasets

X, color = datasets.samples_generator.make_swiss_roll(n_samples=1500)
print("Computing LLE embedding")
X_r, err = manifold.locally_linear_embedding(X, n_neighbors=12,
                                             n_components=2)
print("Done. Reconstruction error: %g" % err)

fig = plt.figure(figsize=(20, 20))
gs = gridspec.GridSpec(2, 3)
nld = plt.subplot(gs[0,0], projection='Fovea3D')
roll = nld.add_layer('roll')
roll.add_data(X[:, 0], X[:, 1], X[:, 2])
nld.build_layer('roll', plot=nld.scatter, c=color, cmap=plt.cm.Spectral)
nld.set_title("Original data")

num_sections = 5
sections = mapping.section(X, num_sections, axis='z')
for i, j, sec in zip([0, 0, 1, 1, 1], range(num_sections), sections):
    ax = plt.subplot(gs[i, (j + 1) % 3], projection='Fovea2D')
    X_r, err = manifold.locally_linear_embedding(sec, n_neighbors=12,
                                                 n_components=2)
    dcolor = len(color) / 5.0
    ax.scatter(X_r[:, 0], X_r[:, 1], c=color[j*dcolor:(j+1)*dcolor], cmap=plt.cm.Spectral)

plt.axis('tight')
plt.xticks([]), plt.yticks([])
plt.title('Projected data')
plt.show()
