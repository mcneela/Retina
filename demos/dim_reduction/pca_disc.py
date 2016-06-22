"""
This module holds the keypress control system class, Fovea setup, and linalg methods
used to transform disc data for the PCA user story.
"""

from __future__ import absolute_import, print_function

from PyDSTool.Toolbox import data_analysis as da

import numpy as np
import matplotlib.pyplot as plt

from PyDSTool import *
import retina.core.axes
import random

def translate(X, axis, amount):
    A = np.zeros((len(X), len(X[0])))
    A[:,axis] = np.ones(len(X))*amount
    Y = X + A
    return Y

def rotate_x(X, theta):
    R = np.array([[1, 0, 0], [0, np.cos(theta), -np.sin(theta)], [0, np.sin(theta), np.cos(theta)]])
    Y = np.dot(R, X.transpose())
    return Y.transpose()

def rotate_y(X, theta):
    R = np.array([[np.cos(theta), 0, -np.sin(theta)], [0, 1, 0], [np.sin(theta), 0, np.cos(theta)]])
    Y = np.dot(R, X.transpose())
    return Y.transpose()

def rotate_z(X, theta):
    R = np.array([[np.cos(theta), np.sin(theta), 0], [-np.sin(theta), np.cos(theta), 0], [0, 0, 1]])
    Y = np.dot(R, X.transpose())
    return Y.transpose()

def stretch(X, axis, amount):
    X[:,axis] = X[:,axis]*amount
    return X

def noise(X, axis, percent, loc, scale):
    for i in range(0, int(round(len(X)*percent))):
        X[i][axis] = np.random.normal(loc, scale, 1)
    return X

def ortho_proj_mat(n, m):
    Z = npy.random.rand(n, m)
    Q, R = npy.linalg.qr(Z)
    return Q

def compute(X, new_dim, layer, style, before, after, variance, proj_vecsLO = None, proj_vecsHI = None):

    data_dict = {}
    data_dict['X'] = X

    p = da.doPCA(X, len(X[0]), len(X[0])) #Creates a pcaNode object.

    pcMat = p.get_projmatrix()

    pcPts = np.concatenate(([pcMat.transpose()[0,:]*15],
                            [-pcMat.transpose()[0,:]*15]), axis=0)

    for j in range(1, new_dim):
        pcPts = np.concatenate((pcPts, [pcMat.transpose()[j,:]*15],
                                [-pcMat.transpose()[j,:]*15]), axis=0)

    Y = p._execute(X, new_dim) #Get dimensionality reduced data.
    data_dict['Y'] = Y

    #Produce proj vecs if none supplied
    if proj_vecsHI is None:
        proj_vecsHI = ortho_proj_mat(len(X[0]), 3)

    if proj_vecsLO is None:
        proj_vecsLO = ortho_proj_mat(len(Y[0]), 2)

    #If data are high-dimensional, use the projection vectors.
    if len(X[0]) > 3:
        X = npy.dot(X, proj_vecsHI)
        pcPts = npy.dot(pcPts, proj_vecsHI)
        data_dict['X_projected'] = X

    if len(Y[0]) > 2:
        proj_vecsLO = proj_vecsLO[0:new_dim, :] #Scrape the needed rows from projection matrix, so we can page between dimensionalities.
        Y = npy.dot(Y, proj_vecsLO)
        data_dict['Y_projected'] = Y

    #Create line plot for variance explained by each component.
    layer_obj = variance.get_layer(layer)
    layer_obj.add_data(range(1, len(p.d)+1), p.d/sum(p.d))
    layer_obj.set_style(style + "-o")

    #Create plot of high-dimensional data and its PC's.
    layer_obj = before.get_layer(layer)
    layer_obj.add_data(X[:,0], X[:,1], X[:,2])
    layer_obj.set_style(style + '.')

    for j in range(0, len(pcPts), 2):
        before.add_layer(layer + " PC")
        layer_obj = before.get_layer(layer + " PC")
        layer_obj.add_data(pcPts[j+0:j+2,0], pcPts[j+0:j+2,1], pcPts[j+0:j+2,2])
        layer_obj.add_data(pcPts[j+2:j+4,0], pcPts[j+2:j+4,1], pcPts[j+2:j+4,2])
        layer_obj.set_style(style)

    #Create plot of low-dimensional data.

    layer_obj = after.get_layer(layer)
    layer_obj.add_data(Y[:,0], Y[:,1])
    layer_obj.set_style(style + ".")

    print("Variance Explained in", layer,"with first",new_dim,"components:")
    print(sum(p.d[0:new_dim])/sum(p.d))
    
    before.build_layers()
    after.build_layers()
    variance.build_layers()

    return data_dict


