import numpy as np
import fovea_plot as fp
import plotly.graph_objs as go


x = np.linspace(-5, 5)
y = x ** 2

y2 = x ** 3

y3 = x ** 4

trace1 = go.Scatter(
    x = x,
    y = y,
    mode = 'lines'
)

trace2 = go.Scatter(
    x = x,
    y = y2,
    mode = 'lines'
)

trace3 = go.Scatter(
    x = x,
    y = y3,
    mode = 'lines'
)

doc = fp.Document()

doc.fovea_plot([trace1, trace2, trace3])
doc.view()

layer1 = fp.Layer2D("Layer1", doc)
layer2 = fp.Layer2D("Layer2", doc)
layer3 = fp.Layer2D("Layer3", doc)

layer1.add_trace(trace1)
layer2.add_trace(trace2)
layer3.add_trace(trace3)

# Try running the following

# myLayer.hide()

# myLayer.show()

# myLayer.toggle_display()

# myLayer.add_vline(2)

# myLayer.add_hline(15)

# print(myLayer.compute_layer_bounds())
