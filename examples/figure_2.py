"""figure_2.py - A script for creating a vector geometry diagram."""

import math
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
        brush = Brush(2)
        length, angle = 7, 30
        vector = scale * Vector.from_polar_coords(length, angle)
        self._draw.line(brush, (0, 0), self._draw.arrow(brush, vector, angle))

        # Display the position vector's angle
        brush.width = 1
        radius = 0.4 * vector.length
        arrow_length = 3 * max(6.0, 4 * brush.width)
        arrow_angle = 90 + angle - math.degrees(0.5 * arrow_length / radius)
        arrow_base = self._draw.arrow(brush, 0.4 * vector, arrow_angle)
        self._draw.arc_segment(brush, radius, (radius, 0), arrow_base)
        font = Font(height=14, bold=True)
        label_position = Vector.from_polar_coords(radius + 10, angle / 2)
        self._draw.label(TextStyle(font), label_position, f'+ {angle} degrees')

        # Display the position vector's length
        text_style = TextStyle(font, anchor=tk.CENTER, angle=angle)
        label_position = Vector(vector.length / 2, 20).rotated(angle)
        self._draw.label(text_style, label_position, f'Length = {length}')

        # Display the position vector's coordinates
        brush = Brush(dash=[5])
        text_style = TextStyle(Font(height=20), anchor=tk.CENTER)
        text = f'({vector.x / scale :0.2f}, {vector.y / scale :0.2f})'
        label_position = Vector(vector.length + 15, 19).rotated(angle)
        self._draw.label(text_style, label_position, text)
        self._draw.line(brush, (0, vector.y), vector)
        self._draw.line(brush, (vector.x, 0), vector)

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
                x_pos = i * scale
                self._draw.line(pen, (x_pos, 0), (x_pos, -10))
                x_pos -= 5 * len(str(i))
                self._draw.label(text_style, (x_pos, -20), str(i))

        self._draw.label(TextStyle(Font(height=20)), (-30, 330), 'Y-Axis')
        self._draw.line(pen, (0, -100), (0, 300))
        text_style.anchor = tk.E
        for i in range(-2, 8):
            if i != 0:
                y_pos = i * scale
                self._draw.line(pen, (0, y_pos), (-10, y_pos))
                self._draw.label(text_style, (-13, y_pos + 1), str(i))


# Execute the script
if __name__ == '__main__':
    main_form = Figure2(tk.Tk())
    main_form.draw_diagram()
    main_form.mainloop()
