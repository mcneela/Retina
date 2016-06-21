# Using Fovea to Visualize Non-Linear Dimensionality Reduction

## Introduction

The process of non-linear dimensionality reduction involves taking
data of some pre-determined dimensionality (usually of dimension three 
or greater) and applying some transformation to it such that it is projected
onto a topological space of lower dimension. The goal in applying such a 
transformation is to make visualization of the data easier while retaining
its key, structural attributes. There are a number of currently established
algorithms that perform nldr, and each facilitates its own set of strengths
and weaknesses. For this demonstration, we will use the default Locally Linear
Embedding algorithm provided with Scikit-Learn to perform the backend dimensionality
reduction, and subsequently visualize the transformed data using Fovea's suite
of tools.

## The Dataset

For this example, we will perform dimensionality reduction on the Swiss Roll
dataset, aptly named given its resemblance to the Swiss Roll cake. This data
is commonly used in evaluating the performance of nldr algorithms as it exhibits
a high degree of structured non-linearity. Pictured here is the dataset with
a rainbow-like Matplotlib colormap applied.

![Swiss Roll 3D](swiss_roll.png "Swiss Roll")  

## Performing the Reduction

The first step in creating our visualization involves generating the Swiss Roll data
and applying the Locally Linear Embedding transformation to that data. To do this,
we will import scikit-learn into our project. The modules relevant to the task at hand
are `manifold` and `datasets`:

    from sklearn import manifold, datasets

Next, we will conjure the Swiss Roll data

    X, color = datasets.samples_generator.make_swiss_roll(n_samples=1500)

In the datasets module, `sample_generator` is a class that provides a number of utility
functions for generating interesting sets of data. The class' `make_swiss_roll` function does
exactly as expected: generates a 3D swiss roll dataset. The function returns two items.
The first, `X`, is an n x 3 array of points residing in the dataset, where `n = n_samples`. The second
is a 1 x n array of the relative positions of each row in `X`. It is this sort of relational
data that we need in order to apply a Matplotlib colormap to the roll, so we call it `color`. 

Now that we have our data, we can apply the LLE transformation to it. Since our source data
makes use of three dimensions, we will make our target topological space have dimension two.
The reduction can be performed painlessly by a single call to scikit-learns `manifold.locally_linear_embedding`
like so:

    X_r, err = manifold.locally_linear_embedding(X, n_neighbors=12,
                                                 n_components=2)

The arguments to the LLE function are `X`: the dataset to be reduced, `n_neighbors`: the number
of neighboring points that the algorithm should use in performing its reduction, and `n_components`:
the dimension of the target topological space. The function returns the reduced dataset (`X_r`) and
the error (`err`) induced by the LLE algorithm. For the purposes of our demonstration, we will not
make use of the error variable, but it can be useful in evaluating the success of the LLE algorithm
when applied to your data.


