"""figure_2.py - A script for creating a vector geometry diagram."""

import tkinter as tk
from pycairotk import DrawArea, Brush, Font, TextStyle, Vector


class Figure2(tk.Frame):
    """The pycairotk graphics diagram window."""

    def __init__(self, master):
        """Construct the main screen window."""
        super().__init__(master)
        master.title('Pycairotk Figure 2')
        master.resizable(False, False)
        self.grid()

        self._draw = DrawArea(self, 560, 560)
        self._draw.set_background('white')
        self._draw.grid()

    def draw_diagram(self):
        """Draw the pycairotk graphics diagram."""
        title = 'Vector Geometry Example'
        text_style = TextStyle(Font(height=24), anchor=tk.CENTER)
        self._draw.label(text_style, (280, 540), title)
        text_style.font = Font(height=16)
        self._draw.label(text_style, (280, 30), 'Figure 2')
        self._draw.rectangle(Brush(3), (10, 10), (540, 500))

        scale = 40  # Number of pixels per unit
        self._draw_axes(scale)

        # Create and draw a position vector
        length, angle = 7, 30
        vector = scale * Vector.from_polar_coords(length, angle)
        self._draw_vector((0, 0), vector)

        # Display the position vector's angle
        font = Font(height=14, bold=True)
        radius = 0.4 * vector.length
        self._draw.arc(Brush(), (0, 0), radius, 0, angle)
        self._draw_tip(0.4 * vector, angle + 86, 8)
        label_position = Vector(radius + 10, 0).rotated(angle / 2)
        self._draw.label(TextStyle(font), label_position, f'+ {angle} degrees')

        # Display the position vector's length
        text_style = TextStyle(font, anchor=tk.CENTER, angle=angle)
        label_position = Vector(vector.length / 2, 20).rotated(angle)
        self._draw.label(text_style, label_position, f'Length = {length}')

        # Display the position vector's coordinates
        text_style = TextStyle(Font(height=20), anchor=tk.CENTER)
        text = f'({vector.x / scale :0.2f}, {vector.y / scale :0.2f})'
        label_position = Vector(vector.length + 15, 19).rotated(angle)
        self._draw.label(text_style, label_position, text)
        self._draw.line(Brush(dash=[5]), (0, vector.y), vector)
        self._draw.line(Brush(dash=[5]), (vector.x, 0), vector)

        self._draw.display()  # This should always be the last statement

    def _draw_axes(self, scale):
        """Draw and label the coordinate system axes."""
        self._draw.origin = (140, 140)
        self._draw.datapoint(Brush(9), (0, 0))
        self._draw.label(TextStyle(Font(height=20)), (-60, 20), '(0, 0)')

        pen = Brush(2)
        text_style = TextStyle(Font(height=14, bold=True))

        self._draw.label(TextStyle(Font(height=20)), (320, 0), 'X-Axis')
        self._draw.line(pen, (-100, 0), (300, 0))
        for i in range(-2, 8):
            if i != 0:
                x = i * scale
                self._draw.line(pen, (x, 0), (x, -10))
                x -= 5 * len(str(i))
                self._draw.label(text_style, (x, -20), str(i))

        self._draw.label(TextStyle(Font(height=20)), (-30, 330), 'Y-Axis')
        self._draw.line(pen, (0, -100), (0, 300))
        text_style.anchor = tk.E
        for i in range(-2, 8):
            if i != 0:
                y = i * scale
                self._draw.line(pen, (0, y), (-10, y))
                self._draw.label(text_style, (-13, y + 1), str(i))

    def _draw_vector(self, start, vector: Vector):
        """Draw a representation of the vector."""
        angle = vector.angle
        start = Vector(start[0], start[1])
        self._draw.line(Brush(2), start, self._draw_tip(start + vector, angle))

    def _draw_tip(self, position: Vector, angle, length=12) -> Vector:
        """Draw a vector tip at the specified position."""
        end = position - Vector.from_polar_coords(length, angle)
        base = Vector.from_polar_coords(length / 2, angle + 90)
        vertices = [end - base, position, end + base]
        self._draw.polygon(Brush(fill=True), vertices)
        return end


# Execute the script
if __name__ == '__main__':
    main_form = Figure2(tk.Tk())
    main_form.draw_diagram()
    main_form.mainloop()
