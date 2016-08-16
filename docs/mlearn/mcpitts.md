# The McCulloch Pitts Neurons

This module provides an implementation of the McCulloch-Pitts model of
neural computation first proposed by Warren McCulloch and Walter Pitts in
1943. The constituent units of the model are called neurons and feature
binary inputs that act in either an excitatory or inhibitory fashion.
In short, the neurons act as logical threshold units and can be strung
together in such a way as to guarantee the functional completeness of the
resulting units. More info regarding the structure and operation of these
neurons can be found in the tutorial located at 
`retina/demos/mcculloch-pitts/McCulloch-Pitts Neurons.ipynb`.

---------------------------------------------------------------------------

## The `MPNeuron` Class

This class provides an implementation of the McCulloch-Pitts Neuron. It
relies on the `MPInput` class.

---------------------------------------------------------------------------

**Instance-Level Properties**

* `self.threshold`: The arithmetical threshold value of the unit. This is
the value that the sum of excitatory inputs must exceed in order for the
neuron to become excited.

* `self.inputs`: A list of `MPInput` objects that serve as the input 
triggers for the neurons.

---------------------------------------------------------------------------

**Instance-Level Functions**

---------------------------------------------------------------------------

`__init__(threshold, inputs)`

* `threshold`: The neuron's threshold value.
* `inputs`: A list of `MPInput` objects to serve as the input triggers for
the neuron.

---------------------------------------------------------------------------

`activate()`: Reads the current state(s) of the neuron's input(s) and 
returns 1 if the neuron is activated as a result and 0 otherwise.

---------------------------------------------------------------------------

## The `MPInput` Class

This class defines an input trigger for an `MPNeuron`. Inputs are
binary-valued and can be either excitatory or inhibitory in nature.

---------------------------------------------------------------------------

**Instance-Level Properties**

* `excitatory`: A boolean. `True` if the input is excitatory and `False` if
it is inhibitory.

* `value`: The current value of the input. Must be either 0 or 1.

---------------------------------------------------------------------------

**Instance-Level Functions**

`__init__(excitatory)`: Initializes either an excitatory or inhibitory input
based on the truth value of `excitatory`.

---------------------------------------------------------------------------

`trigger(value)`: Triggers the input, setting its value to the provided
`value` argument which should be only one of 0 or 1.

---------------------------------------------------------------------------

## The `Decoder` Class

This class allows for the construction of any desired logical function
based on a series of provided inputs and their desired truth values. In
the tutorial, it is used as part of a constructive proof of the functional
completeness of the McCulloch-Pitts computational model.

---------------------------------------------------------------------------

**Instance-Level Properties**

* `self.vectors`: The list of input vectors to be evaluated as `True` by
the returned decoder function. All other vectors are assumed to evaluate
to `False`.

* `self.vec_length`: The arity of the logic function to be produced. Mainly
used in checking for the validity of function arguments.

---------------------------------------------------------------------------

**Instance-Level Functions**

 `__init__(vectors)`: Initializes a decoder with the list of vectors to be
set as the `self.vectors` property.

---------------------------------------------------------------------------

`decode()`: Returns a logical function which evaluates the Decoder's vectors
to `True` and all other possible inputs to `False`.
