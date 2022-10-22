#! /usr/bin/env python3

import gc

import sys

from board import BLACK, RED, GREEN, WHITE, BLUE, Layout

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


def filled_circle(radius):  # type: (int) -> list[tuple[int,int]]
    hexes = []  # type: list[tuple[int,int]]

    for q in range(-radius, radius + 1):
        for r in range(-radius, radius + 1):
            for s in range(-radius, radius + 1):
                if q + r + s == 0:
                    hexes.append((q, r))

    return hexes


def distance(a, b):  # type: (tuple[int,int], tuple[int,int]) -> int
    aq, ar = a
    bq, br = b
    return int((abs(aq - bq) + abs(aq + ar - bq - br) + abs(ar - br)) / 2)


def interpolate_num(a, b, t):  # type: (float, float, float) -> float
    return a + (b - a) * t


def interpolate_hex(
    a, b, t
):  # type: (tuple[int,int], tuple[int,int], float) -> tuple[float,float]
    return (interpolate_num(a[0], b[0], t), interpolate_num(a[1], b[1], t))


def round_hex(hf):  # type: (tuple[float,float]) -> tuple[int,int]
    q_grid = round(hf[0])
    r_grid = round(hf[1])
    q = hf[0] - q_grid
    r = hf[1] - r_grid

    if abs(q) >= abs(r):
        return (q_grid + round(q + 0.5 * r), r_grid)
    else:
        return (q_grid, r_grid + round(r + 0.5 * q))


def line(a, b):  # type: (tuple[int,int], tuple[int,int]) -> list[tuple[int,int]]
    N = distance(a, b)
    results = []  # list[tuple[int,int]]
    for i in range(N):
        results.append(round_hex(interpolate_hex(a, b, 1.0 / N * i)))
    return results


async def circles(display, colors):
    for color in colors:
        for r in range(5):
            await display.write([(h, color) for h in filled_circle(r)])
            await asyncio.sleep(0.4)
    gc.collect()


async def main():
    layout = Layout.from_file("layout.json")
    display = await Display(
        layout=layout,
        color=(10, 10, 10),
        **DISPLAY_CONFIG,
    ).init()

    await circles(display, [RED, GREEN, BLUE, WHITE, BLACK])


try:
    asyncio.run(main())
except (KeyboardInterrupt, Exception) as e:
    if "print_exception" in dir(sys):
        sys.print_exception(e)  # type: ignore
    else:
        raise e
finally:
    asyncio.new_event_loop()
