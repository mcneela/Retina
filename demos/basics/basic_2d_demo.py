"""
A basic demonstration of setting up a Matplotlib
plot using the Fovea2D axes class and adding
layers to said plot.
"""
from retina.core.axes import *
import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure(figsize=(20, 20))

# Create a subplot axes of the Fovea2D variety.
subplots = plt.subplot('111', projection='Fovea2D') 

plt.xlabel('x')
plt.ylabel('y')

plt.title('Polynomial Layer Plots')

# Create a layer to hold the quadratic and quartic function data.
quadratic = subplots.add_layer("quadratic")

# Set the style of the layer.
quadratic.set_style('g-')

x = np.linspace(-2, 2)
y1 = x ** 2
# Add the x ** 2 function to the layer.
quadratic.add_data(x, y1)

y3 = x ** 4
# Add the x ** 4 function to the layer.
quadratic.add_data(x, y3)

# Create a layer to hold the cubic function data.
cubic = subplots.add_layer("cubic")
y2 = x ** 3

# Add the x ** 3 function to the layer.
subplots.cubic.add_data(x, y2)

# Plot the data in each of the layers residing within the
# "subplots" axes.
subplots.build_layers()

# Show the resulting plot.
plt.show()

# Run any of the following commands to experiment with hiding
# and showing individual layers.
#
# quadratic.hide()
# cubic.hide()
# quadratic.show()
# cubic.show()
# quadratic.toggle_display()
# cubic.toggle_display()
