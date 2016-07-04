<style TYPE="text/css">
code.has-jax {font: inherit; font-size: 100%; background: inherit; border: inherit;}
</style>
<script type="text/x-mathjax-config">
MathJax.Hub.Config({
    tex2jax: {
        inlineMath: [['$','$'], ['\\(','\\)']],
        skipTags: ['script', 'noscript', 'style', 'textarea', 'pre'] // removed 'code' entry
    }
});
MathJax.Hub.Queue(function() {
    var all = MathJax.Hub.getAllJax(), i;
    for(i = 0; i < all.length; i += 1) {
        all[i].SourceElement().parentNode.className += ' has-jax';
    }
});
</script>
<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML"></script>s

# An Introduction to the Restricted Boltzmann Machine

## Background

In a previous tutorial we took a look at the Hopfield network, a recurrent neural network
characterized by the symmetry of its connections, the bipolarity of its states, and the 
nature of its convergence  - which can be typified by the topology of its energy landscape.

Today, we will investigate a machine learning model that is the stochastic counterpart of the
Hopfield network. We say that the network is stochastic because its behavior is based on the
assigning of probabilities to different states of the network. More on that later. The model
with which we will concern ourselves is a type of Boltzmann Machine, more specifically, a
Restricted Boltzmann Machine. Like the Hopfield network, the RBM is an unsupervised learner,
 i.e. it is capable of learning from data that is unlabelled.

## The States of an RBM and Recurrence Between Layers

Like the Hopfield network, the Restricted Boltzmann Machine possesses some predefined number of
binary internal units, called *neurons*; however, in the case of RBMs, these units are partitioned
into two groups, called the *hidden* and *visible* layers. The network is configured such that if
we treat neurons as vertices and connections between them as edges, the visible and hidden layers
form a bipartite graph. This means that connections only exist between neurons in different layers,
i.e. no intra-layer connections are present. The definition of the RBM further strengthens this
condition by specifying that in fact each hidden neuron is bidirectionally connected to every visible
neuron and vice-versa. This is where we see the recurrence of the RBM. Similar to the Hopfield network,
the connections *between layers* are symmetric and information feeds both backwards and forwards through
these causeways.

Now, let's return to the formal mathematical specification of the network layers. It is atop these layers
that the stochasticity of the network is built. While each neuron within a layer is just a binary state, we can
construct two vectors representing the configuration of visible and hidden states in their totality
as

### Define Hidden and Visible Vectors HERE!

$$\begin{align}
  v &= \begin{bmatrix}
    v_{1} \\
	v_{2} \\
	\vdots \\
	v_{m}
	\end{bmatrix}
$$

where our network consists of $m$ visible neurons and $n$ hidden neurons. Each $v_i, h_j$ gives the
value of the corresponding neuron, either a 0 or 1. However, the vectors $v$ and $h$ when viewed in
their entirety are treated as *random variables* that can take on any of $2^m$ or $2^n$ possible 
configurations, respectively. What our network seeks to encode, then, is just a


Normally, the neurons of the visible
layer are associated with the features of your dataset on which you'd like to train. For example,
suppose you wanted to use an RBM to perform dimensionality reduction on a three-dimensional data
set. Each of the x, y, and z components of your data vectors would be a feature which you'd like
to capture in your training. Thus, you would need to define an RBM possessing a 
