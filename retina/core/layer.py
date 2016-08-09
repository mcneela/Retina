import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.lines import Line2D
from matplotlib.artist import *
from matplotlib.patches import *
from retina.core.py2 import *
from retina.core.calc_context import tracker_manager

class Layer2D(object):
    """
    Class defining a Layer object. This class
    should only be used in conjunction with a
    valid Fovea axes.
    """
    default_style = 'b-'

    @classmethod
    def set_default_style(cls, style):
        """
        A class method for setting the default
        style of a Layer. This applies to all
        Layer instances.
        """
        cls.default_style = style

    def __init__(self, name, axes, **kwargs):
        """
        Initializes the Layer class.
        New attributes should be given default
        values in self.default_attrs.
        """
        default_attrs = {
                         'visible': True,
                         'style': Layer2D.default_style,
                         'lines': [],
                         'hlines': [],
                         'vlines': [],
                         'x_data': [],
                         'y_data': [],
                         'plots': [],
                         'patches': [],
                         'bounds': [],
                         'tracker': tracker_manager() 
                         }
        self.name = name
        self.axes = axes
        for attr in kwargs:
            setattr(self, attr, kwargs[attr])
        for attr in default_attrs:
            if not hasattr(self, attr):
                setattr(self, attr, default_attrs[attr])

    def _try_method(self, val, method_name, *args, **kwargs):
        try:
            method_name(val, *args, **kwargs)
        except:
            pass

    def _attr_try_method(self, val, method_name, *args, **kwargs):
        """
        Private method which attempts to call the method
        `method_name` from the potential object `val`.
        """
        if not isinstance(val, Axes) and hasattr(val, method_name):
            try:
                method = getattr(val, method_name)
                method(*args, **kwargs)
            except:
                pass

    def _is_iterable(self, value):
        """
        Returns True if value is iterable and not a string.
        Otherwise returns False.
        """
        return hasattr(value, "__iter__") and not isinstance(value, str)

    def _method_loop(self, attr, method_name, iterable, *args, **kwargs):
        """
        Recursively attempts to apply the method having `method_name`
        to every item in the potential sequence `iterable`.
        """
        for val in list(iterable):
            if self._is_iterable(val):
                self._method_loop(attr, method_name, val, *args, **kwargs)
            else:
                if attr:
                    self._attr_try_method(val, method_name, *args, **kwargs)
                else:
                    self._try_method(val, method_name, *args, **kwargs)

    def _set_visibility(self, boolean):
        """
        Set the visibility of a Matplotlib artist. Accepts either True
        or False.
        """
        self._method_loop(True, "set_visible", self.__dict__.values(), boolean)

    @py2plot
    def show(self):
        """
        Display a layer in the axes window.
        """
        self._set_visibility(True)
        self.visible = True

    @py2plot
    def hide(self):
        """
        Hide a layer in the axes window.
        """
        self._set_visibility(False)
        self.visible = False

    @py2plot
    def toggle_display(self):
        if self.visible:
            self.hide()
        else:
            self.show()

    def add_line(self, *args, **kwargs):
        """
        Add a Matplotlib Line2D object to the layer.
        """
        self.lines.append(Line2D(*args, **kwargs))

    @py2plot
    def add_vline(self, x):
        """
        Add a vertical line specified by the equation
        x = `x` to the layer.
        """
        ymin, ymax = plt.ylim()
        try:
            vline = plt.vlines(x, ymin, ymax)
            self.vlines.append(vline)
        except:
            print("Vertical lines are not supported by this Axes type.")

    @py2plot
    def add_hline(self, y):
        """
        Add a horizontal line specified by the equation
        y = `y` to the layer.
        """
        xmin, xmax = plt.xlim()
        try:
            hline = plt.hlines(y, xmin, xmax)
            self.hlines.append(hline)
        except:
            print("Horizontal lines are not supported by this Axes type.")

    def set_style(self, style):
        """
        Apply a style to all Matplotlib artists in the layer.
        """
        self.style = style

    def set_prop(self, *args, **kwargs):
        """
        Sets property(ies) passed as *args and
        **kwargs for each artist in the layer.
        """
        self._method_loop(False, setp, self.__dict__.values(), *args, **kwargs)

    def _set_linewidth(self, artist, linewidth=None, bold=True):
        if linewidth:
            setp(artist, 'linewidth')
        else:
            current_lw = getp(artist, 'linewidth')
            if bold:
                setp(artist, 'linewidth', 2 * current_lw)
            else:
                lw = max(current_lw / 2, 1)
                setp(artist, 'linewidth', lw)

    def bold(self, linewidth=None):
        """
        Sets linewidth of layer artists to either the value of `linewidth`
        or the default of twice the artist's current linewidth.
        """
        self._method_loop(False, self._set_linewidth, self.__dict__.values(), linewidth)

    def unbold(self):
        """
        Reverts boldfacing of Matplotlib artists caused by calls to Layer.bold()
        """
        self._method_loop(False, self._set_linewidth, self.__dict__.values(), bold=False)

    def add_data(self, x_data, y_data):
        """
        Add data to the layer.

        First argument should be a list, tuple, or array of x data.
        Second argument should be a list, tuple or array of y data.
        Optional third argument should be a list, tuple, or array of z data.
        """
        self.x_data.append(np.array(x_data))
        self.y_data.append(np.array(y_data))

    @py2plot
    def bound(self, shape=Rectangle, **kwargs):
        """
        Draws a boundary having specified `shape` around the data
        contained in the layer. Shape should be a valid Matplotlib
        patch class.

        **kwargs should be Patch instantiation arguments.
        """
        if self.bounds:
            self._method_loop(True, "set_visible", self.bounds, True)
        try:
            x_min, x_max = np.amin(self.x_data[0]), np.amax(self.x_data[0])
            y_min, y_max = np.amin(self.y_data[0]), np.amax(self.y_data[0])
        except:
            print("Bound cannot be calculated because data has not yet "
                  "been added to the plot.")
            return

        for x, y in zip(self.x_data, self.y_data):
            x_lmax, x_lmin = np.amax(x), np.amin(x)
            y_lmax, y_lmin = np.amax(y), np.amin(y)
            if x_lmin < x_min:
                x_min = x_lmin
            if x_lmax > x_max:
                x_max = x_lmax
            if y_lmin < y_min:
                y_min = y_lmin
            if y_lmax > y_max:
                y_max = y_lmax

        if shape is Circle:
            x_mid, y_mid = (x_min + x_max)/2, (y_min + y_max)/2
            center = (x_mid, y_mid)
            radius = np.sqrt((y_max - y_mid) ** 2 +  (x_max - x_mid) ** 2)
            self.patches.append(shape(center, radius, fill=False, **kwargs))
        elif shape is Rectangle:
            lower_left = (x_min, y_min)
            width = x_max - x_min
            height = y_max - y_min
            self.patches.append(shape(lower_left, width, height, fill=False, **kwargs))
        else:
            raise ValueError("Unsupported shape")
        self.axes.add_patch(self.patches[-1])
        self.bounds.append(self.patches[-1])

    @py2plot
    def unbound(self):
        self._method_loop(True, "set_visible", self.bounds, False)

    def add_attrs(self, **kwargs):
        """
        Add a custom attribute to the layer.
        """
        for key, value in kwargs.items():
            setattr(self, key, value)

    def clear(self):
        """
        Clear the layer, setting all attributes to either None
        or their default values as specified in self.default_attrs.
        """
        for key in self.__dict__.keys():
            self.__dict__[key] = None
        self.__dict__.update(self.default_attrs)

    def delete(self):
        attributes = [self.plots, self.hlines, self.vlines, self.bounds]
        for attribute in attributes:
            for artist in attribute:
                try:
                    artist[0].remove() 
                except:
                    artist.remove()
            del attribute[:] 
        self.x_data = []
        self.y_data = []

