#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#
"""Dumb clock"""

import os
import sys
import math
import time
import datetime
import struct
import random

from lcd_drawing import LCDSysInfo, TextLines, TextLines, BackgroundColours, TextColours, cc16

paddle_width = 8
paddle_height = 40
ball_size = 8

center_x = int(320/2)
center_y = int(240/2)

paddle1_y = center_y
paddle2_y = center_y

paddle1_old_y = None
paddle2_old_y = None

ball_xspeed = 4
ball_yspeed = 4
ball_x = center_x
ball_y = center_y
ball_old_x = None
ball_old_y = None
points_1 = 0
points_2 = 0

col_white = ( 255, 255, 255 )
col_black = ( 0, 0, 0 )

#def pong_refresh(d):
	# something
	# lala


def pong_score(d):

	d.fill_rectangle(int(center_x - 32), 4, int(center_x - 32 + 22), 24, col_black )
	d.draw_text(str(points_1), int(center_x - 32), 4, "fonts/vcr_osd_mono_regular_20", col_white )

	d.fill_rectangle(int(center_x + 8), 4, int(center_x + 8 + 22), 24, col_black )
	d.draw_text(str(points_2), int(center_x + 8), 4, "fonts/vcr_osd_mono_regular_20", col_white )


def pong_loop(d):

	global ball_x, ball_y, ball_xspeed, ball_yspeed, ball_old_x, ball_old_y

	global col_white, col_black

	global points_1, points_2

	global center_x, center_y

	global paddle1_y, paddle1_old_y
	global paddle2_y, paddle2_old_y

	pong_score(d)

	while 1:		

		# d.draw_text(str(points_2), center_x + 8, 4, "vcr_osd_mono_regular_20", col_white )

		x1 = 0

		# paddle1_y = ball_y - 8
		paddle1_y += ( ( ( ball_y + ball_size ) - paddle1_y - 24 ) / 2 )

		paddle1_y = max( paddle1_y, 0 )
		paddle1_y = min( paddle1_y, 240 - paddle_height )

		# d.fill_rectangle(x1, 0, x1 + paddle_width, 240, col_black )
		if paddle1_old_y:
			d.fill_rectangle(x1, int(paddle1_old_y), x1 + paddle_width, int(paddle1_old_y + paddle_height), col_black )

		d.fill_rectangle(x1, int(paddle1_y), x1 + paddle_width, int(paddle1_y + paddle_height), col_white )

		paddle1_old_y = paddle1_y


		x2 = 320 - paddle_width

		# paddle2_y = ball_y - 8
		# paddle2_y = int( math.sin( time.time() + 1 ) * ( 120 - paddle_height ) ) + 120 - paddle_height
		paddle2_y += ( ( ( ball_y + ball_size ) - paddle2_y - 8 ) / 2 )

		paddle2_y = max( paddle2_y, 0 )
		paddle2_y = min( paddle2_y, 240 - paddle_height )

		# d.fill_rectangle(x2, 0, x2 + paddle_width, 240, col_black )
		if paddle2_old_y:
			d.fill_rectangle(x2, int(paddle2_old_y), x2 + paddle_width, int(paddle2_old_y + paddle_height), col_black )

		d.fill_rectangle(x2, int(paddle2_y), x2 + paddle_width, int(paddle2_y + paddle_height), col_white )

		paddle2_old_y = paddle2_y


		ball_x += ball_xspeed
		ball_y += ball_yspeed

		# if ball_y <= 24:
		# 	pong_score(d)

		

		
		# bounce on top/bottom
		if ball_y >= 240-ball_size or ball_y <= 0:
			ball_yspeed = ball_yspeed * -1


		# right
		if ball_x >= 320 - paddle_width - ball_size and ball_y >= paddle2_y - ball_size and ball_y <= paddle2_y + paddle_height + ball_size:
			
			ball_x = 320 - paddle_width - ball_size - 1
			ball_xspeed = ball_xspeed * -1
			ball_yspeed = ( ( ( ball_y + ball_size / 2 ) - ( paddle2_y + (paddle_height / 2) ) + random.randint(-2,2) ) / 6 )
			if ball_xspeed > 0:
				ball_xspeed += 1
			else:
				ball_xspeed -= 1

		elif ball_x >= 320:
			ball_xspeed = -4
			ball_yspeed = 4
			ball_x = int(center_x)
			ball_y = int(center_y)
			points_1 += 1
			pong_score(d)



		# left
		if ball_x <= paddle_width and ball_y >= paddle1_y - ball_size and ball_y <= paddle1_y + paddle_height + ball_size:
			
			ball_x = paddle_width + ball_size + 1
			ball_xspeed = ball_xspeed * -1
			ball_yspeed = ( ( ( ball_y + ball_size / 2 ) - ( paddle1_y + (paddle_height / 2) ) + random.randint(-2,2) ) / 6 )
			if ball_xspeed > 0:
				ball_xspeed += 1
			else:
				ball_xspeed -= 1

		elif ball_x <= 0:

			ball_xspeed = 4
			ball_yspeed = 4
			ball_x = int(center_x)
			ball_y = int(center_y)
			points_2 += 1
			pong_score(d)



		if ball_old_x:
			d.fill_rectangle(int(ball_old_x), int(ball_old_y), int(ball_old_x + 8), int(ball_old_y + 8), col_black )

		ball_old_x = ball_x
		ball_old_y = ball_y

		#d.fill_rectangle(x2, 0, x2 + 8, 240, cc16( 0, 0, 0 ) )
		d.fill_rectangle(int(ball_x), int(ball_y), int(ball_x + 8), int(ball_y + 8), col_white )

		ball_xspeed = min( 10, ball_xspeed )
		ball_xspeed = max( -10, ball_xspeed )

		time.sleep( 1 / 60 )

		# pong_loop(d)



def main(argv=None):
	if argv is None:
		argv = sys.argv

	bg = BackgroundColours.BLACK

	fg = TextColours.YELLOW
	
	d = LCDSysInfo()
	d.clear_lines(TextLines.ALL, bg)
	d.dim_when_idle(False)
	d.set_brightness(255)
	d.save_brightness(255, 255)

	pong_loop(d)
	
	return 0


if __name__ == "__main__":
	sys.exit(main())