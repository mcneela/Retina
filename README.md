# Retina: Scientific Visualization with Python, Matplotlib, Plotly, and the Jupyter Notebook

This repository serves as a compendium of the work I've done over the course of
Google Summer of Code 2016. The entirety of the code in the repo was
written by me, with the exception of the PCA demo located [here](demos/dim_reduction)
and the Calc Context module located [here](retina/core/calc_context.py),
 both of which were ported from the Fovea package upon which this
project is based. Also included as a dependency is the full source of the SemanticUI 
framework [here](retina/web/api/semantic), which is not of my own creation.

A full list of my commits to this repository can be viewed 
[here](https://github.com/mcneela/Retina/commits/master?author=mcneela).

Near the beginning of GSOC, I also commited to the original Fovea repository.
Those commits can be viewed 
[here](https://github.com/robclewley/fovea/commits/master?author=mcneela).

The main thematic focus of my project was on the implementation, application,
and visualization of recurrent neural networks. Toward this end, I have created
my own versions of both classic and recently-developed recurrent computational models,
namely the Hopfield Network, the Restricted Boltzmann Machine, and the
McCulloch-Pitts Neurons. I have also created a number of Jupyter notebook-based
 tutorials demonstrating the use and visualization of these models.

My project also focused on non-linear dimensionality reduction algorithms.
Although my original proposal included the implementation of a few of these
algorithms as deliverables, I found that most could already be found in
well-developed packages such as Scikit-Learn. As such, I implemented a
single NLDR algorithm called Sammon Mapping, and directed the remainder of
my focus towards creating tools to assist in the visualization of the procedural
action of these NLDR methods.

Perhaps the most significant contribution I made to Fovea was the complete
overhaul of its design and plotting framework. Prior to my revisions, Fovea
was set up as a large, class-based structure for tracking, accessing, and modifying
Matplotlib Axes and Artist attributes. While the package functioned well,
the API was, at times, unintuitive. Fovea overrode a number of key Matplotlib
methods in a sometimes confusing and undocumented way, which made learning its
operational syntax and semantics quite challenging. Moreover, the package in many
cases served as merely a thin layer to already sound Matplotlib functionality
and incurred unnecessary runtime overhead as a result.

In order to address these issues, I redesigned Fovea from the ground up based
on object-oriented principles. The main Fovea classes now subclass and
inherit from their Matplotlib counterparts. They run faster, are called more
succinctly, and write cleaner than before. Over the course of the summer, I
streamlined the majority of Fovea's existing functionality into comparable
modules in Retina, and pared down Fovea's thousands of lines of code to a mere
few hundred lines in Retina.

In addition to these performance and design enhancements, I also created a Javascript
and Plotly-based framework for using Fovea in the browser. I implemented an
interface to this new code via Splinter which allows users to
plot in the browser with Python. While various issues have arisen throughout
the process of designing a browser-based mechanism for plotting, in many respects due
 to the nascency of current open-source development in this area, the code which
I have created implements all of Fovea's current core functionality and
provides a promising point of continuation for future development. 

For all of the work I created, I produced numerous demos and tutorials demonstrating
how to use the new features in code. These can be found
[here](/demos).

Furthermore, I have created documentation of the project's API which can be viewed
[here](http://retina.readthedocs.io)

I am excited by the work I have produced over the course of GSOC 2016, and look
forward to seeing the development of Fovea continue to progress in the future.
