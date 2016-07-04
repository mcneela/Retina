# An Introduction to Restricted Boltzmann Machines

## Background

In a previous tutorial we took a look at the Hopfield network, a recurrent neural network
characterized by the symmetry of its connections, the bipolarity of its states, and the 
nature of its convergence  - which can be typified by the topology of its energy landscape.

Today, we will investigate a machine learning model that is the stochastic counterpart of the
Hopfield network. We say that the network is stochastic because its behavior is based on the
assigning of probabilities to different states of the network. More on that later. The model
with which we will concern ourselves is a type of Boltzmann Machine, more specifically, a
Restricted Boltzmann Machine.

## The States of an RBM and Recurrence Between Layers

Like the Hopfield network, the Restricted Boltzmann Machine possesses some predefined number of
binary internal units, called *neurons*; however, in the case of RBMs, these units are partitioned
into two groups, called the *hidden* and *visible* layers. Normally, the neurons of the visible
layer are associated with the features of your dataset on which you'd like to train. For example,
suppose you wanted to use an RBM to perform dimensionality reduction on a three-dimensional data
set. Each of the x, y, and z components of your data vectors would be a feature which you'd like
to capture in your training. Thus, you would need to define an RBM possessing a 
