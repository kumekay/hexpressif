#! /usr/bin/env python3

import gc

import sys

from board import BLACK, RED, GREEN, WHITE, BLUE, Layout
from hex_math import filled_circle, line

gc.collect()

IS_MICROPYTHON = sys.implementation.name == "micropython"

if IS_MICROPYTHON:
    from display_led import Display
    from config import LED_CONFIG as DISPLAY_CONFIG
    from config import WIFI_CONFIG

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


async def logo_basic(display):
    await display.write([(h, CONFIG["logo_color"]) for h in ESP_LOGO])
    gc.collect()


async def logo_row(display):
    for h in ESP_LOGO:
        await display.write([(h, CONFIG["logo_color"])])
        await asyncio.sleep(0.05)
    gc.collect()


async def logo_lines(display, bg_color):
    head = ESP_LOGO[0]
    for h in list(reversed(ESP_LOGO)):
        l = line(head, h)
        for i, p in enumerate(l[1:]):
            await display.write([(p, CONFIG["logo_color"]), (l[i], bg_color)])
            await asyncio.sleep(0.05)

    await display.write([(head, CONFIG["logo_color"])])
    gc.collect()


async def circles(display, colors):
    for color in colors:
        for r in range(5):
            await display.write([(h, color) for h in filled_circle(r)])
            await asyncio.sleep(0.4)
    gc.collect()


async def start_ap(ssid, password):
    import network

    wlan = network.WLAN(network.AP_IF)
    wlan.active(True)
    wlan.config(essid=ssid, authmode=network.AUTH_WPA_WPA2_PSK, password=password)
    while not wlan.active():
        asyncio.sleep_ms(10)
    print("network config:", wlan.ifconfig())
    return True


async def start_ws():
    from microdot_asyncio import Microdot

    app = Microdot()

    @app.route("/color", methods=["POST"])
    async def index(request):
        CONFIG["logo_color"] = tuple(request.json)
        return {"status": "ok"}

    asyncio.create_task(app.start_server(port=6000, debug=True))


async def start_server():
    if IS_MICROPYTHON:
        await start_ap(WIFI_CONFIG["ssid"], WIFI_CONFIG["pass"])

    await start_ws()


async def main():
    asyncio.create_task(start_server())

    layout = Layout.from_file("layout.json")
    display = await Display(
        layout=layout,
        color=(10, 10, 10),
        **DISPLAY_CONFIG,
    ).init()

    while True:
        await display.fill(WHITE)
        await logo_basic(display)
        await asyncio.sleep(2)

        await display.fill(WHITE)
        await logo_row(display)
        await asyncio.sleep(2)

        await display.fill(WHITE)
        await logo_lines(display, WHITE)
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
