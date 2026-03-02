"""pycolor.py -  A defined Color class and utility color functions.

This module provides the following class and functions:

* Color      - A data class of commonly used drawing colors
* rgba_color - Generates a floating point RGBA color from integer values
"""

__version__ = '1.0.0'

from dataclasses import dataclass


def rgba_color(red: int, green: int, blue: int, alpha: int = 255) -> tuple:
    """Generate a floating point RGBA color value from integer values.

    Parameters
    ----------
    red : int
        The red color component value (0 to 255)
    green : int
        The green color component value (0 to 255)
    blue : int
        The blue color component value (0 to 255)
    alpha : int
        The alpha or opacity component value (0 to 255), the default is 255

    Returns
    -------
    tuple
        A floating point (red, green, blue, alpha) color value
    """
    red = max(0, min(red, 255))
    green = max(0, min(green, 255))
    blue = max(0, min(blue, 255))
    alpha = max(0, min(alpha, 255))
    scale = 1.0 / 255
    return scale * red, scale * green, scale * blue, scale * alpha


@dataclass(frozen=True)
class Color:
    """Commonly used drawing colors."""

    Black = rgba_color(0x00, 0x00, 0x00)
    Magenta = rgba_color(0xFF, 0x00, 0xFF)
    Red = rgba_color(0xFF, 0x00, 0x00)
    Orange = rgba_color(0xFF, 0xA5, 0x00)
    Yellow = rgba_color(0xFF, 0xFF, 0x00)
    Green = rgba_color(0x00, 0x80, 0x00)
    Cyan = rgba_color(0x00, 0xFF, 0xFF)
    Blue = rgba_color(0x00, 0x00, 0xFF)
    Violet = rgba_color(0xEE, 0x82, 0xEE)
    Gray = rgba_color(0x80, 0x80, 0x80)
    Brown = rgba_color(0xA5, 0x2A, 0x2A)
    Coral = rgba_color(0xFF, 0x7F, 0x50)
    DarkRed = rgba_color(0x8B, 0x00, 0x00)
    DarkGreen = rgba_color(0x00, 0x64, 0x00)
    DarkBlue = rgba_color(0x00, 0x00, 0x8B)
    Olive = rgba_color(0x55, 0x6B, 0x2F)
    Lime = rgba_color(0x00, 0xFF, 0x00)
    Crimson = rgba_color(0xDC, 0x14, 0x3C)
    Maroon = rgba_color(0x80, 0x00, 0x00)
    Gold = rgba_color(0xFF, 0xD7, 0x00)
    Silver = rgba_color(0xC0, 0xC0, 0xC0)
    RoyalBlue = rgba_color(0x41, 0x69, 0xE1)
    White = rgba_color(0xFF, 0xFF, 0xFF)
