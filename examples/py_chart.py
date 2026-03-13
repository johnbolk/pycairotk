"""py_chart.py - A demonstration script which uses vectors and segments."""

import tkinter as tk
from pycairotk import DrawArea, Brush, Font, TextStyle, Vector


class DemoWindow(tk.Frame):
    """The pycairotk graphics demonstration window."""

    def __init__(self, master):
        """Construct and draw the pycairotk graphics example."""
        super().__init__(master)
        master.title('Pycairotk Example')
        self._draw = DrawArea(self, 600, 450)
        self._draw.grid()
        self.grid()

        # Draw a simple pie-chart
        radius = 150
        color_names = ['red', 'yellow', 'skyblue']
        inc = 360 / len(color_names)
        line = Vector(0, radius)
        middle = 0.6 * line.rotated(inc / 2)
        brush = Brush(2, fill=True, edge='black')
        text_style = TextStyle(Font(height=20, bold=True), anchor=tk.CENTER)
        self._draw.origin = (self._draw.width / 2, self._draw.height / 2)
        for i, color in enumerate(color_names):
            pnts = [(0, 0), line.rotated(i * inc), line.rotated((i + 1) * inc)]
            segments = [0, radius, 0]  # segments = [line, arc, line]
            self._draw.polygon(brush.copy(color=color), pnts, segments)
            self._draw.label(text_style, middle.rotated(i * inc), color)

        self._draw.display()  # This should always be the last statement


# Execute the script
if __name__ == '__main__':
    main_form = DemoWindow(tk.Tk())
    main_form.mainloop()
