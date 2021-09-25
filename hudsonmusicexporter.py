#!/bin/python3
import time

import keyboard
import os
import time
from pathlib import Path
from PIL import Image, ImageGrab

VERSION = "1.0"
ZOOMED = True
ZOOM = 1.05
ZOOM_CONSTANTS = (767.65, 1023.81)  # Determined by linear regression
OUTPUT_DIRECTORY = os.path.join(str(Path.home()), "Documents", "HudsonBook1")

DEFAULT_SIZES = [
    (735 / 1920, 980 / 1080),   # RELATIVE_PAGE_SIZE
    (593 / 1920, 50 / 1080),    # SINGLE_PAGE_RELATIVE_OFFSET
    (225 / 1920, 50 / 1080),    # DOUBLE_PAGE_RELATIVE_OFFSET
]

ZOOMED_SIZES = [ (round(ZOOM * ZOOM_CONSTANTS[0]) / 1920, round(ZOOM * ZOOM_CONSTANTS[1]) / 1080) ]
ZOOMED_SIZES.append((round((1920 - ZOOMED_SIZES[0][0] * 1920) / 2) / 1920, round((1080 - ZOOMED_SIZES[0][1] * 1080) / 2) / 1080))
ZOOMED_SIZES.append((round((1920 - ZOOMED_SIZES[0][0] * 2 * 1920) / 2) / 1920, ZOOMED_SIZES[1][1]))


def make_screenshot(output_file, offset, page_size):
    screenshot = ImageGrab.grab(bbox=(offset[0], offset[1], offset[0] + page_size[0], offset[1] + page_size[1]))
    screenshot.save(output_file)


def capture(output_dir, offset, page_size):
    global count
    make_screenshot(os.path.join(output_dir, "page" + str(count) + ".png"), offset, page_size)
    print("Captured page " + str(count))
    count += 1


screenshot = ImageGrab.grab(bbox = None)

sizes = ZOOMED_SIZES if ZOOMED else DEFAULT_SIZES
page_size = (sizes[0][0] * screenshot.size[0], sizes[0][1] * screenshot.size[1])
single_page_offset = (sizes[1][0] * screenshot.size[0], sizes[1][1] * screenshot.size[1])
double_page_offset = [(sizes[2][0] * screenshot.size[0], sizes[2][1] * screenshot.size[1])]
double_page_offset.append((double_page_offset[0][0] + page_size[0] + 1, double_page_offset[0][1]))

welcome_text = "Welcome to HusomMusicExporter v"+str(VERSION)
print(welcome_text)
print("-" * len(welcome_text))
print()

page_count = 0
while page_count < 1:
    try:
        page_count = int(input("Please tell me how many pages the book has: "))
    except ValueError:
        pass

print()
print("To export your book do the following:")
print(" - Open the Hudson Music application")
print(" - Find the book you want to export and press \"Read\"")
print(" - Navigate to the first page of the book")
print(" - Set the zoom to 105% (bottom left corner)")
print(" - Go into fullscreen mode")
print(" - Press [Ctrl] + [Enter]")
print(" - Wait until the program completes")
print()
print()

count = 1
output_dir = os.path.join(OUTPUT_DIRECTORY, "pages")
odd_page_count = page_count - (page_count+1) % 2
keyboard.wait("ctrl+enter")

Path(output_dir).mkdir(parents=True, exist_ok=True)
capture(output_dir, single_page_offset, page_size)

while count < odd_page_count:
    keyboard.send("right")
    time.sleep(2)
    capture(output_dir, double_page_offset[0], page_size)
    capture(output_dir, double_page_offset[1], page_size)

if odd_page_count != page_count:
    keyboard.send("right")
    time.sleep(2)
    capture(output_dir, single_page_offset, page_size)

print("Done!")
