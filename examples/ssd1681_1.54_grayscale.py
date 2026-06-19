# SPDX-FileCopyrightText: 2026 Mikey Sklar, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

"""4-gray "ThinkInk" info card for the Adafruit 1.54" 200x200 eInk Breakout (#4196, SSD1681).

Shows the 4-gray path: product text plus a 4-level gray ramp (white / light / dark / black).
Pass ``custom_lut=adafruit_ssd1681.GRAY4_LUT`` and ``grayscale=True`` to enable 4-gray.

Wiring — Feather + EYESPI Breakout:
  TCS -> D9   DC -> D10   RST -> D11   BUSY -> D12   SCK/MOSI/3V3/GND as usual
"""

import time

import board
import displayio
import terminalio
from adafruit_display_text import label
from fourwire import FourWire

import adafruit_ssd1681

displayio.release_displays()

spi = board.SPI()
display_bus = FourWire(
    spi,
    command=board.D10,
    chip_select=board.D9,
    reset=board.D11,
    baudrate=1000000,
)
time.sleep(1)

display = adafruit_ssd1681.SSD1681(
    display_bus,
    width=200,
    height=200,
    busy_pin=board.D12,
    rotation=0,
    custom_lut=adafruit_ssd1681.GRAY4_LUT,
    grayscale=True,
)

WHITE = 0xFFFFFF
LIGHT = 0xAAAAAA
DARK = 0x555555
BLACK = 0x000000
W, H = 200, 200

bg = displayio.Bitmap(W, H, 4)
pal = displayio.Palette(4)
pal[0], pal[1], pal[2], pal[3] = WHITE, LIGHT, DARK, BLACK

# 4-level gray ramp across the bottom
ramp_top, ramp_bot = 150, 190
seg = W // 4
for x in range(W):
    level = 3 - min(x // seg, 3)  # left=black(3) .. right=white(0)
    for y in range(ramp_top, ramp_bot):
        bg[x, y] = level
# black border + dividers so every block (incl. white) reads distinctly
for x in range(W):
    bg[x, ramp_top] = 3
    bg[x, ramp_bot - 1] = 3
for y in range(ramp_top, ramp_bot):
    bg[0, y] = 3
    bg[W - 1, y] = 3
for i in range(1, 4):
    for y in range(ramp_top, ramp_bot):
        bg[i * seg, y] = 3

g = displayio.Group()
g.append(displayio.TileGrid(bg, pixel_shader=pal))
g.append(label.Label(terminalio.FONT, text="Adafruit ThinkInk", color=BLACK, scale=1, x=6, y=14))
g.append(label.Label(terminalio.FONT, text='1.54" 200x200', color=BLACK, scale=2, x=6, y=40))
g.append(label.Label(terminalio.FONT, text="#4196", color=BLACK, scale=2, x=6, y=66))
g.append(label.Label(terminalio.FONT, text="4-Gray E-Ink", color=DARK, scale=2, x=6, y=96))
g.append(label.Label(terminalio.FONT, text="SSD1681 Driver", color=BLACK, scale=2, x=6, y=122))
display.root_group = g

print("Refreshing (4-gray)...")
display.refresh()
print("Done.")

time.sleep(display.time_to_refresh + 5)
print("Ready.")

while True:
    time.sleep(10)
