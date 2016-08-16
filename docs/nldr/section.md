# The Sectioning Module

This module provides utility function that allows you to section, divide,
and prepare your data in unique ways for visualization via a non-linear
dimensionality reduction algorithm. 

---------------------------------------------------------------------------

## Utility Functions

---------------------------------------------------------------------------

`section(data, num_sections)`
	
* `data`: The data array to be sectioned.
* `num_sections`: The number of sections into which to partition the array.

This function indexes along the rows of the `data` array and partitions
the array into the desired number of sections and returning them.

---------------------------------------------------------------------------

`ordered_section(data, num_sections, axis=0)`

* `data`: The data array to be sectioned.
* `num_sections`: The number of sections into which to partition the array.
* `axis`: The axis (column) along which to partition the array. Typically,
the first column of the array holds x data, the second column y data, the
third column z data, and so on and so forth for higher dimensional data.

Performs the same function as `section` but first sorts the array along
the provided axis (column).

---------------------------------------------------------------------------

`progressive_segment(data, num_iterations, axis=0)`

* `data`: The data array to be sectioned.
* `num_iterations`: Indirectly specifies the segment size increment.
* `axis`: The axis (column) along which to segment. 

Partitions the array into segments of increasing length, starting from the
first row. First sorts the array rows along the specified axis.

---------------------------------------------------------------------------

`converge_segment(data, num_iterations, axis=0)`

* `data`: The data array to be sectioned.
* `num_iterations`: Indirectly specifies the segment size increment.
* `axis`: The axis (column) along which to segment.

Returns segments of the `data` array sorted along the column given by `axis`. These segments start along the first and last row and increase in size
until they converge upon the middle of the `data` array.
