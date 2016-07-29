# The Layer Classes 

Retina provides `Layer2D` and `Layer3D` classes designed to encapsulate related plot elements
such that they may be manipulated, styled, and modified in tandem. This facility is provided
for plots created for viewing in any of the following environments:

1. The native Matplotlib interface.
2. The IPython or Jupyter notebooks.
3. The browser via the Plotly.py and Plotly.js libraries.

The documentation provided herein is for the Matplotlib extension, while details about the Plotly
implementation can be found in the "web" section of this site.

## The `Layer2D` Class

The `Layer2D` class defines an object that holds Matplotlib artists in 2D plots.

------------------------------

**Class-Level Properties**

`default_style`: Defines the template default style and applies to **all** `Layer2D` classes
initialized downstream. Defaults to `b-`, i.e. solid blue lines. 

------------------------------

**Class-Level Functions**

`set_default_style(cls, style)`

Sets the default style for a layer by modifying the `Layer2D.default_style` class property
discussed above. Changes to the `Layer2D` class' default style should be instituted by a call
to this function rather than by directly modifying the class `default_style` property.

------------------------------

**Instance-Level Properties**

`default_attrs`: A dictionary holding the default attributes tracked by a layer. At the time of writing,
 these include:

1. `'visible'`: A boolean specifying whether or not the layer is currently visible.
2. `style`: The layer's current style. Is initialized to the `Layer2D` default style.
3. `lines`: The lines contained in the layer.
4. `hlines`: The horizontal lines contained in the layer.
5. `vlines`: The vertical lines contained in the layer.
6. `x_data`: The x-coordinates of all data points contained in the layer.
7. `y_data`: The y-coordinates of all data points contained in the layer.
8. `plots`: The Matplotlib artist instances contained in the layer.
9. `patches`: The Matplotlib patch (shape) instances contained in the layer.
10. `bounds`: The Matplotlib patches (rectangles or circles) that are created when the `Layer2D.bound()`
			  function is invoked.

`name`: The string used to identify the layer. Provided by the user on class instantiation.
`axes`: The Matplotlib Axes instance to which the layer is attached.

------------------------------

**Instance-Level Functions**

`show()`: Sets the layer's `visible` property to `True` and sets the visibility of each layer artist to `True`.

------------------------------

`hide()`: Sets the layer's `visible` property to `False` and sets the visibility of each layer artist to `False`.

------------------------------

`toggle_display()`: Toggles the visibility of the layer. In other words, if the `layer.visible = False` then
`layer.show()` is called. Otherwise `layer.hide()` is called.

------------------------------

`add_line(*args, **kwargs)`: Adds a Matplotlib `Line2D` artist to the layer. Also appends the artist to the 
`layer.lines` attribute.

------------------------------

`add_vline(self, x)`: Adds a Matplotlib vertical `Line2D` artist satisfying the equation x = `x` to the layer.
Also appends the artist to the `layer.lines` attribute.

------------------------------

`set_style(style)`: Applies a Matplotlib style to all artists residing in the layer by updating the `layer.style`
 attribute. As such, the layer must be rebuilt for changes to take effect.

------------------------------

`set_prop(*args, **kwargs)`: Sets the provided artist property(s) to the provided value(s) for all artists in the
 layer via a call to Matplotlib's `setp` function.

------------------------------

`bold(linewidth=None)`: Doubles the linewidth of all artists in the layer unless a value for the linewidth argument
 is specified.

------------------------------

`unbold(linewidth=None)`: Halves the linewidth of all artists in the layer so as to undo the effects caused by the
 `bold()` function.

------------------------------

`add_data(x_data, y_data)`: Add arrays of `x` and `y` data values to the layer.

------------------------------

`bound(shape=Rectangle, **kwargs)`: Draws a boundary having the specified shape around the artists contained in the layer.
 `shape` should be a valid Matplotlib patch class.

------------------------------

`unbound()`: Removes the bounds drawn by the `bound()` function from the layer.

------------------------------

`add_attrs()`: Add a custom attribute to the layer class.

------------------------------

`clear()`: Clears the layer, setting all attributes to either `None` or their default values as specified in `default_attrs`.

------------------------------

## The `Layer3D` Class

The `Layer3D` class inherits from the `Layer2D` classes and implements all of the functions defined therein with the exception
of `add_line()`, `add_vline()`, and `add_hline()`.

------------------------------

**Instance-Level Properties**

1. `visible`: Default `True`
2. `style`: `Layer3D.default_style` 
3. `lines`
4. `hlines`
5. `vlines`
6. `x_data`
7. `y_data`
8. `z_data`: The z-coordinates of the data contained in the layer.
9. `plots`
10. `planes`: The list of planes contained in the layer.
11. `patches`
12. `bounds`

------------------------------

`add_data(x_data, y_data, z_data)`: Add data to the layer specified by its x, y, and z coordinates.

------------------------------

`add_plane(point, normal, **kwargs)`: Add a plane to the layer defined by the following format.

normal -- Normal vector (a, b, c) to the plane.
point  -- point (x, y, z) on the plane

Adds a plane having the equation ax + by + cz = d.

------------------------------

`bound(shape='cube', color='b', **kwargs)`: Draws a cube having the provided color around the boundary of the artists in the layer.

------------------------------

`unbound()`: Undoes the 3D bounding method. 
