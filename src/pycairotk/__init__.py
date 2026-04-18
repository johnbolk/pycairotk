"""A Tkinter DrawArea wrapper class for the pycairo package.

This package provides graphics rendering classes and methods
which operate in a standard, right-handed coordinate system.
The default origin (0, 0) is located in the lower-left corner.

This package provides the following class and function definitions:

* DrawArea    - A Tkinter widget class for rendering and displaying graphics
* BorderStyle - A data class of the available border style options
* Brush       - A data class of graphics rendering options
* Font        - A data class for describing a text font
* TextStyle   - A data class of text rendering options
* Shape       - An enumerated class of available datapoint shapes
* LineCap     - An enumerated class of available line endpoint options
* LineJoin    - An enumerated class of available line junction options
* Antialias   - An enumerated class of available rendering options
* Size        - A named tuple of the width and height dimensions of an
* Vector      - A class which represents a geometric vector in the xy plane

* Color       - A data class of commonly used drawing colors
* rgba_color  - Generates a floating point RGBA color from integer values
"""

__version__ = '1.4.10'

from cairo import LineCap, LineJoin, Antialias
from .pycairotk import DrawArea, BorderStyle, Brush, Font, TextStyle, Shape, Size, Vector
from .pycolor import Color, rgba_color
