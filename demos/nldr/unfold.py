import matplotlib.pyplot as plt
import matplotlib
import retina.core.axes
import retina.nldr as nldr 
import numpy as np
import math
from matplotlib import gridspec
from matplotlib.widgets import Slider
from sklearn import manifold, datasets

        
X, color = datasets.samples_generator.make_swiss_roll(n_samples=1500)
X_r, err = manifold.locally_linear_embedding(X, n_neighbors=12,
                                             n_components=2)

segs = nldr.mapping.progressive_segment(X_r, 10, axis=1)
roll_segs = nldr.mapping.progressive_segment(X, 10, axis=2)
color = color[color.argsort()]

fig = plt.figure(figsize=(20, 20))
roll = fig.add_subplot(211, projection='Fovea3D')
proj = fig.add_subplot(212, projection='Fovea2D')
axcolor = 'lightgoldenrodyellow'
segselector = plt.axes([0.125, 0.025, .8, 0.03], axisbg=axcolor)
dcolor = len(color)/len(segs)
for i in range(len(segs)):
    seg = segs[i]
    roll_seg = roll_segs[i]
    proj_layer = proj.add_layer('segment ' + str(int(i)))
    proj_layer.add_data(seg[:, 0], seg[:, 1])
    roll_layer = roll.add_layer('segment ' + str(int(i)))
    roll_layer.add_data(roll_seg[:,0], roll_seg[:,1], roll_seg[:,2])
    new_colors = color.copy()
    new_colors = new_colors[0:(i+1)*dcolor]
    proj.build_layer(proj_layer.name, plot=proj.scatter, c=new_colors, cmap=plt.cm.Spectral)
    roll.build_layer(roll_layer.name, plot=roll.scatter, c=new_colors, cmap=plt.cm.Spectral)
proj.showcase('segment 9')
roll.showcase('segment 9')

slid = Slider(segselector, 'Segment Selector', 0, 9, valinit=0, valfmt='%0.0f')
def update(val):
    seg_num = math.floor(slid.val)
    proj.showcase('segment ' + str(int(seg_num)))
    roll.showcase('segment ' + str(int(seg_num)))

slid.on_changed(update)
