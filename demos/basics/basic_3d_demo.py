import retina.core.axes
import matplotlib.pyplot as plt
import numpy as np

def randrange(n, vmin, vmax):
    return (vmax-vmin)*np.random.rand(n) + vmin

fig = plt.figure()

# Add a Fovea3D subplot to the figure.
subplot = fig.add_subplot(111, projection='Fovea3D')

# Add a layer to hold the spiral plot.
spiral = subplot.add_layer("spiral")

theta = np.linspace(-4 * np.pi, 4 * np.pi, 100)
z = np.linspace(-2, 2, 100)
r = z**2 + 1
x = r * np.sin(theta)
y = r * np.cos(theta)

# Add the spiral data to the layer.
spiral.add_data(x, y, z)
# Set the style for the layer.
spiral.set_style('b-')

# Add another layer to hold the 3D scatter plot.
scatter_layer = subplot.add_layer("scatter_layer")

n = 50
for c, m, zl, zh in [('r', 'o', -50, -25), ('b', '^', -30, -5)]:
    xs = randrange(n, 23, 32)
    ys = randrange(n, 0, 100)
    zs = randrange(n, zl, zh)
scatter_layer.add_data(xs, ys, zs)

subplot.set_xlabel('X')
subplot.set_ylabel('Y')
subplot.set_zlabel('Z')

# Build both layers.
subplot.build_layer("spiral")
subplot.build_layer("scatter_layer", plot=subplot.scatter, c=c, marker=m)
