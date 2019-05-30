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

from lcd_drawing import LCDSysInfo


screen_x, screen_y = 0, 0  # these are offsets

d = LCDSysInfo()
start = time.time()

for colour in [(0, 0, 0), (255, 255, 255)]:
    d.fill_rectangle_rel(0, 0, 320, 240, colour)  # takes about 0.15157 secs


print('render took %3.5f' % (time.time() - start,) )

