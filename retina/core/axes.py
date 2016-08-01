import matplotlib.pyplot as plt
from abc import ABCMeta, abstractmethod
from future.utils import with_metaclass
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
from retina.core.layer import Layer2D, Layer3D
from retina.core.py2 import *

class Fovea(with_metaclass(ABCMeta, object)):
    """
    Abstract base class specifying standard layer methods
    that all Fovea subclasses should implement.
    """
    @property
    @abstractmethod
    def layers(self):
        """
        Each axes should have a dictionary of associated layers.
        """
        pass

    @property
    def active_layer(self):
        """
        Each axes should have an active layer attribute.
        """
        pass

    @active_layer.setter
    @abstractmethod
    def active_layer(self, layer):
        """
        Each axes should provide a means for setting the
        active layer attribute.
        """
        pass

    @abstractmethod
    def add_layer(self, layer, **kwargs):
        """
        Each axes should implement a method for adding
        layers to itself.
        """
        pass

    @abstractmethod
    def get_layer(self, layer):
        """
        Each axes should allow a user to get the Layer
        object associated with an axes layer.
        """
        pass

    @abstractmethod
    def save_layer(self, layer, *args, **kwargs):
        """
        Each axes should provide a means for saving the
        artists in a layer to an image file or pdf.
        """
        pass

    @abstractmethod
    def delete_layer(self, layer):
        """
        Each axes should allow for the deleting of
        individual layers.
        """
        pass

    @abstractmethod
    def build_layer(self, layer, **kwargs):
        """
        Each axes should provide a means for building
        a single layer.
        """
        pass

    @abstractmethod
    def build_layers(self):
        """
        Each axes should implement a method allowing all
        layers to be built simultaneously using default
        settings.
        """
        pass


class Fovea2D(Fovea, Axes):
    """
    A class providing layer functionality to standard,
    2D axes. Inherits from matplotlib.axes.Axes.
    """
    name = 'Fovea2D'

    def __init__(self, *args, **kwargs):
        Axes.__init__(self, *args, **kwargs)
        self._layers = {}

    @property
    def layers(self):
        """
        self._layers 'getter' method.
        """
        return self._layers

    @property
    def active_layer(self):
        """
        self._active_layer 'getter' method.
        """
        return self._active_layer

    @active_layer.setter
    def active_layer(self, layer):
        """
        self._active_layer 'setter' method.
        """
        self._active_layer = layer

    def add_layer(self, layer, **kwargs):
        """
        Method to add a layer to the axes.

        **kwargs are passed to Layer constructor.
        """
        try:
            # Check to see if layer already exists.
            self._layers[layer]
            print("Layer already exists.")
            return
        except:
            # If layer does not exist, a new layer
            # object is instantiated and tracked
            # by the axes' layers dictionary.
            layer_obj = Layer2D(layer, self, **kwargs)
            self._layers[layer] = layer_obj
            setattr(self, layer, layer_obj)
            return layer_obj

    def get_layer(self, layer):
        """
        Gets the Layer object associated with the
        key 'layer' in the axes layers dictionary.
        """
        return self._layers[layer]

    @py2plot
    def save_layer(self, layer, *args, **kwargs):
        """
        Saves a snapshot of the artists in 'layer'
        to an image file or pdf.

        *args and **kwargs are passed to
        matplotlib.pyplot.savefig(). Documentation
        can be found here:
            
        http://matplotlib.org/api/pyplot_api.html
        
        """
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

    @py2plot
    def showcase(self, layer):
        """
        Sets `layer` to visible and hides all other
        axes layers.
        """
        show_layer = self._layers[layer]
        for layer_obj in self._layers.values():
            if layer_obj is show_layer:
                layer_obj.show()
            else:
                layer_obj.hide()

    def delete_layer(self, layer):
        """
        Deletes the Layer object
        associated with `layer`.
        """
        del self._layers[layer]

    @py2plot
    def build_layer(self, layer=None, *args, **kwargs):
        """
        Build and render a single axes layer.
        This method must be called after applying certain
        changes to a layer object such as setting the style.

        The most importang kwarg is `plot` which specifies
        the pyplot function used to plot the layer data.
        Possible options include `scatter` and `contour`.
        Plot defaults to the built-in plotting function.
        """
        if not layer:
            layer = self._active_layer
        else:
            layer = self._layers[layer]
        if not 'plot' in kwargs:
            plot = self.plot
        else:
            plot = kwargs['plot']
            del kwargs['plot']
        try:
            for (x, y) in zip(layer.x_data, layer.y_data):
                layer.plots.append(
                                   plot(x, y, *args, **kwargs)
                                  )
        except:
            pass
        if layer.lines:
            for line in layer.lines:
                self.add_line(line)
        if not layer.visible:
            layer.hide()
        if layer.patches:
            for patch in layer.patches:
                self.add_patch(patch)

    def build_layers(self):
        self.cla()
        for layer in self._layers.keys():
            self.build_layer(layer)

class Fovea3D(Fovea2D, Axes3D):
    """
    A class providing layer functionality for Matplotlib's
    3D axes. Supports most of the same methods as Fovea2D,
    although certain Layer attributes such as `add_hline`,
    `add_vline`, and `add_line` are not supported.
    """
    name = 'Fovea3D'

    def __init__(self, *args, **kwargs):
        Axes3D.__init__(self, *args, **kwargs)
        self._layers = {}
        self._active_layer = None
        self._tracker = None

    def add_layer(self, layer, **kwargs):
        """
        Method to add a layer to the axes.

        **kwargs are passed to Layer constructor.
        """
        try:
            # Check to see if layer already exists.
            self._layers[layer]
            print("Layer already exists.")
            return
        except:
            # If layer does not exist, a new layer
            # object is instantiated and tracked
            # by the axes' layers dictionary.
            layer_obj = Layer3D(layer, self, **kwargs)
            self._layers[layer] = layer_obj
            setattr(self, layer, layer_obj)
            return layer_obj

    @py2plot
    def build_layer(self, layer, plot=None, **kwargs):
        """
        Build and render a single axes layer.
        This method must be called after applying certain
        changes to a layer object such as setting the style.

        The most importang kwarg is `plot` which specifies
        the pyplot function used to plot the layer data.
        Possible options include `scatter` and `contour`.
        Plot defaults to the built-in plotting function.
        """
        if not layer:
            layer = self._active_layer
        else:
            layer = self._layers[layer]
        if not plot:
            plot = self.plot
        try:
            for x, y, z in zip(layer.x_data, layer.y_data, layer.z_data):
                layer.plots.append(
                                   plot(x, y, z, **kwargs)
                                  )
            
        except:
            pass
        if layer.lines:
            for line in layer.lines:
                self.add_line(line)
        if layer.patches:
            for patch in layer.patches:
                self.add_patch(patch)
        if layer.planes:
            for plane in layer.planes:
                layer.plots.append(
                    self.plot_surface(plane[0], plane[1], plane[2], **kwargs)
                )
        if not layer.visible:
            layer.hide()
