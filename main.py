#! /usr/bin/env python3

import gc

import sys

from board import BLACK, RED, GREEN, WHITE, BLUE, Layout
from hex_math import filled_circle, line

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

CONFIG = {"logo_color": RED}

ESP_LOGO = [
    # Firt pixel
    (-2, 4),
    # U part
    (0, 3),
    (0, 2),
    (-1, 2),
    (-2, 2),
    (-3, 3),
    (-4, 3),
    (-4, 2),
    (-3, 1),
    (-2, 0),
    (-1, 0),
    (0, 0),
    (1, 0),
    (2, 0),
    (2, 1),
    (2, 2),
    # C part
    (4, -1),
    (4, -2),
    (3, -2),
    (2, -2),
    (1, -2),
    (0, -2),
    (-1, -2),
    (-2, -2),
    (-3, -1),
    # Line
    (0, -4),
    (1, -4),
    (2, -4),
    (3, -4),
    (4, -4),
]


async def logo_basic(display, color):
    await display.write([(h, color) for h in ESP_LOGO])
    gc.collect()


async def logo_row(display, color):
    for h in ESP_LOGO:
        await display.write([(h, color)])
        await asyncio.sleep(0.1)
    gc.collect()


async def logo_lines(display, color, bg_color):
    head = ESP_LOGO[0]
    for h in list(reversed(ESP_LOGO)):
        l = line(head, h)
        for i, p in enumerate(l[1:]):
            await display.write([(p, color), (l[i], bg_color)])
            await asyncio.sleep(0.05)

    await display.write([(head, color)])
    await asyncio.sleep(0.05)
    gc.collect()


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

    while True:
        await circles(display, [RED, GREEN, BLUE, BLACK, WHITE])
        await asyncio.sleep(0.1)

        await display.fill(WHITE)
        await asyncio.sleep(1)
        await logo_basic(display, CONFIG["logo_color"])
        await asyncio.sleep(2)

        await display.fill(WHITE)
        await logo_row(display, CONFIG["logo_color"])
        await asyncio.sleep(2)

        await display.fill(WHITE)
        await logo_lines(display, CONFIG["logo_color"], WHITE)
        await asyncio.sleep(2)


try:
    asyncio.run(main())
except (KeyboardInterrupt, Exception) as e:
    if "print_exception" in dir(sys):
        sys.print_exception(e)  # type: ignore
    else:
        raise e
finally:
    asyncio.new_event_loop()
