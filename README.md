# Project Description

**A Tkinter DrawArea wrapper class for the pycairo package.**

Add words here ...

Unlike either the Tkinter Canvas widget or the pycairo package, the DrawArea widget class operates in a standard, right-handed coordinate system, where the y-axis values increase from the bottom the top of the display.  This is illustrated in Figure 1.

![Figure 1](./examples/images/figure_1.png)

This package adds a fully compatible **DrawArea** widget to Tkinter's set of graphical user interface widgets, thereby providing the user with a convenient tool for working with the pycairo package in any Tkinter window based application.

# Installation

```
pip install pycairotk
```

<div class="page"/>

# Overview

This package provides the following class definitions **:**

* **DrawArea -** A Tkinter widget class for displaying an OpenCV image
* **BorderStyle -** A data class of the available border style options
* **Brush -** A data class of graphics rendering options
* **Font -** A data class for describing a text font
* **TextStyle -** A data class of text rendering options
* **Shape -** An enumerated class of available datapoint shapes
* **LineCap -** An enumerated class of available line endpoint options
* **LineJoin -** An enumerated class of available line junction options
* **Vector -** A class which represents a geometric vector in the xy plane

This package also provides a defined Color class and utility color functions:

* **Color -** A data class of commonly used drawing colors
* **rgba_color -** Generates a floating point RGBA color value from integer values
* **build_rgba_color -** Generates a floating point RGBA color value from various formats

Add words here ...

<div class="page"/>

### Color Parameters

A color parameter value can be provided in one of the following forms **:**

