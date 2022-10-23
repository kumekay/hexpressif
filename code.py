"""
This is example code in CircuitPython for Maker Badge by Czech maker and Make More.

We recommend Mu editor for editing, but you should be able to edit .py file with almost any text editor.
You can edit predefined variables, their scale (1 to x) and position. Origin (0,0 point) is in top left corner and values are in pixels from the origin.

When you save your changes, application will be reloaded and screen will refresh.

Enjoy your badge!
"""

"""
You can add text with print_text function. You have to provide all parameters! Edit or add text to screen via function call below in the code.

DO NOT EDIT CODE WHICH DOES NOT START WITH print_text IF YOU DO NOT KNOW WHAT YOU ARE DOING!
"""


def print_text(text, scale, x_cord, y_cord, text_color):
    group = displayio.Group(scale=scale, x=x_cord, y=y_cord)
    text_var = text
    area = label.Label(terminalio.FONT, text=text, color=text_color)
    group.append(area)  # Add this text to the text group
    g.append(group)


import time
import board
import displayio
import terminalio
import adafruit_ssd1680
import touchio
import neopixel
from adafruit_display_text import label
import wifi
import adafruit_requests
import socketpool


# WIFI
SSID = "esp_logo"
PASS = "Espressif32c3"

# Set color values
BLACK = 0x000000
WHITE = 0xFFFFFF

RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
OFF = (0, 0, 0)

displayio.release_displays()

# Define pinout for this boards.
spi = board.SPI()  # Uses SCK and MOSI
epd_cs = board.D41
epd_dc = board.D40
epd_reset = board.D39
epd_busy = board.D42

# Define touch buttons
touch_threshold = 20000
touch_1 = touchio.TouchIn(board.D5)
touch_1.threshold = touch_threshold
touch_2 = touchio.TouchIn(board.D4)
touch_2.threshold = touch_threshold
touch_3 = touchio.TouchIn(board.D3)
touch_3.threshold = touch_threshold
touch_4 = touchio.TouchIn(board.D2)
touch_4.threshold = touch_threshold
touch_5 = touchio.TouchIn(board.D1)
touch_5.threshold = touch_threshold

display_bus = displayio.FourWire(
    spi, command=epd_dc, chip_select=epd_cs, reset=epd_reset, baudrate=1000000
)
time.sleep(1)

# Create the display object
DISPLAY_WIDTH = 250
DISPLAY_HEIGHT = 122

display = adafruit_ssd1680.SSD1680(
    display_bus,
    width=DISPLAY_WIDTH,
    height=DISPLAY_HEIGHT,
    rotation=270,
    busy_pin=epd_busy,
)

pixel_pin = board.D18
num_pixels = 4

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.05, auto_write=False)

g = displayio.Group()

# Set a background
background_bitmap = displayio.Bitmap(DISPLAY_WIDTH, DISPLAY_HEIGHT, 1)
# Map colors in a palette
palette = displayio.Palette(1)
palette[0] = WHITE

# Create a Tilegrid with the background and put in the displayio group
t = displayio.TileGrid(background_bitmap, pixel_shader=palette)
g.append(t)

# Draw simple text using the built-in font into a displayio group
print_text("Push the buttons!", 2, 35, 20, BLACK)
print_text("Maker Faire", 3, 25, 65, BLACK)
print_text("ESPRESSIF Systems", 2, 25, 105, BLACK)


# Connect to WIFI
for network in wifi.radio.start_scanning_networks():
    print(network, network.ssid, network.channel)
wifi.radio.stop_scanning_networks()

wifi.radio.connect(SSID, PASS)

print("my IP addr:", wifi.radio.ipv4_address)


pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool)

print_text(".", 2, 10, 10, BLACK)
display.show(g)
display.refresh()


def send_color(color):
    requests.post("http://192.168.4.1:6000/color", json=color)


while True:
    if touch_1.value:
        # Turn off the LED
        pixels.fill(RED)
        pixels.show()
        send_color(RED)
    if touch_2.value:
        # Set LED to red
        pixels.fill(GREEN)
        pixels.show()
        send_color(GREEN)
    if touch_3.value:
        # Set LED to green
        pixels.fill(BLUE)
        pixels.show()
        send_color(BLUE)
    if touch_4.value:
        # Set LED to blue
        pixels.fill(YELLOW)
        pixels.show()
        send_color(YELLOW)
    if touch_5.value:
        # Turn off the LED
        pixels.fill(OFF)
        pixels.show()
