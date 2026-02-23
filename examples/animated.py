"""animated.py - A script for displaying an animation example."""

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
