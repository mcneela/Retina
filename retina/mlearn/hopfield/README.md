Included in this directory is a visualization of a Hopfield Network applied to an example in character recognition.

The file `hopfield_network.py` contains the definition of the `HopfieldNetwork` class. 
Using this class, Hopfield Networks containing any desired number of constituent neurons can be constructed from scratch. 
The given network implementation provides the following methods intended for the end user:

	weights() 						Returns the network's current weight matrix.
	
	reset()							Resets the network's weight matrix so that the network can be retrained on new data.

	train(patterns,					Trains the network on a series of input states passed as "patterns." Two training methods
		  method="hebbian",			are provided: hebbian and storkey.
		  threshold=0,
		  inject=lambda x: None)

	learn(patterns,					Causes the network to classify the states given by "patterns" based on the states upon
		  steps=None,				which it was trained. Two learning methods are provided: synchronous and asynchronous.
		  mode="asynchronous",		Synchronous learning is the faster of the two, but is not guaranteed to converge.
		  inject=lambda x: None)	Asynchronous learning is rather slow, but is guaranteed to converge to a local low-energy state.

	energy(state)					Calculates the energy associated with the given state.

The file `visuals.py` contains the code for running the network visualization and all associated helper functions for drawing
individual components of that visualization to the Matplotlib canvas. The primary definition of the file is that of the
`VisualHopfield` class. This defines a "visual" Hopfield Network that subclasses the implementation given in hopfield_network.py.

The only method from this class which end users should concern themselves with is `run_visualization(training_data, learning_data=None)`.
This method calls on all the internally-defined helper methods to run a full visualization of the network training on the provided
`training_data` and learning the provided `learning_data`. Thus to run the visualization, do the following...

	$ python -i visuals.py
	
	>>> myNet = VisualHopfield(num_neurons)			# Replace num_neurons with your desired number of neurons.

	>>> training_data = [your_data_here]			# Construct a list of training_data

	>>> learning_data = [learning_data_here]		# Optionally, construct a list of learning data.

	>>>	myNet.run_visualization(training_data, learning_data)

Alternatively, to view the visualization as applied to an example in character recognition, run the ocr.py script.

In this example, the network is trained on an alphabet of letters represented as a 5x5 binary configuration of X's
and .'s. An X corresponds to a 1, and a . to a 0. This alphabet can be viewed in the alphabet.py file. Below the
letters A-Z are defined two letters for which the network is to learn a correct representation. Ideally, the network
should converge to one of A-Z when these "messy" letters are given to the network for learning. However, it is often
the case that the network will view these letters as an amalgam of some two of A-Z and will converge to a spurious
state accordingly.

There are five subplots associated with the network visualization:

1. The first of these is the main network diagram. This displays each neuron as a circle connected to every other
   neuron in the network as is the convention within the Hopfield paradigm. A green line between two neurons
   represents a connection of weight 0, a blue line a connection of weight 1, and a red line a connection of weight -1.
   During the training portion of the visualization, the connections that are in the process of being altered in response
   to training data are highlighted by way of a thicker linewidth and change in color in tandem with the changing of the
   network's weight matrix.

2. Next is the energy function diagram. This provides a plot of the network's energy landscape after it has been trained.
   Since for nearly all cases the network state vectors are of dimension greater than three, the energy landscape is calculated
   by applying the network's energy function to the two-dimensional PCA axes of the network's training vectors. The energy
   function provides a measure of the error at each state of the network. Minima in the energy landscape correspond to system attractors,
   and ideally the only attractors should be those states which the network was trained on. However, due to the complexity of
   the network and the energy landscape, many extraneous local minima exist, called "spurious states," to which the network
   might unwittingly converge. For this reason, sometimes the smaller the training dataset the better the results.

3. Third is a contour plot of the energy landscape. This is self-explanatory.

4. Fourth is a binary visualization of the current network state. When fed a state vector during learning, the network uses
   the weight matrix acquired during training to manipulate it. Because the Hopfield Network is an RNN, it maintains a primitive
   "memory" of those states which it has seen during training. The ideal behavior of the network is to modify each state vector
   that it is presented with until it converges to the most similar state presented during training. Unfortunately, this behavior
   is not always achieved as mentioned in the discussion of spurious states, above.

5. Finally, the visualization displays a heatmap representation of the network's weight matrix at each stage in the training
   process. The values of each entry in the weight matrix can be gleaned from comparing the corresponding coordinate's color
   to the heatmap colorbar located to the right of the diagram.
