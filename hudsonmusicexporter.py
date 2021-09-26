#!/bin/python3

######################################################
# hudsonmusicexporter
# Script to export books from the Hudson Music Digital Library as PDF
#
# Author: Kippi
# Version: 1.0
######################################################

# --- BEGIN IMPORTS (DO NOT EDIT) ---
import argparse
import keyboard
import time
from PIL import Image, ImageGrab
from tkinter import Tk
from tkinter.filedialog import asksaveasfilename
# --- END IMPORTS

# --- BEGIN CONFIG ---

# Define if the default zoom level should be used
zoomed = True

# The zoom level the program has been set to
zoom = 1.05

# The file into which the book should be saven
output_file = None

# --- END CONFIG ---

# DO NOT EDIT BELOW THIS LINE IF YOU DO NOT KNOW WHAT YOU ARE DOING

VERSION = "1.0"

DEFAULT_SIZES = [
    (735 / 1920, 980 / 1080),   # RELATIVE_PAGE_SIZE
    (593 / 1920, 50 / 1080),    # SINGLE_PAGE_RELATIVE_OFFSET
    (225 / 1920, 50 / 1080),    # DOUBLE_PAGE_RELATIVE_OFFSET
]

ZOOM_CONSTANTS = (767.65, 1023.81)  # Determined by linear regression


def main():
    global zoomed, zoom, output_file

    def capture(images, offsets, page_size, count):
        time.sleep(2)
        for offset in offsets:
            images.append(ImageGrab.grab(bbox=(offset[0], offset[1], offset[0] + page_size[0], offset[1] + page_size[1])))
            print("Captured page " + str(count[0]))
            count[0] += 1
        keyboard.send("right")

    parser = argparse.ArgumentParser(description='Export books from the Hudson Music Digital Library')
    parser.add_argument('-z',
                        '--zoom',
                        type=int,
                        action='store',
                        dest='zoom',
                        default=None,
                        required=False,
                        help='Specify the zoom level.')
    parser.add_argument('-o',
                        '--output-file',
                        type=str,
                        action='store',
                        dest='filename',
                        required=False,
                        default=None,
                        help='Specify where the book should be saved. If not specified or invalid a file picker dialog will appear.')

    args = parser.parse_args()

    if args.zoom is not None:
        zoom = args.zoom
        zoomed = True

    if args.filename is not None:
        output_file = args.filename

    screenshot = ImageGrab.grab()

    zoomed_sizes = [(round(zoom * ZOOM_CONSTANTS[0]) / 1920, round(zoom * ZOOM_CONSTANTS[1]) / 1080)]
    zoomed_sizes.append((round((1920 - zoomed_sizes[0][0] * 1920) / 2) / 1920, round((1080 - zoomed_sizes[0][1] * 1080) / 2) / 1080))
    zoomed_sizes.append((round((1920 - zoomed_sizes[0][0] * 2 * 1920) / 2) / 1920, zoomed_sizes[1][1]))

    sizes = zoomed_sizes if zoomed else DEFAULT_SIZES
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
    print(" - Set the zoom to " + str(zoom * 100) + "% (bottom left corner)")
    print(" - Go into fullscreen mode")
    print(" - Press [Ctrl] + [Enter]")
    print(" - Wait until the program completes")
    print()
    print()

    count = [1]  # We want to pass this by reference
    images = []
    odd_page_count = page_count - (page_count+1) % 2
    keyboard.wait("ctrl+enter")

    capture(images, [single_page_offset], page_size, count)

    while count[0] < odd_page_count:
        capture(images, double_page_offset, page_size, count)

    if odd_page_count != page_count:
        capture(images, [single_page_offset], page_size, count)

    Tk().withdraw()
    if output_file is None:
        output_file = asksaveasfilename(defaultextension='.pdf', filetypes=[("PDF Documents", '*.pdf')], title="Save the book as...")

    while True:
        try:
            with open(output_file, "w") as f:
                images.pop(0).save(output_file, "PDF", resolution=100.0, save_all=True, append_images=images)
                print("Creating PDF as \"" + output_file + "\"...")
                break
        except OSError:
            print("The selected file was not valid, please try again")
            output_file = asksaveasfilename(defaultextension='.pdf', filetypes=[("PDF Documents", '*.pdf')], title="Save the book as...")

    print("Done!")


if __name__ == '__main__':
    main()
