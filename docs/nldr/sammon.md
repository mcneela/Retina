# The Sammon Mapping Module

This module implements the Sammon Mapping algorithm for non-linear
dimensionality reduction. The implementation used is based off a Matlab
version given by Gavin C. Cawley, the source of which can be found 
[here](https://people.sc.fsu.edu/~jburkardt/m_src/profile/sammon_test.m).

Essentially, the algorithm works by defining a metric on high-dimensional
source data and then seeking to reconstruct a set of low-dimensional 
projected data such that the pairwise distances given by this metric are
well-preserved by the projection metric.

---------------------------------------------------------------------------

`sammon(data, target_dim=2, max_iterations=250, max_halves=10)`

* `data`: The source data array in which rows are patters and columns are features.
* `target_dim`: The dimension of the target projection space.
* `max_iterations`: The maximum number of iterations of the algorithm to run.
* `max_halves`: The maximum number of step halvings.
