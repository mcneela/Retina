import retina.core.axes
import matplotlib.pyplot as plt
import numpy as np

def randrange(n, vmin, vmax):
    return (vmax - vmin)*np.random.rand(n) + vmin

fig = plt.figure()
ax = fig.add_subplot(111, projection='Fovea3D')
n = 100

# Create two layers to hold the two styles of scatter data.
circles = ax.add_layer('circles')
triangles = ax.add_layer('triangles')

# Add the scatter data to each layer and build the layer
# using the desired scatter plot.
for c, m, zl, zh, layer, name in [('r', 'o', -50, -25, circles, 'circles'), ('b', '^', -30, -5, triangles, 'triangles')]:
    xs = randrange(n, 23, 32)
    ys = randrange(n, 0, 100)
    zs = randrange(n, zl, zh)
    layer.add_data(xs, ys, zs)
    ax.build_layer(name, plot=ax.scatter, c=c, marker=m)

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Show the original data
plt.pause(2)

# Hide the triangles
print("Hiding triangles...")
triangles.hide()
plt.pause(2)

# Bound the circles
print("Bounding circles...")
circles.bound()
plt.pause(2)

# Hide the circles
print("Hiding circles...")
circles.hide()
plt.pause(2)

# Show the triangles
print("Showing triangles...")
triangles.show()
plt.pause(2)

# Bound the triangles with a different color box
print("Bounding triangles...")
triangles.bound(color='g')
plt.pause(2)

# Show all layers
print("Showing all layers...")
circles.show()
