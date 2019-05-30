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
filename = sys.argv[1]

d = LCDSysInfo()
start = time.time()
d.draw_image(filename, screen_x, screen_y)
print('render took %3.5f' % (time.time() - start,) )

