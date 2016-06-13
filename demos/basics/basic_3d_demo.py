from retina.core.axes import *
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def randrange(n, vmin, vmax):
    return (vmax-vmin)*np.random.rand(n) + vmin

fig = plt.figure()
subplot = fig.add_subplot(111, projection='Fovea3D')
subplot.add_layer("spiral")
spiral = subplot.get_layer("spiral")
theta = np.linspace(-4 * np.pi, 4 * np.pi, 100)
z = np.linspace(-2, 2, 100)
r = z**2 + 1
x = r * np.sin(theta)
y = r * np.cos(theta)
spiral.add_data(x, y, z)
spiral.set_style('b-')

subplot.add_layer("scatter_layer")
scatter_layer = subplot.get_layer("scatter_layer")
n = 50
for c, m, zl, zh in [('r', 'o', -50, -25), ('b', '^', -30, -5)]:
    xs = randrange(n, 23, 32)
    ys = randrange(n, 0, 100)
    zs = randrange(n, zl, zh)
scatter_layer.add_data(xs, ys, zs)

subplot.set_xlabel('X')
subplot.set_ylabel('Y')
subplot.set_zlabel('Z')

subplot.build_layer("spiral")
subplot.build_layer("scatter_layer", plot=subplot.scatter, c=c, marker=m)
#plt.show()
