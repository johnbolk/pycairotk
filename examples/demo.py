"""demo.py - A script for demonstrating the use of vectors and segments."""

import tkinter as tk
from pycairotk import DrawArea, Brush, Vector


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
        colors = ('red', 'yellow', 'skyblue')
        brush = Brush(2, fill=True, edge='black')
        line = Vector.from_polar_coords(radius, 90)
        self._draw.origin = (self._draw.width / 2, self._draw.height / 2)
        for i, color in enumerate(colors):
            pnts = [(0, 0), line.rotated(i * 120), line.rotated((i + 1) * 120)]
            segments = [0, radius, 0]  # segments = [straight, arc, straight]
            self._draw.polygon(brush.copy(color=color), pnts, segments)
        self._draw.display()  # This should always be the last statement


# Execute the script
if __name__ == '__main__':
    main_form = DemoWindow(tk.Tk())
    main_form.mainloop()
