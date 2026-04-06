"""A Tkinter DrawArea wrapper class for the pycairo package.

This module provides graphics rendering classes and methods
which operate in a standard, right-handed coordinate system.
The default origin (0, 0) is located in the lower-left corner.

This module provides the following class definitions:

* DrawArea    - A Tkinter widget class for rendering and displaying graphics
* BorderStyle - A data class of the available border style options
* Brush       - A data class of graphics rendering options
* Font        - A data class for describing a text font
* TextStyle   - A data class of text rendering options
* Shape       - An enumerated class of available datapoint shapes
* LineCap     - An enumerated class of available line endpoint options
* LineJoin    - An enumerated class of available line junction options
* Antialias   - An enumerated class of available rendering options
* Size        - A named tuple of the width and height dimensions of an object
* Vector      - A class which represents a geometric vector in the xy plane
"""

__version__ = '1.4.8'

import enum
import math
import warnings
import platform
import tkinter as tk
from dataclasses import dataclass, replace, field
from typing import Any, List, Tuple, Union, Optional, NamedTuple, Sequence
import cairo
import numpy as np
from PIL import Image, ImageTk, ImageColor

# pylint: disable=no-name-in-module
from cairo import Antialias, FontSlant, FontWeight, LineCap, LineJoin


@dataclass
class Brush:
    """The graphics rendering options data class.

    Attributes
    ----------
    width : float
        The width of the displayed line/arc segment or the datapoint size
    color : str | tuple
        The color of a line/arc segment, perimeter, or the solid fill color
    fill : bool
         If True, the polygon is filled with solid color, default is False
    edge : str | tuple
        The perimeter color of the solid filled polygon, default is no color
    dash : list | tuple
        The dash pattern of the line/arc segment, default is a solid line
    line_cap: LineCap
        The shape of a line/arc segment's end caps, default is LineCap.BUTT
    line_join : LineJoin
        The polygon's perimeter joining style, default is LineJoin.MITER
    """

    width: float = 1.0
    color: Union[str, tuple] = 'black'
    fill: bool = False
    edge: Union[str, tuple] = ''
    dash: Union[list, tuple] = ()
    line_cap: LineCap = LineCap.BUTT
    line_join: LineJoin = LineJoin.MITER

    @property
    def line_width(self) -> float:
        """Get the displayed region perimeter line width."""
        return -1 if (self.fill and not self.edge) else self.width

    @property
    def line_color(self) -> Union[str, tuple]:
        """Get the displayed region perimeter line color."""
        return self.edge if self.fill else self.color

    def copy(
        self,
        width: Optional[float] = None,
        color: Optional[Union[str, tuple]] = None,
        fill: Optional[bool] = None
    ) -> 'Brush':
        """Make a deep copy with optional new width, color, and/or fill values.

        Parameters
        ----------
        width : float, optional
            The new width assigned to the copy, default is the original width
        color : str | tuple, optional
            The new color assigned to the copy, default is the original color
        fill : bool, optional
            The new fill assigned to the copy, default is the original fill
        """
        new_width = self.width if width is None else width
        new_color = self.color if color is None else color
        new_fill = self.fill if fill is None else fill
        # noinspection PyTypeChecker
        return replace(self, width=new_width, color=new_color, fill=new_fill)


@dataclass
class Font:
    """The text font description class.

    Attributes
    ----------
    family : str
        The font family name as a string, default is 'Arial'
    height : float
        The font height (in pixels), default is 12.0
    bold : bool
        Boldface text if True, otherwise normal text, default is False
    italic : bool
        Italic text if True, otherwise upright text, default is False
    """

    family: str = 'Arial'
    height: float = 12.0
    bold: bool = False
    italic: bool = False


@dataclass
class TextStyle:
    """The text rendering options data class.

    Attributes
    ----------
    font : tuple
        The font of the displayed text, default is Font()
    color : str | tuple
        The color of the displayed text, default is 'black'
    anchor : str
        The anchor point of the displayed text, default is tk.LEFT
    angle : float
        The orientation angle (measured in degrees), default angle is 0.0
    border_width: float
        A positive value displays outlined text, default is -1.0
    """

    font: Font = field(default_factory=Font)
    color: Union[str, tuple] = 'black'
    anchor: str = tk.LEFT
    angle: float = 0.0
    border_width: float = -1.0


