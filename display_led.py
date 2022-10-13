import neopixel
from machine import Pin
from display import BaseDisplay

try:
    from typing import Any
except ImportError:
    pass


class Display(BaseDisplay):
    def __init__(
        self, pin=1, color_map=(0, 1, 2), *args, **kwargs
    ):  # type: (int, tuple(), Any, Any) -> None
        self.pin = Pin(pin, Pin.OUT)
        self._pixels = neopixel.NeoPixel(self.pin, len(kwargs["layout"]))

        self.color_map = color_map

        super(Display, self).__init__(*args, **kwargs)

    def write(self, board):
        for pixel, color in board.pixels.items():
            rgb = color.to_json()
            self._pixels[self.layout[pixel]] = [rgb[i] for i in self.color_map]

        self._pixels.write()
