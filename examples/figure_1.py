"""figure_1.py - A script for creating a coordinate system diagram."""

import tkinter as tk
from pycairotk import DrawArea, Brush, Font, TextStyle


class Figure1(tk.Frame):
    """The pycairotk graphics diagram window."""

    def __init__(self, master):
        """Construct the main screen window."""
        super().__init__(master)
        master.title('Pycairotk Figure 1')
        master.resizable(False, False)
        self.grid()

        self._draw = DrawArea(self, 560, 560)
        self._draw.set_background('white')
        self._draw.grid()

    def draw_diagram(self):
        """Draw the pycairotk graphics diagram."""
        title = 'Right-Handed Coordinate System'
        text_style = TextStyle(Font(height=24), anchor=tk.CENTER)
        self._draw.label(text_style, (280, 540), title)
        text_style.font = Font(height=16)
        self._draw.label(text_style, (280, 30), 'Figure 1')
        self._draw.rectangle(Brush(3), (10, 10), (540, 500))

        self._draw.origin = (140, 140)
        self._draw.datapoint(Brush(9), (0, 0))
        self._draw.label(TextStyle(Font(height=20)), (10, 25), '(0, 0)')

        scale = 40  # Number of pixels per unit
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

        self._draw.display()  # This should always be the last statement


# Execute the script
if __name__ == '__main__':
    main_form = Figure1(tk.Tk())
    main_form.draw_diagram()
    main_form.mainloop()
