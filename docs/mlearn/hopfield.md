
# Hopfield Networks with Retina

As part of its machine learning module, Retina provides a full implementation of a general Hopfield Network along with classes for visualizing its training and action on data.
Historically speaking, the Hopfield Network was one of the first *Recurrent Neural Networks* and provided an early computational model of autoassociative memory. To learn more
about the network, we highly recommend [this exposition](https://page.mi.fu-berlin.de/rojas/neural/chapter/K13.pdf), due to Rojas. Furthermore, you can find our walkthrough of
the Retina implementation in the source folder `demos/mlearn/hopfield/Hopfield-Tutorial.ipynb`.

--------------------------------------------------------

## The Structure of Fovea's Machine Learning Utilities

The network implementation code is contained in `retina/mlearn/hopfield_network.py`. The file defines a single class, `HopfieldNetwork`, which is easily instantiated by a single call of the form `myNet = HopfieldNetwork(num_neurons)`. Optionally, a custom activation function can be supplied. The `num_neurons` argument specifies the number of neurons to be used internally by the network.

The file `visuals.py` contains the front-end code that defines a `VisualHopfield` network built on top of the `HopfieldNetwork` backend. The `VisualHopfield` network also relies on an internal `VisualNeuron` class which creates drawings of neurons and the connections between them. In its default form, `VisualHopfield` runs a detailed visual simulation of the Hopfield network training and learning on whatever data it's supplied. That said, each component of the visualization can easily be separated from the action of the others should your needs require a customized approach.

## The HopfieldNetwork Class

This class defines the Hopfield Network sans a visual interface. The class provides methods for instantiating the network, returning its weight matrix, resetting the network, training the network,
performing recall on given inputs, computing the value of the network's energy function for the given state, and more.

--------------------------------------------------------

**Class-Level Properties**

None at this time.

--------------------------------------------------------

**Class-Level Functions**

None at this time.

--------------------------------------------------------

**Instance-Level Properties**

`num_neurons`: The number of neurons contained in the network.
`_weights`: The network's weight matrix.

`_trainers`: A dictionary containing the available network training algorithms. At the time of writing the network supports Hebbian and Storkey training and the dictionary is

	{"hebbian": self._hebbian, "storkey": self._storkey}

`_recall_modes`: A dictionary containing the two different recall methods, `_synchronous` and `_asynchronous`.

	{"synchronous": self._synchronous, "asynchronous": self._asynchronous}

`_vec_activation`: A vectorized version of the network's activation function.

`_train_act`: A vectorized version of the activation function used in network training.

---------------------------------------------------------

**Instance-Level Functions**

`weights()`: A getter method that return's the network's weight matrix.

---------------------------------------------------------

`reset()`: Resets the network to an untrained state by making the weight matrix identically zero.

---------------------------------------------------------

`train(patterns, method="hebbian", threshold=0, inject=lambda x, y: None)`: Trains the network. 

`patterns`: The input data on which the network is to be trained.

`method`: Specifies the `self._trainers` key for the training algorithm to be used.

`threshold`: The threshold value for the network activation function.

`inject`: A function to call after each iteration of the training algorithm. Primarily used by the `VisualHopfield` class for updating the network drawing loop.

---------------------------------------------------------

`recall(patterns, steps=None, mode="asynchronous", inject=lambda x, y: None)`: This function should only be called after the network has been trained. Given an input
state the network attempts to "recall" the closest representative state seen during training. In other words, the network seeks to generalize the input state to one
from its internal "memory".

`patterns`: The input states to be recalled.

`steps`: The number of steps of the recall algorithm to be computed. This argument is unnecessary for *asynchronous* learning which is guaranteed to converge to some
final resting state, but is highly useful in avoiding infinite recursion in the case of *synchronous* learning.

`mode`: The dictionary key for `self._recall_modes` specifying the type of recall to be performed. Options are `"synchronous"` and `"asynchronous"`.

`inject`: Has the same purpose as the corresponding argument of the training function.

----------------------------------------------------------

`energy(state)`: Returns the value of the network's energy function applied to the given `state`.

----------------------------------------------------------

## The `VisualNeuron` Class

Provides a visual interpretation of a constituent neuron of a Hopfield Network. All calls to `VisualNeuron` are hidden internally within `VisualHopfied`, and it is unlikely that you will need to alter this class. That said, if you do decide to adjust the visualization of individual neurons to your own specifications you will need to be familiar with the following class specifics.

----------------------------------------------------------

**Class-Level Properties**

None at this time.

----------------------------------------------------------

**Class-Level Functions**

None at this time.

----------------------------------------------------------

**Instance-Level Properties**

`theta`: The angular component of the polar representation of the neuron's position within the `VisualHopfield` network diagram.

`r`: The radial component of the polar representation of the neuron's position within the `VisualHopfield` network diagram.

`x`: The x component of the cartesian representation of the neuron's position within the `VisualHopfield` network diagram.

`y`: The y component of the cartesian representation of the neuron's position within the `VisualHopfield` network diagram.

`connections`: A dictionary which tracks the connections between this neuron and other neurons within the Hopfield Network. The keys are

`VisualNeuron` objects and the values are the `Line2D` artists of the `VisualHopfield` network diagram.

----------------------------------------------------------

**Instance-Level Properties**

`draw(axes)`: Draws a neuron to the provided Matplotlib Axes instance.

----------------------------------------------------------

`draw_connection(neuron, connection_color, axes)`: Draws a connection between two neurons.

`neuron`: The terminal `VisualNeuron` of the connection.

`connection_color`: The color of the connection line to be drawn.

`axes`: The Matplotlib axes to which the connection should be drawn.

----------------------------------------------------------

`delete_connection(neuron)`: Deletes the connection between the calling `VisualNeuron` and the `VisualNeuron` specified by the `neuron` argument.

----------------------------------------------------------
## The VisualHopfield Class

This class is a wrapper to the `HopfieldNetwork` class which injects code for drawing and plotting various facets of the network dynamics
throughout the course of the network's operation. It subclasses `HopfieldNetwork`.

----------------------------------------------------------

**Class-Level Properties**

None at this time.

----------------------------------------------------------

**Class-Level Functions**

None at this time.

----------------------------------------------------------

**Instance-Level Properties**

`d_theta`: A theta increment value calculated as 2pi multiplied by the number of neurons in the network. Used for positioning `VisualNeuron`s in the
network diagram.

`neurons`: A list of the `VisualNeuron` objects associated with the network.

`cs_plot`: None

`training_data`: The user-provided training data.

`recall_data`: The user-provided recall data.

`cmap`: The Matplotlib colormap used in the weight matrix diagram.

`mode`: The current mode of the visualization, either "training" or "recalling".

`iteration`: A Matplotlib `Text` instance displaying the current iteration of the network in either the training or recalling method.

`network_fig`: The Matplotlib `Figure` instance which holds the Axes associated with the visualization.

`main_network`: The network diagram axes.

`energy_diagram`: The energy diagram axes.

`contour_diagram`: The energy contour diagram axes.

`weight_diagram`: The weight diagram axes.

`state_diagram`: The state diagram axes.

`view_wfbutton`: A Matplotlib `Button` used to toggle the wireframe view in the energy function diagram.

`view_attractbutton`: A Matplotlib `Button` used to toggle the plotting of attractors in the energy function diagram.

----------------------------------------------------------

**Instance-Level Functions**






## The `_setup_display` Function

The task of the `_setup_display` function is to construct the Matplotlib figure window and arrange its component axes. The figure is assigned to the instance attribute `self.network_fig` and can be accessed as such. The component axes are the following:

```
        self.main_network    --  Axes to which VisualNeurons and their connections are drawn.
        self.energy_diagram  --  The 3D axes in which the network's energy function is plotted.
        self.contour_diagram --  Axes to hold the contour plot of the network's energy function.
        self.state_diagram   --  Axes to which a checkerboard representation of the network's binary state is drawn.
        self.weight_diagram  --  Axes to hold a heatmap representation of the network's weight matrix.
```

The function also creates widgets to toggle layer visibility in the energy diagram and dynamic text labels that change based on the network's current mode (training or recalling) and iteration count within those methods.

## The `_draw_network` Function

This method uses a simple loop to draw the symmetric connections that occur between each of the network's neurons. Probably the most useful information that can be gleaned from the function is the significance of a connection's color. In our setup, connections having the weight 0 are colored green, the weight 1 colored blue, and the weight -1 colored red. You can change these colors to suit your preferences by altering the variable `colors`.

## The `_plot_state` Function

This method handles all of the plotting necessary for creating the network's state diagram. The network's "state" at any given point in time is the output of its recall function in response to an input vector. Since all network vectors are bipolar, we split its output vector at even intervals and use these vectors as the rows of a matrix. This matrix is converted to a black-and-white patchwork diagram using Matplotlib's `imshow` function.

**IMPORTANT:** Each state is a numpy array, and is converted to a matrix using the `state.reshape()` function. You will need to alter this call should you seek to visualize a network not having exactly 25 neurons as is used for the OCR example.

## The `_plot_weights` Function

This one is similar to `_plot_state` in its action and construction. The `imshow` map is used to create a colormap representation of the network's weight matrix. You can modify this method to change the colormap used.

## The `_set_mode` Function

Updates the network's "mode" text label based on the network's current operation: either training or recalling.

## The `_train_inject` Function

This function contains visualization code that is injected into the `HopfieldNetwork` base class' training method. Alter with care.

## The `_recall_inject` Function

Same as above, except for the network's recalling method. Alter with care, as well.

## The `_normalize_network` Function

This method serves one purpose: resetting the linewidth of those neuronal connections that were manipulated by the network during its training phase so as not to pollute with thickness the visual space.

## The `_plot_energy` Function

The `_plot_energy` function is probably the most involved method of the entire visualization, as there is a great deal of legwork that goes into creating a 3-dimensional representation of the energy landscape. For networks having $\geq 3$ neurons, the plot of the energy function will reside in 4 or more dimensions. In order to reduce this $n$-dimensional information to a 3-dimensional representation, we perform a 2D PCA transformation on the network's training data. If we treat these PCA axes as our x and y axes and the energy value as the z-axis, we are able to plot the energy function accordingly.

This function, in fact, contains three plot artists in three different layers. The first layer contains the network's attractors, plotted in a scatter plot as green markers. The second layer contains a wireframe plot of the energy landscape onto which the attractor markers can be overlaid. The third layer contains the energy landscape plotted as a surface.
