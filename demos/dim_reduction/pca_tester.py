"""
Executable code for the PCA user story.
Run disc() to explore a randomly generated flat disc data. Run hypesphere to explore a high dimensional ball
of randomly generated data.
"""

import pca_disc
from pca_disc import *

from PyDSTool.Toolbox import synthetic_data as sd

import random
import numpy as np
import __future__

DOI = [(-10,10),(-10,10)]

def disc():
    pts = sd.generate_ball(100, 2, 10)
    pts = np.concatenate((pts, np.zeros((100, 1))), axis=1)

    trans_am = 12
    trans_ax = 1

    X = [[],[],[]]
    for i in range(3):
        X[i] = rotate_z(rotate_y(rotate_x(translate(pts, trans_ax, trans_am),
                                          random.uniform(0, 2*np.pi)),
                                 random.uniform(0, 2*np.pi)),
                        random.uniform(0, 2*np.pi))
        X[i] = noise(X[i], 2, 0.3, 0, 10)

    rot_layers = ['rot1', 'rot2', 'rot3']
    rot_styles = ['r', 'g', 'b']

    fig, [before, after, variance] = pca_disc.setupDisplay(rot_layers, rot_styles, DOI)
    layer_obj = before.get_layer('orig_data')
    layer_obj.add_data(pts[:,0], pts[:,1], pts[:,2])
    layer_obj.set_style('y.')

    before.build_layers()
    after.build_layers()
    variance.build_layers()

    return ControlSys(fig, X, rot_layers, rot_styles, 2, before, after, variance)

def hypersphere(dim):
    pts = sd.generate_ball(100, dim, 10)

    #Create and stretch different hypersphere "clusters":
    X1 = translate(stretch(stretch(sd.generate_ball(133, dim, 10), 0, 1.4), 1, 1.4), 0, 25)
    X2 = translate(sd.generate_ball(110, dim, 10), 1, 20)
    X3 = translate(noise(sd.generate_ball(95, dim, 10), 2, 0.6, 0, 2), 2, 15)

    X = [X1, X2, X3]

    clus_layers = ['clus1', 'clus2', 'clus3']
    clus_styles = ['r', 'g', 'b']

    fig, [before, after, variance] = pca_disc.setupDisplay(clus_layers, clus_styles, DOI)

    proj_vecsHI = pca_disc.ortho_proj_mat(len(X[0][0]), 3)
    proj_vecsLO = pca_disc.ortho_proj_mat(len(X[0][0]), 2)

    #Plot the entire dataset in blue.
    X_all = np.concatenate((X1,X2,X3))

    layer_obj = before.get_layer('orig_data')
    layer_obj.add_data(np.dot(X_all, proj_vecsHI).transpose())
    layer_obj.set_style('y.')

    return ControlSys(gui.masterWin, X, clus_layers, clus_styles, 2, proj_vecsLO, proj_vecsHI)

ctrl_sys = disc()
#ctrl_sys = hypersphere(6)

halt= True
