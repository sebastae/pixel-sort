#!/usr/bin/env python3.6
import sys

import time
from PIL import Image
import argparse

def rgb_to_hsv(r=0, g=0, b=0):

    if r==g==b:
        return 0, 0, r/255

    R = r/255
    G = g/255
    B = b/255

    cmax = max([R,G,B])
    cmin = min([R,G,B])

    d = cmax - cmin

    if cmax == R:
        hue = 60*(((G-B)/d)%6)
    elif cmax == G:
        hue = 60*(((B-R)/d)+2)
    else:
        hue = 60*(((R-G)/d)+4)

    if cmax == 0:
        sat = 0
    else:
        sat = d/cmax

    val = cmax

    return hue, sat, val


def create_array_from_image(image):
    width, height = image.size
    array = []
    for x in range(width):
        array.append([])
        for y in range(height):
            array[x].append(image.getpixel((x,y)))
    return array

def get_pixel_hue(val):
    r = val[0]
    g = val[1]
    b = val[2]

    return rgb_to_hsv(r,g,b)

def sort_by_hue(array):
    swapped = True
    while swapped:
        swapped = False
        for i in range(len(array)-1):
            if get_pixel_hue(array[i]) > get_pixel_hue(array[i+1]):
                temp = array[i]
                array[i] = array[i+1]
                array[i+1] = temp
                swapped = True
    return array

s = time.time()
if len(sys.argv) > 1:
    image = Image.open(sys.argv[1])
else:
    print("No file specified, exiting")
    exit()
e = time.time()

print("Loaded image '{0}' - {1}".format(sys.argv[1], e-s))

s = time.time()
imgarr = create_array_from_image(image)
e = time.time()

print("Created array -", e-s)

s = time.time()
newimg = []
for line in imgarr:
    newimg.append(sort_by_hue(line))
e = time.time()

print("Sorted image -", e-s)

s= time.time()
result = Image.new('RGBA', image.size)

for x in range(len(newimg)):
    for y in range(len(newimg[x])):
        result.putpixel((x,y), newimg[x][y])
e = time.time()

print("Wrote new image -", e-s)

result.save('out.png')

print("Done!")

