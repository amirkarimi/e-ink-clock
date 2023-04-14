#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import typer
import json
import urllib.request
from datetime import datetime
from inky.what import InkyWHAT

from PIL import Image, ImageFont, ImageDraw


def cur_temp(api_key: str, lat: float, lon: float):
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}'
    response = urllib.request.urlopen(url)
    result = json.loads(response.read().decode('utf-8'))
    return result["main"]["temp"] - 273.15 # Kelvin to Celsius


def build_img(inky_display, cur_temp: str):
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

    def draw_text(height, text, font, align='center', margin=10, color=inky_display.BLACK):
        x, y, w, h = font.getbbox(text)
        w += x
        h += y
        if align == 'center':
            width = WIDTH//2 - w//2
        elif align == 'right':
            width = WIDTH - w - margin
        elif align == 'left':
            width = margin
        draw.text((width, height), text, fill=color, font=font)
        return (width, height, w, h)

    now = datetime.now()
    time = now.strftime('%H:%M')
    date = now.strftime(f'{now.month}/{now.day}')

    font_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "fonts/ChessType.ttf")

    draw_text(60, time, ImageFont.truetype(font_path, 125))
    draw_text(230, date, ImageFont.truetype(font_path, 70), align='right', margin=5)
    
    cur_temp = str(round(cur_temp)).replace('-', '–') # Have to use a different dash as regular `-` is not supported by the font
    draw_text(230, f'{cur_temp}°', ImageFont.truetype(font_path, 70), align='left', margin=5)
    return img

def main(weather_api_key: str, lat: float, lon: float, debug: bool = False):
    if debug:
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

    temp = cur_temp(weather_api_key, lat, lon)
    img = build_img(inky_display, temp)
    
    if debug:
        img = img.convert("RGB")
        img.show()
    else:
        # Display the completed canvas on Inky wHAT
        inky_display.set_image(img)
        inky_display.show()

if __name__ == "__main__":
    typer.run(main)