def setupDisplay(clus_layers, clus_styles, DOI):
    fig = plt.figure(figsize=(14,6))
    fig.suptitle('PCA Disc')
    fig.canvas.set_window_title('Master')
    
    before = plt.subplot('131', projection='Fovea3D')
    before.set_title('Before')
    after = plt.subplot('132', projection='Fovea2D')
    after.set_title('After')
    variance = plt.subplot('133', projection='Fovea2D')
    variance.set_title('Variance by Components')
    subplots = [before, after, variance]

    #Setup all layers
    before.add_layer('orig_data')
    before.add_layer('meta_data', kind='text')

    for clus in clus_layers:
        before.add_layer(clus)
        after.add_layer(clus)
        variance.add_layer(clus)

    for subplot in subplots:
        subplot.build_layers()

    return fig, subplots

proj_thresh = 20

class ControlSys(object):
    def __init__(self, fig, data, clus_layers, clus_styles, d, before, after, variance, proj_vecsLO=None, proj_vecsHI=None):
        self.fig = fig
        self.before = before
        self.after = after
        self.variance = variance
        self.data = data
        self.data_dict = None
        self.proj_thresh = 4
        self.clus_layers = clus_layers
        self.clus_styles = clus_styles
        self.proj_vecsLO = proj_vecsLO
        self.proj_vecsHI = proj_vecsHI
        self.d = d
        self.c = 0
        self.m = False
        self.fig.canvas.mpl_connect('key_press_event', self.keypress)

        for i in range(len(clus_layers)):
            self.data_dict = compute(data[i], d, clus_layers[i], clus_styles[i], self.before, self.after, self.variance, proj_vecsLO, proj_vecsHI)

        self.highlight_eigens(self.variance)

        #Initialize Bombardier callbacks on 2D subplot.
        #gui.current_domain_handler.assign_criterion_func(self.get_projection_distance)
        #gui.assign_user_func(self.get_displacements)

        #User tips
        print("Press left or right arrow keys to view different rotations of Hi-D data and their PC's.")
        print("Press m to display or hide all layers.")
        print("Press h to show or hide original data.")

    def highlight_eigens(self, variance):
        for i in range(len(self.clus_layers)):
            for j in range(1, self.d+1):
                layer_obj = variance.get_layer(self.clus_layers[i])
                layer_obj.add_vline(j)

    def get_projection_distance(self, pt_array, fsign=None):
        #Judge by nearest point rather than points inside. Otherwise, I would need to access the whole polygon,
        #which would be difficult.
        nearest_pt = []
        index = []

        try:
            pts = self.data_dict['Y_projected']
        except KeyError:
            pts = self.data_dict['Y']

        #Find closest projected point.
        dist = 10000000
        for i, row in enumerate(pts):
            if np.linalg.norm(pt_array - row) < dist:
                dist = np.linalg.norm(pt_array - row)
                nearest_pt = row
                index = i

        #Need more formal way to do this. Standard deviation? This doesn't seem to accomplish anything right now anyways.
        if dist > 2 and fsign is not None:
            return -fsign

        #Calculate distance between projected point and loD point.
        orig_pt = self.data_dict['Y'][i]
        proj_pt = np.append(nearest_pt, np.zeros(len(orig_pt)-len(nearest_pt)))
        if np.linalg.norm(orig_pt - proj_pt) > self.proj_thresh:
            return -1
        else:
            return 1

    def keypress(self, event):

        if event.key == 'left' or event.key == 'right':
            if event.key == 'left':
                self.c += 1
            else:
                self.c -= 1

            layer_obj = self.before.get_layer(self.clus_layers[self.c%len(self.clus_layers)])
            layer_obj.toggle_display()

        if event.key == 'm':
            self.m = not self.m
            for clus in self.clus_layers:
                layer_obj = self.before.get_layer(clus)
                if self.m:
                    layer_obj.show()
                else:
                    layer_obj.hide()

        if event.key == 'h':
            layer_obj = self.before.get_layer('orig_data')
            layer_obj.toggle_display()

        if self.proj_vecsHI is not None:
            if (event.key == 'up' and self.d is not len(self.proj_vecsHI)) or (event.key == 'down' and self.d is not 2):
                if event.key == 'up':
                    self.d += 1
                elif event.key == 'down':
                    self.d -= 1

                print("Attempting to display", self.d,"-dimensional data...")

                for i in range(len(self.clus_layers)):
                    self.data_dict = compute(self.data[i], self.d, self.clus_layers[i], self.clus_styles[i], self.before, self.after, self.variance, self.proj_vecsLO, self.proj_vecsHI)

                self.highlight_eigens(self.variance)

    def get_displacements(self, x, y):
        print("Last output = (mag dict, vector dict)")
        Fxs = []
        Fys = []
        Fs = []

        try:
            pts = self.data_dict['Y_projected']
        except KeyError:
            pts = self.data_dict['Y']

        ixs = range(len(pts))
        for i in ixs:
            Fx = x - pts[i][0]
            Fy = y - pts[i][1]
            Fxs.append(Fx)
            Fys.append(Fy)
            Fs.append(sqrt(Fx*Fx+Fy*Fy))
        return dict(zip(ixs, Fs)), dict(zip(ixs, zip(Fxs, Fys)))
