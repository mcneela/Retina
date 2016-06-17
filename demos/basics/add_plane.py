"""
Demo of the add_plane() feature of the Fovea3D class.
"""
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
import retina.core.axes

fig = plt.figure(figsize=(20, 20))
ax = plt.subplot('111', projection='Fovea3D')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
plt.title('Plane Demo')

# Add four layers to the axes to hold the 
# four different planes to be generated.
x = ax.add_layer('x_plane')
y = ax.add_layer('y_plane')
z = ax.add_layer('z_plane')
gen = ax.add_layer('gen_plane')

# Add a plane to each of the four layers.
# The method signature for add_plane is
# def add_plane(self, point, normal, **kwargs)
# point is of the form [x, y, z]
# normal is of the form [a, b, c]
# **kwargs are styling and other keyword arguments
# to matplotlib's plot_surface function.
#
# The method generates a plane having the equation
# ax + by + cz = d

# Plot a plane having equation x = 1 and styled red
x.add_plane([1, 0, 0], [1, 0, 0], color='r')

# Plot a plane having equation y = 0.5 and styled green
y.add_plane([0, .5, 0], [0, 1, 0], color='g')

# Plot a plane having equation z = 0.5 and styled blue
z.add_plane([0, 0, .5], [0, 0, 1], color='b')

# Plot a plane having equation x + y + z = 2 and styled orange
gen.add_plane([1, -1, 2], [1, 1, 1], color=colors.cnames['orange'])
