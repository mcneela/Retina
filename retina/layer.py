import matplotlib
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt

class Layer:
    default_style = 'b-'

    @classmethod
    def set_default_style(cls, style):
        cls.default_style = style
    
    def __init__(self, name, **kwargs):
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
        if hasattr(val, method_name):
            try:
                method = getattr(val, method_name)
                method(*args, **kwargs)
            except:
                pass

    def _is_iterable(self, value):
        return hasattr(value, "__iter__") and not isinstance(value, str) 

    def _method_loop(self, method_name, iterable, *args, **kwargs):
        for val in list(iterable):
            if self._is_iterable(val):
                self._method_loop(method_name, val, *args, **kwargs)
            else:
                self._try_method(val, method_name, *args, **kwargs)

    def _set_visibility(self, boolean):
        self._method_loop("set_visible", self.__dict__.values(), boolean)

    def show(self):
        self._set_visibility(True)
        self.visible = True

    def hide(self):
        self._set_visibility(False)
        self.visible = False

    def add_line(self, *args, **kwargs):
        self.lines.append(Line2D(*args, **kwargs))

    def add_vline(self, x):
        ymin, ymax = plt.ylim()
        try:
            vline = plt.vlines(x, ymin, ymax)
            self.vlines.append(vline)
        except:
            print("Vertical lines are not supported by this Axes type.")

    def add_hline(self, y):
        xmin, xmax = plt.xlim()
        try:
            hline = plt.hlines(y, xmin, xmax)
            self.hlines.append(hline)
        except:
            print("Horizontal lines are not supported by this Axes type.")

    def set_style(self, style):
        self.style = style

    def add_data(self, *args):
        self.x_data.append(args[0])
        self.y_data.append(args[1])
        try:
            self.z_data.append(args[2])
        except:
            pass

    def add_attrs(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def clear(self):
        for key in self.__dict__.keys():
            self.__dict__[key] = None
        self.__dict__.update(self.default_attrs)
