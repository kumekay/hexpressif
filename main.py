#! /usr/bin/env python3

import gc

import sys

from board import BLACK, RED, GREEN, WHITE, BLUE, Board, Layout, Hex, Color

gc.collect()

if sys.implementation.name == "micropython":
    from display_led import Display
    from config import LED_CONFIG as DISPLAY_CONFIG

    import uasyncio as asyncio
else:
    from display_ws import Display
    from config import WS_CONFIG as DISPLAY_CONFIG

    import asyncio

gc.collect()

from random import randint


class HexFloat:
    def __init__(self, q, r):  # type: (float, float) -> None
        self.q = q
        self.r = r


def filled_circle(radius):  # type: (int) -> list[Hex]
    hexes = []  # type: list[Hex]

    for q in range(-radius, radius + 1):
        for r in range(-radius, radius + 1):
            for s in range(-radius, radius + 1):
                if q + r + s == 0:
                    hexes.append(Hex(q, r))

    return hexes


def distance(a, b):  # type: (Hex, Hex) -> int
    return (abs(a.q - b.q) + abs(a.q + a.r - b.q - b.r) + abs(a.r - b.r)) / 2


def interpolate_num(a, b, t):  # type: (float, float, float) -> float
    return a + (b - a) * t


def interpolate_hex(a, b, t):  # type: (Hex, Hex, float) -> HexFloat
    return HexFloat(interpolate_num(a.q, b.q, t), interpolate_num(a.r, b.r, t))


def round_hex(hf):  # type: (HexFloat) -> Hex
    q_grid = round(hf.q)
    r_grid = round(hf.r)
    q = hf.q - q_grid
    r = hf.r - r_grid

    if abs(q) >= abs(r):
        return Hex(q_grid + round(q + 0.5 * r), r_grid)
    else:
        return Hex(q_grid, r_grid + round(r + 0.5 * q))


def line(a, b):  # type: (Hex, Hex) -> list[Hex]
    N = distance(a, b)
    results = []  # list[Hex]
    for i in range(N):
        results.append(round_hex(interpolate_hex(a, b, 1.0 / N * i)))
    return results


async def main():
    layout = Layout.from_file("layout.json")
    display = await Display(
        layout=layout, color=Color(10, 10, 10), **DISPLAY_CONFIG
    ).init()

    COLORS = [RED, GREEN, BLUE, WHITE, BLACK]
    while True:
        for color in COLORS:
            for r in range(5):
                await display.write(Board.from_list(filled_circle(r), color))
                await asyncio.sleep(0.5)
        gc.collect()

        for _ in range(10):
            x = Hex(randint(-4, 4), randint(-4, 4))
            y = Hex(randint(-4, 4), randint(-4, 4))
            await display.write(Board.from_list(line(x, y), COLORS[randint(0, 3)]))
            await asyncio.sleep(1)
        gc.collect()


try:
    asyncio.run(main())
except (KeyboardInterrupt, Exception) as e:
    if "print_exception" in dir(sys):
        sys.print_exception(e)  # type: ignore
    else:
        raise e
finally:
    asyncio.new_event_loop()
