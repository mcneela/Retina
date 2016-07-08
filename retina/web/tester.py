import plotly.offline as offline 
import plotly.graph_objs as go
import numpy as np
import json

pts = np.loadtxt('dataset.txt')
x, y, z = zip(*pts)

trace = go.Mesh3d(x=x, y=y, z=z, color='90EE90', opacity=0.75)
offline.plot([trace])


