#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#
"""Demo drawing an image using raw interface

Draws directly to the screen.
Does not write to flash.
"""

import sys
import time

from PIL import Image, ImageDraw

from lcd_drawing import LCDSysInfo


d = LCDSysInfo()

screen_x, screen_y = 0, 0  # these are offsets
MAX_IMAGE_SIZE = (320, 240)

clock_color = (255, 0, 0)
start = time.time()
for colour in [(0, 0, 0), (255, 255, 255)]:
    im = Image.new('RGBA', MAX_IMAGE_SIZE, colour)
    id = ImageDraw.Draw(im)
    id.text((0, 0), 'Hello world', fill=clock_color)  # default font.... TODO pick something large
    d.draw_image_im(im, screen_x, screen_y)  # takes about 2.25 secs

print('render took %3.5f' % (time.time() - start,) )

