"""
Adapted from the swiss_roll.py example
packaged with Scikit-Learn.
"""
import matplotlib.pyplot as plt
import retina.core.axes
import retina.nldr as nldr
import numpy as np
from matplotlib import gridspec
from sklearn import manifold, datasets

class EventSystem:
    def __init__(self, fig):
        self.fig = fig
        self.hover_sec = None
        self.click_sec = None
        self.fig.canvas.mpl_connect('motion_notify_event', self.mouse_over)
        self.fig.canvas.mpl_connect('button_press_event', self.mouse_click)

    def mouse_over(self, event):
        ax = event.inaxes
        try:
            sec = nld.get_layer(ax.title._text)
        except:
            return
        if sec is not self.hover_sec and self.hover_sec:
            self.hover_sec.unbound()
        sec.bound()
        self.hover_sec = sec

    def mouse_click(self, event):
        ax = event.inaxes
        try:
            sec = nld.get_layer(ax.title._text)
        except:
            return
        if sec is not self.click_sec and self.click_sec:
            nld.showcase(sec.name)
        self.click_sec = sec


X, color = datasets.samples_generator.make_swiss_roll(n_samples=1500)
X_r, err = manifold.locally_linear_embedding(X, n_neighbors=12,
                                             n_components=2)

dat_min = np.amin(X[:,1])
dat_max = np.amax(X[:,1])
fig = plt.figure(figsize=(20, 20))
gs = gridspec.GridSpec(2, 3)
nld = plt.subplot(gs[0,0], projection='Fovea3D')

num_sections = 5
sections = nldr.mapping.ordered_section(X, num_sections, axis=0)
color = color[color.argsort()]
colors = [color[i*len(color)/5.0:(i+1)*len(color)/5.0] for i in range(5)]

for i, j, sec, clr in zip([0, 0, 1, 1, 1], range(num_sections), sections, colors):
    swiss_sec = nld.add_layer('section ' + str(j))
    ax = plt.subplot(gs[i, (j + 1) % 3], projection='Fovea2D')
    X_r, err = manifold.locally_linear_embedding(sec, n_neighbors=50,
                                                 n_components=2)
    dcolor = len(color) / 5.0
    swiss_sec.add_data(sec[:, 0], sec[:, 1], sec[:, 2])
    nld.build_layer(swiss_sec.name, c=color[j*dcolor:(j+1)*dcolor], plot=nld.scatter, cmap=plt.cm.Spectral)
    proj = ax.add_layer('section ' + str(j) + ' proj')
    proj.add_data(X_r[:, 0], X_r[:, 1])
    ax.build_layer(proj.name, plot=ax.scatter, c=color[j*dcolor:(j+1)*dcolor], cmap=plt.cm.Spectral)
    ax.set_title('section ' + str(j))

handler = EventSystem(fig)
print("Hover over a projected data plot to see the corresponding segment in the original Swiss Roll.")
print("Click on a subplot to see the corresponding segment of the original Swiss Roll be showcased.")
nld.set_title("Original data")
plt.axis('tight')
plt.xticks([]), plt.yticks([])
plt.show()
