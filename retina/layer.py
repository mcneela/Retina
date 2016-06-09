import matplotlib
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt

class Layer:
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
    
    def __init__(self, name, **kwargs):
        """
        Initializes the Layer class.
        New attributes should be given default
        values in self.default_attrs.
        """
        self.default_attrs = {
                             'visible': True,
                             'style': Layer.default_style,
                             'lines': [],
                             'hlines': [], 
                             'vlines': [], 
                             'x_data': [],
                             'y_data': [],
                             'z_data': [],
                             'plots': [] 
                             }
        self.name = name
        for attr in kwargs:
            setattr(self, attr, kwargs[attr])
        for attr in self.default_attrs: 
            if not hasattr(self, attr):
                setattr(self, attr, self.default_attrs[attr])

    def _try_method(self, val, method_name, *args, **kwargs):
        """
        Private method which attempts to call the method
        `method_name` from the potential object `val`.
        """
        if hasattr(val, method_name):
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

    def _method_loop(self, method_name, iterable, *args, **kwargs):
        """
        Recursivley attempts to apply the method having `method_name`
        to every item in the potential sequence `iterable`.
        """
        for val in list(iterable):
            if self._is_iterable(val):
                self._method_loop(method_name, val, *args, **kwargs)
            else:
                self._try_method(val, method_name, *args, **kwargs)

    def _set_visibility(self, boolean):
        """
        Set the visibility of a Matplotlib artist. Accepts either True
        or False.
        """
        self._method_loop("set_visible", self.__dict__.values(), boolean)

    def show(self):
        """
        Display a layer in the axes window.
        """
        self._set_visibility(True)
        self.visible = True

    def hide(self):
        """
        Hide a layer in the axes window.
        """
        self._set_visibility(False)
        self.visible = False

    def add_line(self, *args, **kwargs):
        """
        Add a Matplotlib Line2D object to the layer.
        """
        self.lines.append(Line2D(*args, **kwargs))

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

    def add_data(self, *args):
        """
        Add data to the layer.

        First argument should be a list, tuple, or array of x data.
        Second argument should be a list, tuple or array of y data.
        Optional third argument should be a list, tuple, or array of z data.
        """
        self.x_data.append(args[0])
        self.y_data.append(args[1])
        try:
            self.z_data.append(args[2])
        except:
            pass

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
