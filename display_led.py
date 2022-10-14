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
    ):  # type: (int, tuple[int, int, int], Any, Any) -> None
        self.pin = Pin(pin, Pin.OUT)
        self._pixels = neopixel.NeoPixel(self.pin, len(kwargs["layout"]))

        self._color_map = color_map

        super(Display, self).__init__(*args, **kwargs)

    async def init(self):  # type: () -> BaseDisplay
        await super().init()

        if self.color is not None:
            await self.fill(self.color)

        return self

    async def write(self, board):
        await super().write(board)

        for pixel, color in board.pixels.items():
            rgb = color.to_json()

            if pixel not in self.layout_dict:
                continue

            self._pixels[self.layout_dict[pixel]] = [rgb[i] for i in self._color_map]

        self._pixels.write()
