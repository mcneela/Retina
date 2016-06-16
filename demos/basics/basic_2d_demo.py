from retina.core.axes import *
import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure(figsize=(20, 20))
subplots = plt.subplot('111', projection='Fovea2D') 
plt.xlabel('x')
plt.ylabel('y')
plt.title('Polynomial Layer Plots')
quadratic = subplots.add_layer("quadratic")
quadratic.set_style('g-')
x = np.linspace(-2, 2)
y1 = x ** 2
quadratic.add_data(x, y1)

cubic = subplots.add_layer("cubic")
y2 = x ** 3
subplots.cubic.add_data(x, y2)
subplots.build_layers()
y3 = x ** 4
quadratic.add_data(x, y3)
subplots.build_layers()
plt.show()
