#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
from datetime import datetime
from inky.what import InkyWHAT

from PIL import Image, ImageFont, ImageDraw

DEBUG=len(sys.argv) >= 2 and sys.argv[1] == 'debug'

# Set up the correct display and scaling factors
if DEBUG:
    class MockInky:
        WHITE='white'
        BLACK='black'
        RED='red'
        width=400
        height=300
    inky_display = MockInky()
else:
    inky_display = InkyWHAT(colour = 'black') # Using `black` only to speed up the display refresh rate
    inky_display.set_border(inky_display.WHITE)

WIDTH = inky_display.width
HEIGHT = inky_display.height

# Create a new canvas to draw on
img = Image.new("P", (WIDTH, HEIGHT))
draw = ImageDraw.Draw(img)
draw.rectangle(
    [
        0,
        0,
        WIDTH,
        HEIGHT
    ], fill=inky_display.WHITE)

def draw_center(height, text, font, align='center', margin=10, color=inky_display.BLACK):
    x, y, w, h = font.getbbox(text)
    w += x
    if align == 'center':
        width = WIDTH//2 - w//2
    elif align == 'right':
        width = WIDTH - w - margin
    elif align == 'left':
        width = margin
    draw.text((width, height), text, fill=color, font=font)

now = datetime.now()
time = now.strftime('%H:%M')
date = now.strftime(f'{now.day}/{now.month}')

font_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "fonts/ChessType.ttf")

draw_center(60, time, ImageFont.truetype(font_path, 125))
draw_center(230, date, ImageFont.truetype(font_path, 70), align='right', margin=5)

# TODO: Add temp
# https://api.openweathermap.org/data/2.5/weather?lat=...&lon=...&appid={api-key}

if DEBUG:
    img = img.convert("RGB")
    img.show()
else:
    # Display the completed canvas on Inky wHAT
    inky_display.set_image(img)
    inky_display.show()