* It can be expressed as a defined color in the **Color** class **(e.g. Color.Crimson)**
* It can be expressed as a named color string, e.g. **'white'**. A defined set of named colors can be found at **:** [CSS Color 4: Named Colors](https://drafts.csswg.org/css-color-4/#named-colors)
* It can be expressed as a 6-digit hexadecimal notation color string **'#rrggbb'**
* It can be expressed as a 8-digit hexadecimal notation color string **'#rrggbbaa'**
* It can be expressed as a tuple color value **( red, green, blue, [alpha] )** that conforms to one of these formats **:**
    * 3 or 4 integer color components ranging in value from 0 to 255
    * 3 or 4 floating point color components ranging in value from 0.0 to 1.0

### Coordinates Parameters

A coordinates parameter value can be provided in one of the following two forms **:**

* It can be expressed as a **Vector** value
* It can be expressed as a two element tuple **( x-coordinate, y-coordinate )**

The ability to to use vectors ...

![Figure 2](./examples/images/figure_2.png)

<div class="page"/>

# Documentation

## DrawArea

### DrawArea( *parent, width, height* )

Constructs and initializes the graphics drawing area.

* ***parent* : Any -** The parent widget of the DrawArea.
* ***width* : int -** The width of the graphics drawing area (in pixels).
* ***height* : int -** The height of the graphics drawing area (in pixels).

By default, the **border_style** property is set to **BorderStyle.Flat**, and the **origin (0, 0)** is located in the lower-left corner.

### Properties

* **border_style : str -** The border style of the DrawArea. This property can be set to any one of the available BorderStyle options **( e.g. BorderStyle.Ridge )**. ( read / write )

* **cursor : str -** The cursor style for the DrawArea **( e.g. 'crosshair'** ). ( read / write )

* **origin : tuple -** The location of the origin in the graphics drawing area (in pixels). ( read / write)

* **width : int -** The width of the graphics drawing area (in pixels). ( readonly )

* **height : int -** The height of the graphics drawing area (in pixels). ( readonly )

### Methods

* **clear() -** Clear all graphics objects from the drawing area.

* **display() -** Display all the currently defined graphics objects.

* **save( *filename* ) -** Save the currently displayed graphics image to a file.  This method returns **True** if the image was successfully saved, **False** otherwise.

    * ***filename* : str -** The full filename of the image file.

* **set_background( *color* ) -** Set the background color of the DrawArea.

    * ***color* : Color | str | tuple -** The specified background color (the alpha component is ignored).

<div class="page"/>

* **arc( *brush, center, radius, start, end* ) -** Draw an arc of given radius from the start angle to the end angle.

    * ***brush* : Brush -** The specified graphics rendering options.
    * ***center* : Vector | tuple -** The center location coordinates of the arc (in pixels).
    * ***radius* : float -** The arc radius (in pixels), negative denotes a clockwise direction.
    * ***start* : float -** The start angle (measured in degrees).
    * ***end* : float -** The end angle (measured in degrees).

* **arc_segment( *brush, radius, start, end* ) -** Draw a circular arc segment from the start point to the end point.

    * ***brush* : Brush -** The specified graphics rendering options.
    * ***radius* : float -**  : The arc radius (in pixels), negative denotes a clockwise direction.
    * ***start* : Vector | tuple -** The start point coordinates (in pixels).
    * ***end* : Vector | tuple -** The end point coordinate (in pixels).

* **circle( *brush, center, radius* ) -** Draw a circle of specified radius, centered on the given location.

    * ***brush* : Brush -** The specified graphics rendering options.
    * ***center* : Vector | tuple -** The center location coordinates (in pixels).
    * ***radius* : float -** The specified radius of the circle (in pixels).

* **datapoint( *brush, center, shape* ) -** Draw a datapoint centered at the given location.

    * ***brush* : Brush -** The specified graphics rendering options.
    * ***center* : Vector | tuple -** The center location coordinates (in pixels).
    * ***shape* : Shape -** The specified datapoint shape, default is **Shape.CIRCLE**

* **ellipse( *brush, center, size, angle* ) -** Draw an ellipse of given dimensions, centered on the given location.

    * ***brush* : Brush -** The specified graphics rendering options.
    * ***center* : Vector | tuple -** The center location coordinates (in pixels).
    * ***size* : tuple -** The width and height dimensions of the ellipse (in pixels).
    * ***angle* : float -** The rotation angle of the ellipse (measured in degrees), default is **0.0**

* **line( *brush, start, end* ) -** Draw a straight line segment from the start point to the end point.

    * ***brush* : Brush -** The specified graphics rendering options.
    * ***start* : Vector | tuple -** The start point coordinates (in pixels).
    * ***end* : Vector | tuple -** The end point coordinate (in pixels).

<div class="page"/>

* **polygon( *brush, coords* ) -** Draw a polygon as defined by a list of vertex coordinates.

    * ***brush* : Brush -** The specified graphics rendering options.
    * ***coords* : list[Vector] | list[tuple] -** The list of the vertex coordinates that define the polygon.

* **rectangle( *brush, start, size* ) -** Draw a rectangle with the given dimensions at the starting location.

    * ***brush* : Brush -** The specified graphics rendering options.
    * ***start* : Vector | tuple -** The starting location coordinates (in pixels).
    * ***size* : tuple -** The width and height dimensions of the rectangle (in pixels).

* **square( *brush, center, side, angle* ) -** Draw a square of given side length, centered on the given location.

    * ***brush* : Brush -** The specified graphics rendering options.
    * ***center* : Vector | tuple -** The center location coordinates (in pixels).
    * ***side* : float -** The side length of the square (in pixels).
    * ***angle* : float -** The rotation angle of the square (measured in degrees), default is **0.0**

* **label( *style, start, text* ) -** Draw a text label at the starting location. This method returns the dimensions of the rendered text string (in pixels).

    * ***style* : TextStyle -** The specified text rendering options.
    * ***start* : Vector | tuple -** The starting location coordinates (in pixels).
    * ***text* : str -** The text string to display

<div class="page"/>

## BorderStyle

**These are the available border style options for the DrawArea.**

* **Raised -** The DrawArea appears raised above the background.
* **Sunken -** The DrawArea appears recessed into the background.
* **Groove -** The DrawArea has a carved groove border.
* **Ridge -** The DrawArea has a raised ridge border.
* **Solid -** The DrawArea has a simple solid border.
* **Flat -** The DrawArea appears flat, no border.

## Brush

**The graphics rendering options data class.**

### Brush( *[width], [color], [fill], [edge], [dash], [line_cap], [line_join]* )

### Attributes

* **width : float -** The width of the displayed line segment or the datapoint size, default is **1.0**
* **color : Color | str | tuple -** The color of a line segment, perimeter, or the solid fill color, default is **'black'**
* **fill : bool -** A True value will fill the defined region with solid color, default is **False**
* **edge : Color | str | tuple -** The color of the solid filled region's perimeter, default is **' '**
* **dash : list | tuple -** The dash pattern of the line segment, default is **( )**
* **line_cap : LineCap -** The shape of a line segment's endpoints, default is **LineCap.BUTT**
* **line_join : LineJoin -** The defined region's perimeter joining style, default is **LineJoin.MITER**

### Methods

* **copy( *[width], [color]* ) -** Returns a deep copy of the brush.

    * ***width* : float -** The new width of the copied brush. [optional]
    * ***color* : Color | str | tuple -** The new color of the copied brush. [optional]

## Font

**The text font description data class.**

### Font( *[family], [height], [bold], [italic]* )

### Attributes

* **family : str -** The font family name as a string, default is **'Arial'**
* **height : flat -** The font height (in pixels), default is **12.0**
* **bold : bool -** Boldface text if True, otherwise normal text, default is **False**
* **italic : bool -** Italic text if True, otherwise upright text, default is **False**

## TextStyle

**The text rendering options data class.**

### TextStyle( *[font], [color], [anchor], [angle], [border]* )

### Attributes

* **font : Font -** The font of the displayed text, default is **Font()**
* **color : Color | str | tuple -** The color of the displayed text, default is **'black'**
* **anchor -** The anchor point of the displayed text, default is **tk.LEFT**
* **angle -** The orientation angle of the displayed text (measured in degrees), default is **0.0**
* **border -** A positive value displays outlined text, default is **-1.0**

## Shape

**These are the available datapoint shape options.**

* **CIRCLE -** The datapoint is drawn as a circular dot.
* **DIAMOND -** The datapoint is drawn as a diamond
* **SQUARE -** The datapoint is drawn as a square.
* **TRIANGLE -** The datapoint is drawn as an upward pointing triangle.

## LineCap

**These constants specify how to render the endpoints of a line segment.**

* **BUTT -** The line segment ends exactly at each endpoint.
* **ROUND -** The line segment includes a circle centered on each endpoint.
* **SQUARE -** The line segment includes a square centered on each endpoint.

## LineJoin

**These constants specify how to render the junction of two line segments.**

* **BEVEL -** The join is a flat facet drawn at the mid-angle between the line segments.
* **MITER -** The join is a sharp corner formed by continuing the line edges until they meet.
* **ROUND -** The join is a circle centered on the point where the line segments meet.

<div class="page"/>

## Vector

**A class which represents a geometric vector in the xy plane.**

### Vector( *x, y* )

Constructs a new Vector from the x-axis & y-axis vector components.

* ***x* : float -** The x-axis component of the vector.
* ***y* : float -** The y-axis component of the vector.

### Vector.from_polar_coords( *length, angle* )

Constructs a new Vector using polar coordinate values.

* ***length* float -*** The length (or magnitude) of the vector.
* ***angle* : float -*** The angle (or direction) of the vector w.r.t. the x-axis (measured in degrees).

### Attributes

* **x : float -** The x-axis component of the vector. ( read / write )
* **y : float -** The x-axis component of the vector. ( read / write )

### Properties

* **length : float -** The magnitude (or length) of the vector. ( readonly )

* **angle : float -** The direction (or angle) of the vector w.r.t. the x-axis (measured in degrees). ( readonly )

### Methods

* **rotated( *angle* ) -** Returns a copy of the vector rotated by the given angle (measured in degrees).

### Operators

The following operations are supported by the Vector class :

* **Vector Addition :**

```
    vector_c = vector_a + vector_b
    vector_a += vector_b
```

* **Vector Subtraction :**

```
    vector_c = vector_a - vector_b
    vector_a -= vector_b
```

* **Scalar Multiplication :**

```
    vector_b = scalar * vector_a
    vector_b = vector_a * scalar
    vector_a *= scalar
```

* **Scalar Division :**

```
    vector_b = vector_a / scalar
    vector_a /= scalar
```


<div class="page"/>

* **Unary Plus & Unary Minus :**

```
    vector_b = +vector_a
    vector_b = -vector_a
```

* **Checking Equality :**

```
    boolean = vector_a == vector_b
    boolean = vector_a != vector_b
```

* **The Inner (or Dot) Product :**

```
    scalar = vector_a @ vector_b
```

* **The Outer (or Cross) Product :**

```
    scalar = vector_a ^ vector_b
```

### Miscellaneous

* **A vector can be indexed just like a tuple with two elements :**

```
    # The x-axis component can be accessed as vector[0]
    # The y-axis component can be accessed as vector[1]
    # The len() function returns the number of vector components

    vector = Vector(3, 4)
    x, y = vector  # Assigns: x = 3, y = 4
    print(len(vector))  # Output: 2
```

* **The abs() function returns the magnitude (or length) of a vector :**

```
    vector = Vector(3, 4)
    print(abs(vector))  # Output: 5.0
    print(vector.length)  # Output: 5.0
```

# User Notes

The DrawArea widget is derived from the Tkinter Label widget. This means that the DrawArea inherits all of the Universal Tkinter widget methods, and that all of these methods are available to the user. This also means that all of the Label widget's options are exposed to the user. To avoid the possibility of creating any unpredictable DrawArea behavior, the user should never directly modify the values of the underlying Label widget's options. The one exception to this "hands-off rule" is that the user can safely modify the widget's **'state'** value.

<div class="page"/>

# DrawArea Example

```
import tkinter as tk
from pycairotk import DrawArea, Brush, Font, TextStyle, Vector


class Animated(tk.Frame):
    """The pycairotk graphics window."""

    def __init__(self, master):
        """Construct the main screen window."""
        super().__init__(master)
        master.title('Pycairotk Animated')
        master.resizable(False, False)
        self.grid()

        self._draw = DrawArea(self, 320, 320)
        self._draw.set_background('lightblue')
        self._draw.grid()

        self._brush = Brush(4, 'red', True, 'white')
        font = Font(height=60, bold=True)
        self._text_style = TextStyle(font, 'white', tk.CENTER)
        self._draw.origin = (self._draw.width / 2, self._draw.height / 2)
        self._update_screen(0)

    def _update_screen(self, angle):
        """Update the screen display."""
        n = 8
        delta = 360 / n
        vertex = Vector.from_polar_coords(100, angle + delta / 2 - 90)
        vertices = [vertex.rotated(i * delta) for i in range(n)]
        self._text_style.angle = angle

        self._draw.clear()
        self._draw.polygon(self._brush, vertices)
        self._draw.label(self._text_style, (0, 0), 'STOP')
        self._draw.display()

        self.after(20, self._update_screen, (angle + 2) % 360)


# Execute the script
if __name__ == '__main__':
    main_form = Animated(tk.Tk())
    main_form.mainloop()
```