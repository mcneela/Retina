"""
Adopted from the swiss_roll.py example
packaged with Scikit-Learn.
"""
import mapping
import matplotlib.pyplot as plt
import retina.core.axes
import numpy as np
from matplotlib import gridspec
from sklearn import manifold, datasets

def mouse_over(event):
    ax = event.inaxes
    print(ax.name)
    sec = nld.get_layer(ax.title._text)
    sec.bound()

X, color = datasets.samples_generator.make_swiss_roll(n_samples=1500)
print("Computing LLE embedding")
X_r, err = manifold.locally_linear_embedding(X, n_neighbors=12,
                                             n_components=2)
print("Done. Reconstruction error: %g" % err)

dat_min = np.amin(X[:,1])
dat_max = np.amax(X[:,1])
fig = plt.figure(figsize=(20, 20))
gs = gridspec.GridSpec(2, 3)
nld = plt.subplot(gs[0,0], projection='Fovea3D')

fig.canvas.mpl_connect('motion_notify_event', mouse_over)
num_sections = 5
sections = mapping.section(X, num_sections, axis='z')
colors = mapping.section(X, num_sections, axis='y')
for i, j, sec, clr in zip([0, 0, 1, 1, 1], range(num_sections), sections, colors):
    swiss_sec = nld.add_layer('section ' + str(j))
    ax = plt.subplot(gs[i, (j + 1) % 3], projection='Fovea2D')
    X_r, err = manifold.locally_linear_embedding(sec, n_neighbors=50,
                                                 n_components=2)
    dcolor = len(color) / 5.0
    swiss_sec.add_data(sec[:, 0], sec[:, 1], sec[:, 2])
    nld.build_layer(swiss_sec.name, c=color[j*dcolor:(j+1)*dcolor], plot=nld.scatter, vmin=dat_min, vmax=dat_max, cmap=plt.cm.Spectral)
    ax.scatter(X_r[:, 0], X_r[:, 1], c=color[j*dcolor:(j+1)*dcolor], vmin=dat_min, vmax=dat_max, cmap=plt.cm.Spectral)
    ax.set_title('section ' + str(j))

nld.set_title("Original data")
plt.axis('tight')
plt.xticks([]), plt.yticks([])
plt.show()
