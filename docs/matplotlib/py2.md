# Python 2 Compatibility

The `py2.py` file in the `retina.core` module provides a wrapper function which
checks the version of Python being used to run any Retina Matplotlib script. If
it is found that the user is working with some iteration of Python 2, the wrapper
slips in a call to Matplotlib's `plt.show()` after all relevant plotting commands.
It is unclear to the Retina developers why this is necessary, but there seems to
be some differences between Python 2 and Python 3 in the way in which Matplotlib
 handles the interactive generation and manipulation of plots.

