import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.projections import projection_registry
from axes import *

# Registers the Fovea2D and Fovea3D classes as valid projections.
projection_registry.register(Fovea2D)
projection_registry.register(Fovea3D)