class Shape(enum.IntEnum):
    """The available datapoint shape options."""

    CIRCLE = 0
    DIAMOND = 1
    SQUARE = 2
    TRIANGLE = 3


@dataclass(frozen=True)
class BorderStyle:
    """The available border style options for the DrawArea.

    Attributes
    ----------
    Raised
        The DrawArea appears raised above the background.
    Sunken
        The DrawArea appears recessed into the background.
    Groove
        The DrawArea has a carved groove border.
    Ridge
        The DrawArea has a raised ridge border.
    Solid
        The DrawArea has a simple solid border.
    Flat
        The DrawArea appears flat, no border.
    """

    Raised = tk.RAISED
    Sunken = tk.SUNKEN
    Groove = tk.GROOVE
    Ridge = tk.RIDGE
    Solid = tk.SOLID
    Flat = tk.FLAT


class Size(NamedTuple):
    """The width and height dimensions of an object."""

    width: float
    height: float


class Vector:
    """A class which represents a geometric vector in the xy plane.

    Attributes
    ----------
    x : float
        The x-axis component of the vector
    y : float
        The y-axis component of the vector
    """

    x: float
    y: float

    def __init__(self, x: float, y: float):
        """Construct a new vector from the x & y vector components.

        Parameters
        ----------
        x : float
            The x-axis component of a vector
        y : float
            The y-axis component of a vector
        """
        self.x = x
        self.y = y

    @classmethod
    def from_polar_coords(cls, length: float, angle: float) -> 'Vector':
        """Construct a new vector using polar coordinate values.

        Parameters
        ----------
        length : float
            The length (or magnitude) of the vector
        angle : float
            The angle (or direction) of the vector (measured in degrees)

        Returns
        -------
        Vector
            The newly created vector
        """
        angle = math.radians(angle)
        return cls(length * math.cos(angle), length * math.sin(angle))

    @property
    def length(self) -> float:
        """Get the magnitude (or length) of the vector."""
        return math.hypot(self.x, self.y)

    @property
    def angle(self) -> float:
        """Get the direction (or angle) of the vector (measured in degrees)."""
        return math.degrees(math.atan2(self.y, self.x))

    def __eq__(self, other: Any) -> bool:
        """Test for identical vector/tuple component values (self == other)."""
        return (isinstance(other, Vector) or _is_valid_tuple(other)) and (
            abs(self.x - other[0]) < 5.0e-07
            and abs(self.y - other[1]) < 5.0e-07
        )

    def __repr__(self) -> str:
        """Generate a string representation of the vector."""
        return f'{type(self).__name__}(x={self.x!r}, y={self.y!r})'

    def __len__(self) -> int:
        """Get the number of vector components."""
        return 2

    def __iter__(self) -> Any:
        """Make the vector class an iterable collection."""
        return (i for i in (self.x, self.y))

    def __getitem__(self, index: int) -> float:
        """Get the indexed vector component value."""
        return (self.x, self.y)[index]

    def __setitem__(self, index: int, value: float):
        """Set the indexed vector component value."""
        components = [self.x, self.y]
        components[index] = value
        self.x, self.y = components

    def __abs__(self) -> float:
        """Determine the magnitude (or length) of the vector."""
        return self.length

    def __neg__(self) -> 'Vector':
        """Generate a negative copy of the vector => (-1 * self)."""
        return self._scaled(-1.0)

    def __pos__(self) -> 'Vector':
        """Generate a positive copy of the vector => (+1 * self)."""
        return self._scaled(1.0)

    def __add__(self, other: 'Vector') -> 'Vector':
        """Perform a vector addition (self + other)."""
        return Vector(self.x + other.x, self.y + other.y)

    def __iadd__(self, other: 'Vector') -> 'Vector':
        """Perform an 'in-place' vector addition (self += other)."""
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self, other: 'Vector') -> 'Vector':
        """Perform a vector subtraction (self - other)."""
        return Vector(self.x - other.x, self.y - other.y)

    def __isub__(self, other: 'Vector') -> 'Vector':
        """Perform an 'in-place' vector subtraction (self -= other)."""
        self.x -= other.x
        self.y -= other.y
        return self

    def __mul__(self, scale: float) -> 'Vector':
        """Generate a scaled copy of the vector (self * scale)."""
        return self._scaled(scale)

    def __rmul__(self, scale: float) -> 'Vector':
        """Generate a scaled copy of the vector (scale * self)."""
        return self._scaled(scale)

    def __imul__(self, scale: float) -> 'Vector':
        """Perform an 'in-place' scaling of the vector (self *= scale)."""
        self.x *= scale
        self.y *= scale
        return self

    def __truediv__(self, scale: float) -> 'Vector':
        """Generate a scaled copy of the vector (self / scale)."""
        return self._scaled(1.0 / scale)

    def __itruediv__(self, scale: float) -> 'Vector':
        """Perform an 'in-place' scaling of the vector (self /= scale)."""
        self.x /= scale
        self.y /= scale
        return self

    def __matmul__(self, other: 'Vector') -> float:
        """Perform a dot (or inner) vector product (self @ other)."""
        return (self.x * other.x) + (self.y * other.y)

    def __xor__(self, other: 'Vector') -> float:
        """Perform an outer (or cross) vector product (self ^ other)."""
        return (self.x * other.y) - (self.y * other.x)

    def rotated(self, angle: float) -> 'Vector':
        """Generate a copy of the vector rotated by the specified angle.

        Parameters
        ----------
        angle : float
            The specified rotation angle (measured in degrees)

        Returns
        -------
        Vector
            A copy of the vector rotated by the specified angle
        """
        return self.from_polar_coords(self.length, self.angle + angle)

    def _scaled(self, scale: float) -> 'Vector':
        """Generate a scaled copy of the vector (scale * self)."""
        return Vector(scale * self.x, scale * self.y)