class Layer3D(Layer2D):
    def __init__(self, name, axes, **kwargs):
        """
        Initializes the Layer class.
        New attributes should be given default
        values in self.default_attrs.
        """
        self.default_attrs = {
                             'visible': True,
                             'style': Layer3D.default_style,
                             'lines': [],
                             'hlines': [],
                             'vlines': [],
                             'x_data': [],
                             'y_data': [],
                             'z_data': [],
                             'plots': [],
                             'planes': [],
                             'patches': [],
                             'bounds': []
                             }
        self.name = name
        self.axes = axes
        for attr in kwargs:
            setattr(self, attr, kwargs[attr])
        for attr in self.default_attrs:
            if not hasattr(self, attr):
                setattr(self, attr, self.default_attrs[attr])

    def add_data(self, x_data, y_data, z_data):
        """
        Add data to the layer.

        First argument should be a list, tuple, or array of x data.
        Second argument should be a list, tuple or array of y data.
        Optional third argument should be a list, tuple, or array of z data.
        """
        self.x_data.append(np.array(x_data))
        self.y_data.append(np.array(y_data))
        self.z_data.append(np.array(z_data))

    def add_plane(self, point, normal, **kwargs):
        """
        normal -- Normal vector (a, b, c) to the plane
        point -- point (x, y, z) on the plane

        Adds a plane having the equation ax + by + cz = d.
        """
        point = np.array(point)
        normal = np.array(normal)
        lims = [self.axes.get_xlim, self.axes.get_ylim, self.axes.get_zlim]
        indices = np.argsort(normal)

        point = point[indices]
        normal = normal[indices]
        lim_list = []
        for sort in indices:
            lim_list.append(lims[sort])
        [l, r, u] = lim_list
        d = point.dot(normal)

        (l_min, l_max), (r_min, r_max) = l(), r()
        l, r = np.meshgrid(np.linspace(l_min, l_max), np.linspace(r_min, r_max))
        u = (d - normal[0] * l - normal[1] * r) * 1. / normal[2]
        var_list = [l, r, u]
        diff_ind = np.argsort(indices)
        unsort = []
        for ind in diff_ind:
            unsort.append(var_list[ind])
        self.planes.append(unsort)
        self.axes.build_layer(self.name, **kwargs)

    @py2plot
    def bound(self, shape='cube', color='b', **kwargs):
        if self.bounds:
            self._method_loop(True, "set_visible", self.bounds, True)
            return
        try:
            x_min, x_max = np.amin(self.x_data[0]), np.amax(self.x_data[0])
            y_min, y_max = np.amin(self.y_data[0]), np.amax(self.y_data[0])
            z_min, z_max = np.amin(self.z_data[0]), np.amax(self.z_data[0])
        except:
            print("Bound cannot be calculated because data has not yet "
                  "been added to the plot.")
            return

        for x, y, z in zip(self.x_data, self.y_data, self.z_data):
            x_lmax, x_lmin = np.amax(x), np.amin(x)
            y_lmax, y_lmin = np.amax(y), np.amin(y)
            z_lmax, z_lmin = np.amax(z), np.amin(z)
            if x_lmin < x_min:
                x_min = x_lmin
            if x_lmax > x_max:
                x_max = x_lmax
            if y_lmin < y_min:
                y_min = y_lmin
            if y_lmax > y_max:
                y_max = y_lmax
            if z_lmin < z_min:
                z_min = z_lmin
            if z_lmax > z_max:
                z_max = z_lmax

        self.bounds = []
        if shape == 'cube':
            x, y, z = [x_min, x_max], [y_min, y_max], [z_min, z_max]
            from itertools import product, combinations
            for s, e in combinations(np.array(list(product(x, y, z))), 2):
                corner = np.sum(np.abs(s - e))
                if corner == (x_max - x_min) or corner == (y_max - y_min) or corner == (z_max - z_min):
                    self.plots.append(self.axes.plot(*zip(s, e), color=color, **kwargs))
                    self.bounds.append(self.plots[-1])
        else:
            raise ValueError("Unsupported shape")

    @py2plot
    def unbound(self):
        self._method_loop(True, "set_visible", self.bounds, False)
