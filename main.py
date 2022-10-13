#! /usr/bin/env python3

import gc
import sys

from board import BLACK, RED, GREEN, GRAY_50, BLUE, Board, Layout, Hex

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


async def main():
    layout = Layout.from_json("layout.json")
    display = Display(layout=layout, fill=GRAY_50, **DISPLAY_CONFIG)

    center = Hex(0, 0)
    while True:
        for color in [RED, GREEN, BLUE, BLACK]:
            display.write(Board({center: color}))
            await asyncio.sleep(0.7)


try:
    asyncio.run(main())
except (KeyboardInterrupt, Exception) as e:
    if "print_exception" in dir(sys):
        sys.print_exception(e)  # type: ignore
    else:
        raise e
finally:
    asyncio.new_event_loop()
