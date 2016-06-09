from abc import ABCMeta, abstractmethod
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.projections import projection_registry
import matplotlib.pyplot as plt
from layer import *

class Fovea(metaclass=ABCMeta):
    
    @property
    @abstractmethod
    def layers(self):
        pass

    @property
    def active_layer(self):
       pass

    @active_layer.setter
    @abstractmethod
    def active_layer(self, layer):
       pass

    @abstractmethod
    def add_layer(self, layer, **kwargs):
       pass

    @abstractmethod
    def get_layer(self, layer):
        pass

    @abstractmethod
    def save_layer(self, layer, *args, **kwargs):
        pass

    @abstractmethod
    def delete_layer(self, layer):
       pass

    @abstractmethod
    def build_layer(self, layer, **kwargs):
       pass

    @abstractmethod
    def build_layers(self):
       pass


class Fovea2D(Fovea, Axes):
    name = 'Fovea2D'

    def __init__(self, *args, **kwargs):
        Axes.__init__(self, *args, **kwargs)
        self._layers = {}
        self._active_layer = None
        self._tracker = None

    @property
    def layers(self):
        return self._layers

    @property
    def active_layer(self):
        return self._active_layer

    @active_layer.setter
    def active_layer(self, layer):
        self._active_layer = layer

    def add_layer(self, layer, **kwargs):
        try:
            self._layers[layer]
            print("Layer already exists.")
            return
        except:
            layer_obj = Layer(layer, **kwargs)
            self._layers[layer] = layer_obj
            setattr(self, layer, layer_obj)

    def get_layer(self, layer):
        return self._layers[layer]

    def save_layer(self, layer, *args, **kwargs):
        reshow = set()
        for name, layer_obj in self._layers.items():
            if name == layer:
                continue
            elif layer_obj.visible:
                reshow.add(layer_obj)
                layer_obj.hide()
        plt.savefig(*args, **kwargs)
        for layer_obj in reshow:
            layer_obj.show()

    def delete_layer(self, layer):
        del self._layers[layer]

    def build_layer(self, layer=None, **kwargs):
        if not layer:
            layer = self._active_layer
        else:
            layer = self._layers[layer]
        if not 'plot' in kwargs:
            plot = self.plot
            try:
                for (x, y) in zip(layer.x_data, layer.y_data):
                    layer.plots.append(plot(x, y,
                                            layer.style,
                                            **kwargs))
            except:
                pass
        if layer.lines:
            for line in layer.lines:
                self.add_line(line)
        if not layer.visible:
            layer.hide()

    def build_layers(self):
        self.cla()
        for layer in self._layers.keys():
            self.build_layer(layer)

class Fovea3D(Fovea2D, Axes3D):
    name = 'Fovea3D'

    def __init__(self, *args, **kwargs):
        Axes3D.__init__(self, *args, **kwargs)
        self._layers = {}
        self._active_layer = None
        self._tracker = None

    def build_layer(self, layer, plot=None, **kwargs):
        if not layer:
            layer = self._active_layer
        else:
            layer = self._layers[layer]
        if not plot:
            plot = self.plot
        try:
            layer.plot = plot(layer.x_data, layer.y_data, layer.z_data,
                              layer.style, **kwargs)
        except:
            pass
        if layer.lines:
            for line in layer.lines:
                self.add_line(line)
        if not layer.visible:
            layer.hide()

projection_registry.register(Fovea2D)
projection_registry.register(Fovea3D)
