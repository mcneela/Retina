"""
A demo of the Layer2D.bold()/Layer3D.bold() function.
"""
import matplotlib.pyplot as plt
import numpy as np
import retina.core.axes
import time

plt.ion()
fig = plt.figure(figsize=(20, 20))
ax = plt.subplot('111', projection='Fovea2D')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Boldface Plot Demo')

sinc = ax.add_layer('sinc')
x = np.linspace(-6, 6)
y = 20 * (np.sin(x) / x)
sinc.add_data(x, y)
sinc.set_style('r-')

quadsin = ax.add_layer('quadsin')
y = (x ** 2) * np.sin(x)
quadsin.add_data(x, y)
quadsin.set_style('b--')

ax.build_layers()
plt.show()

plt.pause(2)

# Bold the sinc layer.
sinc.bold()
print("Making 'sinc' layer bold.")

plt.pause(2)

# Bold the sinc layer a second time.
# As you can see, boldening effects
# stack incrementally.
sinc.bold()
print("Increasing boldness of 'sinc' layer.")

plt.pause(2)

# Unbold the sinc layer.
sinc.unbold()
print("Decreasing boldness of 'sinc' layer.")

plt.pause(2)

# Unbold a second time.
sinc.unbold()
print("Returning 'sinc' layer to default linewidth.")

plt.pause(2)

# Subsequent unbolds have no effect
# since layer has reached default linewidth.
sinc.unbold()
print("This unbold operation has no effect.")