class DrawArea(tk.Label):
    """A Tkinter widget class for rendering and displaying graphics."""

    @dataclass
    class _Properties:
        """The DrawArea widget properties."""

        size: Tuple[int, int]
        color: tuple
        origin: Vector

    _image_array: np.ndarray
    _image: ImageTk.PhotoImage

    # pylint: disable=no-member
    def __init__(
        self,
        parent: Any,
        width: int,
        height: int,
        antialias: Antialias = Antialias.DEFAULT,
    ):
        """Construct and initialize the graphics drawing area.

        Parameters
        ----------
        parent: Any
            The parent widget of the drawing area
        width : int
            The width of the graphics drawing area (in pixels)
        height: int
            The height of the graphics drawing area (in pixels)
        antialias : Antialias
            The type of antialiasing used for rendering text or shapes

        Notes
        -----
        By default, the border style is set to BorderStyle.Flat, and the origin
        is located in the lower-left corner.
        """
        super().__init__(parent)
        self._surface = cairo.ImageSurface(cairo.Format.ARGB32, width, height)
        self._context = cairo.Context(self._surface)
        self._context.set_antialias(antialias)

        size = (max(1, int(width)), max(1, int(height)))
        self._widget = self._Properties(size, (), Vector(0, 0))
        linux = platform.platform().startswith('Linux')
        self.set_background('#d9d9d9' if linux else '#f0f0f0')
        self.border_style = BorderStyle.Flat

    @property
    def border_style(self) -> str:
        """Get/Set the border style of the DrawArea."""
        return self['relief']

    @border_style.setter
    def border_style(self, style: str):
        """Get/Set the border style of the DrawArea."""
        width = -1
        if style in (tk.RAISED, tk.SUNKEN, tk.RIDGE):
            width = 3
        elif style in (tk.GROOVE, tk.SOLID):
            width = 2
        elif style == tk.FLAT:
            width = 0

        if width >= 0:
            self['bd'] = width
            self['relief'] = style
        else:
            warnings.warn('Invalid border style designator', stacklevel=2)

    @property
    def cursor(self) -> str:
        """Get/Set the cursor style for the DrawArea."""
        return self['cursor']

    @cursor.setter
    def cursor(self, style: str):
        """Get/Set the cursor style for the DrawArea."""
        self['cursor'] = style

    @property
    def width(self) -> int:
        """Get the width of the graphics drawing area (in pixels)."""
        return self._widget.size[0]

    @property
    def height(self) -> int:
        """Get the height of the graphics drawing area (in pixels)."""
        return self._widget.size[1]

    @property
    def origin(self) -> Tuple[float, float]:
        """Get/Set the origin location in the graphics drawing area."""
        return self._widget.origin.x, -self._widget.origin.y

    @origin.setter
    def origin(self, point: Tuple[float, float]):
        """Get/Set the origin location in the graphics drawing area."""
        if self._valid_coordinate(point):
            new_origin = Vector(point[0], -point[1])
            shift = new_origin - self._widget.origin
            self._context.translate(shift.x, shift.y)
            self._widget.origin = new_origin

    def clear(self):
        """Clear all graphics objects from the drawing area."""
        self._context_set_source_rgba(self._widget.color)
        self._context.rectangle(
            -self._widget.origin.x,
            -self._widget.origin.y,
            self.width,
            self.height,
        )
        self._context.fill()

    def display(self):
        """Display all the currently defined graphics objects."""
        shape = (self.height, self.width, 4)
        buffer_array = np.ndarray(shape, np.uint8, self._surface.get_data())

        # Convert the image color from BGRA to RGBA
        self._image_array = buffer_array.copy()
        self._image_array[:, :, 0] = buffer_array[:, :, 2]
        self._image_array[:, :, 2] = buffer_array[:, :, 0]
        self._image = ImageTk.PhotoImage(Image.fromarray(self._image_array))
        self['image'] = self._image

    def save(self, filename: str) -> bool:
        """Save the currently displayed graphics image to the specified file.

        Parameters
        ----------
        filename : str
            The full pathname of the image file

        Returns
        -------
        bool
            True if the image was successfully saved, False otherwise
        """
        success = False
        try:
            image = Image.fromarray(self._image_array[:, :, :3])
            image.save(filename)
            success = True
        except OSError:
            warnings.warn('The image file could not be written', stacklevel=2)
        except ValueError:
            warnings.warn('Invalid image filename', stacklevel=2)
        return success

    def set_background(self, color: Union[str, tuple]):
        """Erase the drawing and set the background to the specified color.

        Parameters
        ----------
        color : str | tuple
            The specified background color of the DrawArea widget
        """
        color_value = self._rgba_color(color, 3)
        if color_value != (0.0, 0.0, 0.0, 0.0):
            self._widget.color = color_value[0:3] + (1.0,)
            self.clear()
            self.display()

    def arc(
        self,
        brush: Brush,
        radius: float,
        start: Union[Vector, Tuple[float, float]],
        end: Union[Vector, Tuple[float, float]],
    ):
        """Draw a circular arc segment from the start point to the end point.

        Parameters
        ----------
        brush : Brush
            The specified graphics rendering options
        radius : float
            The arc radius (in pixels), negative denotes a clockwise direction
        start : Vector | tuple[float, float]
            The start point coordinates (in pixels)
        end : Vector | tuple[float, float]
            The end point coordinate (in pixels)
        """
        if self._valid_coordinate(start) and self._valid_coordinate(end):
            self._context.save()  # Save the Previous Graphics Context
            begin = Vector(start[0], self.height - start[1])
            stop = Vector(end[0], self.height - end[1])
            self._context_set_line_properties(brush)
            self._create_segment(-radius, begin, stop)
            self._context.stroke()
            self._context.restore()  # Restore the Previous Graphics Context

    def arrow(
        self,
        brush: Brush,
        location: Union[Vector, Tuple[float, float]],
        angle: float,
    ) -> Vector:
        """Draw a standard 3:1 ratio arrowhead at the specified location.

        The length of the arrowhead equals: 3 * max(6.0, 4 * brush.width)

        Parameters
        ----------
        brush : Brush
            The specified graphics rendering options
        location : Vector | tuple[float, float]
            The location coordinates of the arrowhead's tip (in pixels)
        angle : float
            The direction angle of the arrowhead (measured in degrees)

        Returns
        -------
        Vector
            The coordinates of the center of the arrowhead's base (in pixels)
        """
        end = Vector(0, self.height)
        if self._valid_coordinate(location):
            self._context.save()  # Save the Previous Graphics Context
            position = Vector(location[0], self.height - location[1])
            width = max(3.0, 2 * brush.width)
            base = Vector.from_polar_coords(width, -(angle + 90))
            end = position - Vector.from_polar_coords(6 * width, -angle)
            self._context_set_source_rgba(brush.color)
            self._create_polygon([end - base, position, end + base], None)
            self._context.fill()
            self._context.restore()  # Restore the Previous Graphics Context
        return Vector(end.x, self.height - end.y)

    def circle(
        self,
        brush: Brush,
        center: Union[Vector, Tuple[float, float]],
        radius: float,
    ):
        """Draw a circle of specified radius, centered on the given location.

        Parameters
        ----------
        brush : Brush
            The specified graphics rendering options
        center : Vector | tuple[float, float]
            The center location coordinates (in pixels)
        radius: float
            The specified radius of the circle (in pixels)
        """
        if self._valid_coordinate(center):
            size = (2 * radius, 2 * radius)
            self.ellipse(self._local_copy(brush), center, size)

    def datapoint(
        self,
        brush: Brush,
        center: Union[Vector, Tuple[float, float]],
        shape: Shape = Shape.CIRCLE,
    ):
        """Draw a datapoint centered at the given location.

        Parameters
        ----------
        brush : Brush
            The specified graphics rendering options
        center : Vector | tuple[float, float]
            The center location coordinates (in pixels)
        shape : Shape
            The specified datapoint shape, default shape is a circle
        """
        if self._valid_coordinate(center):
            line_width = 1 if brush.width < 8 else 2
            local_brush = self._local_copy(brush, line_width, True)
            width = max(5.0, brush.width) - (line_width if brush.edge else 0)
            if shape == Shape.CIRCLE:
                self.circle(local_brush, center, 0.5 * width)
            elif shape == Shape.DIAMOND:
                self.square(local_brush, center, 0.8 * width, 45)
            elif shape == Shape.SQUARE:
                self.square(local_brush, center, width)
            elif shape == Shape.TRIANGLE:
                center = Vector(center[0], center[1])
                vertex = Vector(0, 0.6 * width)
                vertices = [center + vertex.rotated(i * 120) for i in range(3)]
                self.polygon(local_brush, vertices)
            else:
                warnings.warn(f"Unrecognized shape: '{shape}'", stacklevel=2)

    def ellipse(
        self,
        brush: Brush,
        center: Union[Vector, Tuple[float, float]],
        size: Union[Size, Tuple[float, float]],
        angle: float = 0.0,
    ):
        """Draw an ellipse of given dimensions, centered on the given location.

        Parameters
        ----------
        brush : Brush
            The specified graphics rendering options
        center : Vector | tuple[float, float]
            The center location coordinates (in pixels)
        size : Size | tuple[float, float]
            The width and height dimensions of the ellipse (in pixels)
        angle : float
            The rotation angle (measured in degrees), default angle is 0.0
        """
        if self._valid_coordinate(center) and self._valid_dimensions(size):
            self._context.save()  # Save the Previous Graphics Context
            width, height = size
            self._context.translate(center[0], self.height - center[1])
            self._context.rotate(-math.radians(angle))
            self._context.scale(1.0, height / width)
            if brush.fill:
                self._context_set_source_rgba(brush.color)
                self._context.arc(0, 0, 0.5 * width, 0, 2 * math.pi)
                self._context.fill()
            if brush.line_width >= 0:
                scale_factor = 0.5 * ((width + height) / min(width, height))
                local_brush = brush.copy(scale_factor * brush.line_width)
                self._context_set_line_properties(local_brush)
                self._context.arc(0, 0, 0.5 * width, -math.pi, math.pi)
                self._context.stroke()
            self._context.restore()  # Restore the Previous Graphics Context

    def label(
        self,
        style: TextStyle,
        start: Union[Vector, Tuple[float, float]],
        text: str,
    ) -> Size:
        """Draw a text label at the starting location.

        Parameters
        ----------
        style : TextStyle
            The specified text rendering options
        start : Vector | tuple[float, float]
            The starting location coordinates (in pixels)
        text : str
            The text string to display

        Returns
        -------
        Size
            The dimensions of the rendered text string (in pixels)
        """
        text = f'{text}'  # Ensure a string value
        self._context.save()  # Save the Previous Graphics Context
        self._context.select_font_face(
            style.font.family,
            FontSlant.ITALIC if style.font.italic else FontSlant.NORMAL,
            FontWeight.BOLD if style.font.bold else FontWeight.NORMAL,
        )
        self._context.set_font_size(style.font.height)
        self._context_set_source_rgba(style.color)
        extents = self._context.text_extents(text)
        width, height = extents.width + 2, extents.height
        shift_x, shift_y = 1.5, -3.0
        if style.anchor in (tk.NW, tk.N, tk.NE):
            shift_y = height
        if style.anchor in (tk.W, tk.LEFT, tk.CENTER, tk.RIGHT, tk.E):
            scale = 0.17 if any(char in text for char in 'gjpqy') else 0.02
            shift_y = 0.5 * height - 0.75 - scale * style.font.height
        if style.anchor in (tk.N, tk.CENTER, tk.S):
            shift_x = -0.5 * width + 2.0 - 0.05 * style.font.height
        if style.anchor in (tk.NE, tk.RIGHT, tk.E, tk.SE):
            shift_x = -width
        if self._valid_coordinate(start):
            self._context.translate(start[0], self.height - start[1])
            self._context.rotate(-math.radians(style.angle))
            self._context.translate(shift_x, shift_y)
            self._context.move_to(0, 0)
            if style.border_width <= 0:  # Normal(Solid) Text
                self._context.show_text(text)
            else:  # Outlined Text
                self._context.text_path(text)
                self._context.set_line_width(style.border_width)
            self._context.stroke()
        self._context.restore()  # Restore the Previous Graphics Context
        return Size(extents.width + 3, extents.height + 3)

    def line(
        self,
        brush: Brush,
        start: Union[Vector, Tuple[float, float]],
        end: Union[Vector, Tuple[float, float]],
    ):
        """Draw a straight line segment from the start point to the end point.

        Parameters
        ----------
        brush : Brush
            The specified graphics rendering options
        start : Vector | tuple[float, float]
            The start point coordinates (in pixels)
        end : Vector | tuple[float, float]
            The end point coordinates (in pixels)
        """
        if self._valid_coordinate(start) and self._valid_coordinate(end):
            self._context.save()  # Save the Previous Graphics Context
            self._context_set_line_properties(brush)
            self._context.move_to(start[0], self.height - start[1])
            self._context.line_to(end[0], self.height - end[1])
            self._context.stroke()
            self._context.restore()  # Restore the Previous Graphics Context

    def polygon(
        self,
        brush: Brush,
        coords: Sequence[Union[Vector, Tuple[float, float]]],
        segments: Optional[Sequence[Union[int, float]]] = None,
    ):
        """Draw an enclosed region as defined by the coordinates and segments.

        The polygon's perimeter path endpoint is always joined to coords[0].
        By default, the segments parameter is set to None, which results in a
        perimeter path composed of all line segments. When the segments
        parameter is set to a list of radii, each radius value is rendered as
        follows: A radius > 0 draws a counter-clockwise arc segment. A radius
        < 0 draws a clockwise arc segment. A radius == 0 draws a line segment.
        The number of segments must equal the number of coordinates.

        Parameters
        ----------
        brush : Brush
            The specified graphics rendering options
        coords : Sequence[Vector | tuple[float, float]]
            The list of the coordinates that define the polygon
        segments : Sequence[int | float], optional
            The optional list of segment radii, defaults to all line segments
        """
        if self._valid_coord_list(coords) and self._valid_radii_list(segments):
            self._context.save()  # Save the Previous Graphics Context
            vertices = [Vector(pnt[0], self.height - pnt[1]) for pnt in coords]
            if segments is None or len(coords) == len(segments):
                if brush.fill:
                    self._context_set_source_rgba(brush.color)
                    self._create_polygon(vertices, segments)
                    self._context.fill()
                if brush.line_width >= 0:
                    self._context_set_line_properties(brush)
                    self._create_polygon(vertices, segments)
                    self._context.stroke()
            else:
                error = "Lengths do not match: 'len(coords) != len(segments)'"
                warnings.warn(error, stacklevel=2)
            self._context.restore()  # Restore the Previous Graphics Context

    def rectangle(
        self,
        brush: Brush,
        start: Union[Vector, Tuple[float, float]],
        size: Union[Size, Tuple[float, float]],
    ):
        """Draw a rectangle with the given dimensions at the starting location.

        Parameters
        ----------
        brush : Brush
            The specified graphics rendering options
        start: Vector | tuple[float, float]
            The starting location coordinates (in pixels)
        size: Size | tuple[float, float]
            The width and height dimensions of the rectangle (in pixels)
        """
        if self._valid_coordinate(start) and self._valid_dimensions(size):
            self._context.save()  # Save the Previous Graphics Context
            width, height = size
            plot_x, plot_y = start[0], self.height - start[1]
            if brush.fill:
                self._context_set_source_rgba(brush.color)
                self._context.rectangle(plot_x, plot_y, width, -height)
                self._context.fill()
            if brush.line_width >= 0:
                self._context_set_line_properties(brush)
                self._context.rectangle(plot_x, plot_y, width, -height)
                self._context.stroke()
            self._context.restore()  # Restore the Previous Graphics Context

    def square(
        self,
        brush: Brush,
        center: Union[Vector, Tuple[float, float]],
        side: float,
        angle: float = 0.0,
    ):
        """Draw a square of given side length, centered on the given location.

        Parameters
        ----------
        brush : Brush
            The specified graphics rendering options
        center : Vector | tuple[float, float]
            The center location coordinates (in pixels)
        side : float
            The side length of the square (in pixels)
        angle : float
            The rotation angle (measured in degrees), default angle is 0.0
        """
        if self._valid_coordinate(center):
            origin = Vector(center[0], center[1])
            corner = Vector.from_polar_coords(side / math.sqrt(2), 45 + angle)
            vertices = [origin + corner.rotated(i * 90) for i in range(4)]
            self.polygon(self._local_copy(brush), vertices)

    @staticmethod
    def _angle(origin: Vector, coord: Vector) -> float:
        """Determine the angle of a coordinate with respect to the origin."""
        return math.atan2(coord.y - origin.y, coord.x - origin.x)

    def _create_polygon(self, vertices: List[Vector], segments: Any):
        """Draw a polygon specified by the vertices and segments lists."""
        start = vertices[0]
        self._context.move_to(start.x, start.y)
        if segments is None:
            for vertex in vertices[1:]:
                self._context.line_to(vertex.x, vertex.y)
        else:
            coordinates = list(vertices + [start])
            for i, end in enumerate(coordinates[1:]):
                self._create_segment(-segments[i], start, end)
                start = end
        self._context.close_path()

    def _create_segment(self, radius: float, start: Vector, end: Vector):
        """Draw the specified segment."""
        mid_point = 0.5 * (end - start)
        if radius == 0.0 or start == end or mid_point.length > abs(radius):
            self._context.line_to(end.x, end.y)
        else:
            length = math.sqrt((radius / mid_point.length) ** 2 - 1)
            offset = length * mid_point.rotated(math.copysign(90, radius))
            center = start + (mid_point + offset)
            begin, stop = self._angle(center, start), self._angle(center, end)
            x_pos, y_pos = center
            if radius < 0:
                self._context.arc_negative(x_pos, y_pos, -radius, begin, stop)
            else:
                self._context.arc(x_pos, y_pos, radius, begin, stop)

    def _context_set_line_properties(self, brush: Brush):
        """Set the context line properties."""
        self._context.set_dash(brush.dash)
        self._context.set_line_cap(brush.line_cap)
        self._context.set_line_join(brush.line_join)
        self._context.set_line_width(max(0.0, brush.line_width))
        self._context_set_source_rgba(brush.line_color, 5)

    def _context_set_source_rgba(self, color: Any, level: int = 4):
        """Set the context source rgba color."""
        color = self._rgba_color(color, level)
        self._context.set_source_rgba(color[0], color[1], color[2], color[3])

    def _local_copy(self, brush: Brush, width=None, fill=None) -> Brush:
        """Make a valid color, local copy of the brush."""
        return brush.copy(width, self._rgba_color(brush.color, 4), fill)

    @staticmethod
    def _rgba_color(color: Any, level: int = 1) -> tuple:
        """Generate a floating point RGBA color value from various formats."""
        result: tuple = (0.0, 0.0, 0.0, 0.0)
        error_message = f"Invalid color value: '{color}'"
        if color:
            try:
                if isinstance(color, str):
                    color = ImageColor.getrgb(color)
                all_numbers = all(_is_number(value) for value in color)
                if len(color) >= 3 and all_numbers:
                    if all(isinstance(value, int) for value in color):
                        color = tuple((int(value) / 255) for value in color)
                    color = tuple(max(0.0, min(value, 1.0)) for value in color)
                    result = color + (1.0,)
                else:
                    warnings.warn(error_message, stacklevel=level)
            except ValueError:
                warnings.warn(error_message, stacklevel=level)
        return result[0:4]

    @staticmethod
    def _valid_coordinate(value: Any, level: int = 3) -> bool:
        """Test for a valid coordinate value."""
        valid = isinstance(value, Vector) or (
            not isinstance(value, Size) and _is_valid_tuple(value)
        )
        if not valid:
            warnings.warn(f"Not a valid location: '{value}'", stacklevel=level)
        return valid

    @staticmethod
    def _valid_dimensions(value: Any) -> bool:
        """Test for a valid dimensions value."""
        valid = isinstance(value, Size) or _is_valid_tuple(value)
        if not valid:
            warnings.warn(f"Not a valid size: '{value}'", stacklevel=3)
        return valid

    def _valid_coord_list(self, coords: Sequence) -> bool:
        """Test for a valid list of coordinate values."""
        valid = False
        if isinstance(coords, Sequence) and len(coords) > 2:
            valid = all(self._valid_coordinate(vertex, 5) for vertex in coords)
        else:
            warnings.warn('coordinates count is less than 3', stacklevel=3)
        return valid

    @staticmethod
    def _valid_radii_list(radii: Optional[Sequence]) -> bool:
        """Test for a valid list of segment radii values or None."""
        valid = radii is None
        if radii is not None:
            if isinstance(radii, Sequence) and len(radii) > 2:
                valid = all(_is_number(value, 5) for value in radii)
            else:
                warnings.warn('segment count is less than 3', stacklevel=3)
        return valid


def _is_valid_tuple(value: Any) -> bool:
    """Test for a valid tuple value."""
    return (
        isinstance(value, tuple)
        and len(value) == 2
        and all(_is_number(n) for n in value)
    )


def _is_number(value: Any, level: Optional[int] = None) -> bool:
    """Test for a numerical value."""
    valid = isinstance(value, (int, float)) and not isinstance(value, bool)
    if level is not None and not valid:
        warnings.warn(f"Invalid segment radius: '{value}'", stacklevel=level)
    return valid
