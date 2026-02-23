from dataclasses import dataclass

__version__: str

@dataclass(frozen=True)
class Color:
    Black: tuple
    Magenta: tuple
    Red: tuple
    Orange: tuple
    Yellow: tuple
    Green: tuple
    Cyan: tuple
    Blue: tuple
    Violet: tuple
    Gray: tuple
    Brown: tuple
    Coral: tuple
    DarkRed: tuple
    DarkGreen: tuple
    DarkBlue: tuple
    Olive: tuple
    Lime: tuple
    Crimson: tuple
    Maroon: tuple
    Gold: tuple
    Silver: tuple
    RoyalBlue: tuple
    White: tuple

def rgba_color(red: int, green: int, blue: int, alpha: int = 255) -> tuple: ...
def build_rgba_color(color: Union[str, tuple], level: int = 1) -> tuple: ...

