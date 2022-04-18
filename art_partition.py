# Add faint lines to partition images as guide lines for drawing practice.
# Pad blank space to fit standard paper ratio.
# Usage: python art_partition.py FILE_PATH [HORIZONTAL] [VERTICAL]
# 4 Partitions by default.
# Vertical partitions same as horizontal partitions by default.
# If a directory is given, all the image files in the directory will be processed into a new directory.

import os
import sys
import math
import numpy as np
from glob import glob
from PIL import Image, ImageDraw

IMAGE_RATIO = math.sqrt(2)


def art_partition(file_path, horizontal, vertical):
    """
    Pad blank space to fit standard paper ratio and add faint lines to
    partition images as guide lines for drawing practice.

    file_path: image file path
    horizontal: number of horizontal partitions
    vertical: number of vertical partitions
    """
    try:
        image = Image.open(file_path)
    except IOError:
        print(f"{file_path} is not an image.")
        return

    # Analyse the size of the image to know which direction to pad.
    width, height = image.size
    pad_h = 0
    pad_v = 0
    if (height > width and height > width * IMAGE_RATIO) or \
            (width > height and height * IMAGE_RATIO > width):
        # Pad horizontally
        if height > width: # Portrait
            raw_difference = height / IMAGE_RATIO - width
        elif width > height: # Landscape
            raw_difference = height * IMAGE_RATIO - width
        halved_floor = math.floor(raw_difference / 2)
        remainder = raw_difference - halved_floor * 2
        if remainder < 1:
            pad_h = halved_floor
        else:
            pad_h = halved_floor + 1
    elif (height > width and height < width * IMAGE_RATIO) or \
            (width > height and height * IMAGE_RATIO < width):
        # Pad vertically
        if height > width: # Portrait
            raw_difference = width * IMAGE_RATIO - height
        elif width > height: # Landscape
            raw_difference = width / IMAGE_RATIO - height
        halved_floor = math.floor(raw_difference / 2)
        remainder = raw_difference - halved_floor * 2
        if remainder < 1:
            pad_v = halved_floor
        else:
            pad_v = halved_floor + 1

    # Create new image with padding
    new_width = width + 2 * pad_h
    new_height = height + 2 * pad_v
    new_image = Image.new(
        image.mode, (new_width, new_height), color = (255, 255, 255, 0)
    )
    new_image.paste(image, (pad_h, pad_v))

    # Draw partition lines
    line_width = max(2, round(new_width / 200), round(new_height / 200))
    line_layer = Image.new(
        image.mode, (new_width, new_height), color = (255, 255, 255, 0)
    )
    if vertical == None: # If unspecified
        vertical = horizontal
    draw = ImageDraw.Draw(line_layer)
    for i in range(1, horizontal):
        x = round(new_width * i / horizontal)
        draw.line(
            [(x, 0), (x, new_height)], fill=(0, 0, 0, 128), width=line_width
        )
    for i in range(1, vertical):
        y = round(new_height * i / vertical)
        draw.line(
            [(0, y), (new_width, y)], fill=(0, 0, 0, 128), width=line_width
        )

    # Save image
    new_image.alpha_composite(line_layer)
    new_image.save(f"processed_{file_path}") # New file or directory
    print(f"Processed and saved {file_path}.")


if __name__ == '__main__':
    # Parse arguments
    if len(sys.argv) < 2:
        print("Usage: python art_partition.py FILE_PATH [HORIZONTAL] [VERTICAL]")
    elif len(sys.argv) > 4:
        print("Too many arguments.")
    else:
        file_path = sys.argv[1]
        if len(sys.argv) > 2:
            horizontal = int(sys.argv[2])
        else:
            horizontal = 4
        if len(sys.argv) > 3:
            vertical = int(sys.argv[3])
        else:
            vertical = None
        if os.path.isfile(file_path):
            art_partition(file_path, horizontal, vertical)
        else:
            try:
                os.mkdir(f"processed_{file_path}")
            except OSError:
                pass
            for file_name in os.listdir(file_path):
                art_partition(
                    os.path.join(file_path, file_name), horizontal, vertical
                )
