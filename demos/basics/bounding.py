"""
A demonstration of Retina's ability to
create a bounding shape around the data
plotted in a layer.
"""
import retina.core.axes
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import numpy as np

fig = plt.figure(figsize=(20, 20))
subplot = plt.subplot('111', projection='Fovea2D') 
plt.xlabel('x')
plt.ylabel('y')
plt.title('Layer Bounding Functionality Demonstration')

######################
# Set up first layer #
######################
x = np.linspace(-10, 10)
y = np.sin(2 * np.sin( 2 * np.sin( 2 * np.sin(x))))
# Add layer 'sin_like' to the subplot axes
# subplot.add_layer returns the Layer object
sin_like = subplot.add_layer('sin_like') 
# Add x and y data to the layer
sin_like.add_data(x, y)
# Set the style for the layer
sin_like.set_style('r-')

#######################
# Set up second layer #
#######################
logs = subplot.add_layer('logs')
x = np.linspace(0.01, 10)
y = np.log(x)
logs.add_data(x, y)

logs.add_data(-x, y)

# Build all of the axes layers using the default
# plt.plot() plotting function.
subplot.build_layers()

# Run the following commands in iPython or the interpreter to
# watch a bounding box be drawn for both of the layers.
# sin_like.bound()
# logs.bound()

# Run the following commands in iPython or the interpreter to
# watch a bounding circle be drawn for both of the layers.
# sin_like.bound(shape=Circle)
# logs.bound(shape=Circle)
