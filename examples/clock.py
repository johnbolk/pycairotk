"""clock.py - An animated analog clock script."""

import tkinter as tk
from datetime import datetime
from pycairotk import DrawArea, Font, Brush, TextStyle, LineCap, Vector


class Clock(tk.Frame):
    """The main screen clock window."""

    def __init__(self, master):
        """Construct and initialize the main screen clock window."""
        super().__init__(master, bd=5, relief='sunken')
        master.title('Pycairotk Clock')
        master.resizable(False, False)
        self.grid()

        # Dimension and position the clock window
        self.clock_radius = 280
        clock_center = self.clock_radius + 20
        self._clock = DrawArea(self, 2 * clock_center, 2 * clock_center)
        self._clock.set_background('green')
        self._clock.origin = (clock_center, clock_center)
        self._clock.grid()
        start = self.master.winfo_screenwidth() // 2 - clock_center
        top = self.master.winfo_screenheight() // 2 - clock_center - 20
        master.geometry(f'+{start}+{top}')

        # Initialize and start the clock
        self._tick = -360 / 60
        self._hour = self._tick * 5
        self._noon_start = Vector.from_polar_coords(self.clock_radius, 90)
        self._update()

    def _update(self):
        """Update the clock display."""
        time = datetime.today()
        sec_angle = self._tick * (time.second + 1e-6 * time.microsecond)
        min_angle = self._tick * time.minute + (sec_angle / 60)
        hrs_angle = self._hour * (time.hour % 12) + (min_angle / 12)

        self._draw_face()
        self._draw_3d_hand(Brush(9, fill=True), 0.60, hrs_angle, 4)
        self._draw_3d_hand(Brush(6, fill=True), 0.85, min_angle, 6)
        self._draw_3d_hand(Brush(3, 'red'), 0.935, sec_angle, 8)
        self._clock.datapoint(Brush(3), (0, 0))
        self._clock.display()

        self.after(20, self._update)  # Continuously update the clock display

    def _draw_face(self):
        """Draw the face."""
        brush = Brush(5, 'white', True, 'black')
        self._clock.circle(brush, (0, 0), self.clock_radius + 3)
        self._clock.circle(Brush(3), (0, 0), 0.95 * self.clock_radius)

        # Draw the tick marks
        brush = Brush(line_cap=LineCap.ROUND)
        for i in range(60):
            hour_mark = not bool(i % 5)
            head = self._noon_start.rotated(i * self._tick)
            tail = head * (0.92 if hour_mark else 0.95)
            brush.width = 7 if hour_mark else 3
            self._clock.line(brush, head, tail)

        # Label the hours
        font = Font('Times', 65, True)
        style = TextStyle(font, 'black', tk.CENTER, border_width=4)
        length = [0.77, 0.79, 0.80, 0.78, 0.78, 0.77,
                  0.77, 0.78, 0.79, 0.74, 0.76, 0.78]
        for i in range(1, 13):
            position = length[i - 1] * self._noon_start.rotated(i * self._hour)
            self._clock.label(style, position, str(i))

    def _draw_3d_hand(self, brush, length, angle, shift):
        """Draw a clock hand and its shadow."""
        self._draw_hand(brush.copy(color='#00000050'), length, angle, shift)
        self._draw_hand(brush, length, angle, 0)

    def _draw_hand(self, brush, length, angle, shift):
        """Draw a clock hand."""
        center = shift * Vector(1, -1)
        head = length * self._noon_start.rotated(angle) + center
        tail = -head * (0.4 if brush.fill else 0.3) + center
        if brush.fill:  # Draw the minute and hour hands
            base = Vector.from_polar_coords(3, head.angle + 90)
            size = brush.width * base / 3
            body = 0.7 * head
            hand = [
                center - base,
                body - size,
                head,
                body + size,
                center + base,
                tail + size,
                0.9 * tail,
                tail - size,
            ]
            self._clock.polygon(brush, hand)
        else:  # Draw the second hand with a circular loop on the tail
            radius = 10
            loop_center = tail + Vector.from_polar_coords(radius, tail.angle)
            self._clock.line(brush, head, tail)
            self._clock.circle(brush, loop_center, radius)
        self._clock.datapoint(brush.copy(brush.width + 10), center)


# Execute the script
if __name__ == '__main__':
    clock_app = Clock(tk.Tk())
    clock_app.mainloop()
