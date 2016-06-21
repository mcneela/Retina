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
