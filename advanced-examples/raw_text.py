from lcd_drawing import LCDSysInfo, LCDText, TextLines, BackgroundColours, TextColours

font = 'fonts/vcr_osd_mono_regular_20'
# NOTE RGB tuples, not BackgroundColours nor TextColours
COL_WHITE = ( 255, 255, 255 )
COL_BLACK = ( 0, 0, 0 )

bg = BackgroundColours.BLACK
fg = TextColours.YELLOW

d = LCDSysInfo()
d.clear_lines(TextLines.ALL, bg)

#d.draw_text(string will wrap, X, Y, font name, RGB colour tuple)
# X, Y are screen pixel coords (e.g. old hard 320*240
d.draw_text('Hello World', 100, 100, font, COL_WHITE)
d.draw_text('Hello World', 100, 200, font, COL_WHITE)


# unclear on coord system, looks like screen pixels
# output appears to be double spaced
t = LCDText(d, 50, 50, font)
t.setText('Hello World')

