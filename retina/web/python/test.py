x = np.linspace(-5, 5)
y = x ** 2

trace = go.Scatter(
    x = x,
    y = y,
    mode = 'lines',
)

doc = Document()

doc.fovea_plot([trace])
doc.view()

myLayer = Layer2D("myLayer", doc)

# Try running the following

# myLayer.hide()

# myLayer.show()

# myLayer.toggle_display()

# myLayer.add_vline(2)

# myLayer.add_hline(15)

# print(myLayer.compute_layer_bounds())
