import os
import sys
import math
import struct

import pygame

from pylcdsysinfo import LCDSysInfo, TextLines, TextLines, BackgroundColours, TextColours

import xml.etree.ElementTree as ET

from PIL import Image, ImageDraw

LCD_DEVICE_INFO = 12
LCD_SET_BRIGHTNESS = 13
LCD_SAVE_BRIGHTNESS = 14 
LCD_WRITE_TO_FLASH = 15
LCD_WRITE_RAW_TO_FLASH = 16
LCD_DIM_WHEN_IDLE = 17

LCD_DRAW_NET_INFO = 20 
LCD_DRAW_CPU_INFO = 21 
LCD_DRAW_GPU_INFO = 22 
LCD_DRAW_FAN_INFO = 23 

LCD_DRAW_TEXT_ON_LINE = 24
LCD_DRAW_TEXT_ANYWHERE = 25
LCD_CLEAR_TEXT_LINE = 26

LCD_DRAW_ICON = 27
LCD_DRAW_ICON_ANYWHERE = 29

LCD_SET_TEXT_BGCOLOR = 30

LCD_DRAW_MANUAL = 95

LCD_DRAW_MANUAL_FILL = 1
LCD_DRAW_MANUAL_NOFILL = 2
LCD_DRAW_MANUAL_LINE = 3
LCD_DRAW_MANUAL_PROGRESS = 4

char_lookup = {}
char_images = {}

"""

	// UsbSetupPacket
		- request
			
			12 = get device info
			13 = set brightness
			14 = save brightness
			15 = write to flash
			16 = write raw to flash
			17 = dim when idle
	
			20 = draw net info
			21 = draw cpu info
			22 = draw gpu info
			23 = draw fan info

			24 = draw text on line
			25 = draw text anywhere
			26 = clear text line

			27 = draw icon
			29 = draw icon anywhere

			30 = set text bgcolor

			95 = draw rectangle
				- draw mode
				1 = fill
				2 = no fill
				3 = line
				4 = progress bar

		- color
		
		- last
		 0x0

	// ControlTransfer
		- packet

		- buffer

		- length
		 10

		- transferred

}
"""

def cc16(r, g, b):

	# print "\ncol:"

	R = float( r ) / 256 * 32
	G = float( g ) / 256 * 64
	B = float( b ) / 256 * 32

	# print R, G, B

	final = ( int(R) << 11 )
	final = final + ( int(G) << 5 )
	final = final + ( int(B) )

	return final

def cc16o( o ):

	# print "\ncol:"

	R = float( o[0] ) / 256 * 32
	G = float( o[1] ) / 256 * 64
	B = float( o[2] ) / 256 * 32

	# print R, G, B

	final = ( int(R) << 11 )
	final = final + ( int(G) << 5 )
	final = final + ( int(B) )

	return final

class LCDSysInfo( LCDSysInfo ):

	screen = None

	screenBuffer = [ [ (0,0,0) for x in range( 320 ) ] for y in range( 240 ) ]

	# def __init__(self, index=0):

		# super(LCDSysInfo, self).__init__( index )

		# self.screen = pygame.display.set_mode( [320, 240] )


	def fill_rectangle(self, X1, Y1, X2, Y2, colour):

		X1 = max(0, min(X1, 320))

		Y1 = max(0, min(Y1, 240))

		X2 = max(0, min(X2, 320))

		Y2 = max(0, min(Y2, 240))

		ba = struct.pack(
			"<BBBBBBBBBB",
			Y1 >> 8,
			Y1 & 0xFF,
			X1 >> 8,
			X1 & 0xFF,
			Y2 >> 8,
			Y2 & 0xFF,
			X2 >> 8,
			X2 & 0xFF,
			0 >> 8,
			0 & 0xFF
		)

		'''
		# single check
		if X2 - X1 == 1 and Y2 - Y1 == 1 and self.screenBuffer[Y1][X1] == colour:
			# print( "Already has single pixel, " + str(colour) )			
			return False


		# area check
		hasAllPixels = True
		for y in range( Y1, Y2 ):
			for x in range( X1, X2 ):
				if self.screenBuffer[y][x] != colour:
					hasAllPixels = False
					break

		if hasAllPixels:
			# print( "Already has area, " + str(colour) )
			return False
		'''

		# fill buffer
		for y in range( Y1, Y2 ):
			for x in range( X1, X2 ):
				self.screenBuffer[y][x] = colour


		self.devh.controlMsg(0x40, LCD_DRAW_MANUAL, ba, LCD_DRAW_MANUAL_FILL, cc16o( colour ), self.usb_timeout_ms)

		# pygame.draw.rect( self.screen, colour, [X1, Y1, X2-X1, Y2-Y1] )

		# pygame.display.flip()

		# pygame.display.update()

		# pygame.event.wait()

	'''
	public static void Draw_line(int Y1, int X1, int Y2, int X2, int color_value) {
        UsbSetupPacket packet = new UsbSetupPacket((byte)(UsbCtrlFlags.Direction_Out | UsbCtrlFlags.RequestType_Vendor), (byte)95,
           (short)3, (short)color_value, (short)0x0);
        byte[] ba = new byte[10];
        ba[0] = (byte)(Y1 / 256);
        ba[1] = (byte)(Y1 % 256);
        ba[2] = (byte)(X1 / 256);
        ba[3] = (byte)(X1 % 256);
        ba[4] = (byte)(Y2 / 256);
        ba[5] = (byte)(Y2 % 256);
        ba[6] = (byte)(X2 / 256);
        ba[7] = (byte)(X2 % 256);
        ba[8] = (byte)(0 / 256);
        ba[9] = (byte)(0 % 256);
        if (LCDDrive.MyUsbDevice != null) { LCDDrive.MyUsbDevice.ControlTransfer(ref packet, ba, 10, out bytes_transferred); }
    }
    '''
	def draw_line(self, X1, Y1, X2, Y2, colour):

		X1 = max(0, min(X1, 320))
		Y1 = max(0, min(Y1, 240))
		X2 = max(0, min(X2, 320))
		Y2 = max(0, min(Y2, 240))

		sendBytes = struct.pack(
			"<BBBBBBBBBB",
			Y1 >> 8,
			Y1 & 0xFF,
			X1 >> 8,
			X1 & 0xFF,
			Y2 >> 8,
			Y2 & 0xFF,
			X2 >> 8,
			X2 & 0xFF,
			0 >> 8,
			0 & 0xFF
		)

		self.devh.controlMsg(0x40, LCD_DRAW_MANUAL, sendBytes, LCD_DRAW_MANUAL_LINE, cc16o( colour ), self.usb_timeout_ms)



	def fill_rectangle_rel(self, x, y, width, height, colour):
		self.fill_rectangle(x, y, x + width, y + height, colour)

	def draw_image(self, filename, screen_x, screen_y, opacity = 1):

		"""Given `filename`, open image and display on LCD
        screen_x and screen_y are offsets
		"""
		im = Image.open( filename )
		im = im.convert('RGBA')  # below code expects RGBA, e.g. below will fail with a BMP without Alpha
		width = im.size[0]
		height = im.size[1]
		print( "draw image: " + filename + ", " + str( width ) + "x" + str( height ) )
		self.draw_image_im(im, screen_x, screen_y, opacity=opacity)

	def draw_image_im(self, im, screen_x, screen_y, opacity=1):
		"""
        `im` is a PIL Image, this should be in RGBA format/mode
        screen_x and screen_y are offsets

        Does NOT write to flash memory.
        NOTE this is not fast, can take between 2-4 minutes for a 320x240 image
        (135-235 seconds) on Raspberry Pi 3B+ depending on complexity of image.
        Speed is due to converting each pixel and then writing/sending each pixel one-by-one
		"""
		assert im.mode == 'RGBA'
		pix = im.load()

		width = im.size[0]
		height = im.size[1]


		for y in range(0, height):

			#if y > 240:
			#	break

			x = 0

			while x < width:

				#if x > 320:
				#	break

				col = pix[x, y]

				if len(col) <= 2:
					r = col[0]
					g = col[0]
					b = col[0]
					a = col[1]

				else:
					r = col[0]
					g = col[1]
					b = col[2]
					a = col[3]

				aa = ( a * opacity ) / 255

				pw = 1

				if x + pw < width:
					while x + pw < width:

						lk = pix[ x + pw, y]

						if len(lk) <= 2:

							if(lk[0] == r and lk[1] == a):
								pw += 1
							else:
								break

						else:

							if(lk[0] == r and lk[1] == g and lk[2] == b and lk[3] == a):
								pw += 1
							else:
								break

				final_x = screen_x + x
				final_y = screen_y + y

				if final_x + pw > 320:
					break

				if final_y + 1 > 240:
					return

				#if final_y < 0 or final_y + 1 > 240:
				#	continue

				self.fill_rectangle(final_x, final_y, final_x + pw, final_y + 1, ( r * aa, g * aa, b * aa ) )

				x = min(x + pw, width)

	def generate_font_lookup( self, font ):

		tree = ET.parse( font + ".xml")

		root = tree.getroot()

		char_lookup[font] = {}

		for lt in root.iter('Char'):

			code = lt.get('code')

			entry = {}

			entry["width"] = int( lt.get('width') )

			rect = lt.get('rect').split(" ")

			entry["l_x"] = int( rect[0] )
			entry["l_y"] = int( rect[1] )
			entry["l_w"] = int( rect[2] )
			entry["l_h"] = int( rect[3] )

			offset = lt.get('offset').split(" ")

			entry["offset_x"] = int( offset[0] )
			entry["offset_y"] = int( offset[1] )

			char_lookup[ font ][ code ] = entry

		
		print("lookup table for " + font + " created")


	def draw_text(self, text, x, y, font, colour=None, overflow=True):

		global char_lookup, char_images

		chars = list(text)

		if not font in char_lookup:

			print("no lookup table for " + font)

			self.generate_font_lookup( font )
			
			
		# print( char_lookup[ font ] )


		# for child in root:
		# 	print child.tag, child.attrib

		if not font in char_images:
			im = Image.open( font + ".png" )
			char_images[font] = im.load()
			print("image loaded for " + font)

		pix = char_images[font]

		global_x = x
		global_y = y

		total_width = 0
		total_height = 0

		fontsize = font.split("_")
		fontsize = int( fontsize[ len(fontsize) - 1 ] )

		# loop through characters in string
		for char in chars:

			# newline
			if char == "\n":
				global_y += fontsize
				global_x = x

			# if character exists in lookup table
			if char in char_lookup[ font ]:

				cdef = char_lookup[ font ][ char ]

				# local_x = 0
				# local_y = 0
				
				if cdef["l_h"] + cdef["offset_y"] > total_height:
					total_height = cdef["l_h"] + cdef["offset_y"]

				rect_height = 1

				# letter_x = global_x + cdef["offset_x"]
				# letter_y = global_y + cdef["offset_y"]
				# letter_width = cdef["l_w"]
				# letter_height = cdef["l_h"]

				# print( "" )
				# print( char )
				# print( str(letter_x) + ", " + str(letter_y) )
				# print( str(letter_width) + "x" + str(letter_height) )

				# clear previous
				
				'''
				for img_y in range( letter_y, letter_y + letter_height ):
					for img_x in range( letter_x, letter_x + letter_width ):
						# print( str(img_x) + "x" + str(img_y) )
						if self.screenBuffer[ img_y ][ img_x ] != (0, 0, 0):
							self.fill_rectangle_rel(img_x, img_y, 1, 1, (0, 0, 0) )
							# print("has in screen buffer " + str(img_x) + " " + str(img_y) )

				'''
				
				# self.fill_rectangle_rel(letter_x, letter_y, letter_width, letter_height, (255, 0, 0) )

				# character y
				map_y = cdef["l_y"]
				while map_y < cdef["l_y"] + cdef["l_h"]:					
					
					# character x
					map_x = cdef["l_x"]
					while map_x < cdef["l_x"] + cdef["l_w"]:
						
						col = pix[ map_x, map_y ]
						
						r = col[0]
						g = col[1]
						b = col[2]
						a = col[3]

						# skip pixel if alpha
						if a == 0:
							map_x += 1
							continue

						aa = a / 255 # divisible alpha

						rect_width = 1

						# optimize i think
						while map_x + rect_width < cdef["l_x"] + cdef["l_w"]:

							lk = pix[ map_x + rect_width, map_y]

							if(lk[0] == r and lk[1] == g and lk[2] == b and lk[3] == a):
								rect_width += 1
							else:
								break

							# final_x = screen_x + x
							# final_y = screen_y + y

						final_x = global_x + ( map_x - cdef["l_x"] ) + cdef["offset_x"]
						final_y = global_y + ( map_y - cdef["l_y"] ) + cdef["offset_y"]

						if colour:
							self.fill_rectangle_rel(final_x, final_y, rect_width, rect_height, colour )
						else:
							self.fill_rectangle_rel(final_x, final_y, rect_width, rect_height, ( int(r * aa) , int(g * aa), int(b * aa) ) ) # alpha only works on black

						map_x += rect_width

					
					# local_y += 1

					map_y += 1

				
				if overflow and global_x + cdef["width"] + cdef["width"] > 320:
					global_x = x
					global_y += 10
					# print("text new line")
				else:
					global_x += cdef["width"]
					total_width += cdef["width"]
					# print("text new char, " + str( total_width ) )

			else:
				print("char not found: " + char)


		return total_width, total_height


	def dump_buffer( self, dest ):

		im = Image.new("RGB", ( 320, 240 ) )

		dr = ImageDraw.Draw(im)

		for y in range( 0, 240 ):

			for x in range( 0, 320 ):

				# print( str(x) + "x" + str(y) + ": " + str( self.screenBuffer[y][x] ) )

				dr.point( (x, y), self.screenBuffer[y][x] )

		im.save( dest, "PNG")

		del dr
		del im

		print("dumped to " + dest)


class LCDText( object ):

	def __init__(self, lcd, x, y, font):
		
		self.lcd = lcd

		self.x = x
		self.y = y

		self.font = font
		
		self.oldText = ""
		self.text = ""

		self.width = 0
		self.height = 0

		self.letterPositions = []


	def draw( self ):
		
		# print( "Draw text: " + str(self.text) )
		
		# lazy clear
		'''
		if self.width > 0 and self.height > 0:
			# print("Clear text")
			self.lcd.fill_rectangle_rel(self.x, self.y, self.width, self.height, ( 0, 0, 0 ) )
		
		self.width, self.height = self.lcd.draw_text( self.text, self.x, self.y, self.font, overflow=False )
		'''

		# print( str(self.width) + "x" + str(self.height) )
		
		'''
		if len( self.oldText ) > 0:

			for i, letter in enumerate(self.text):

				if len( self.oldText ) >= i and self.oldText[i] != letter:
					# print( "Different: " + str( letter ) )
					self.lcd.fill_rectangle_rel( self.x, self.y, self.width, self.height, ( 255, 0, 0 ) )

					self.lcd.draw_text( letter, self.x, self.y, self.font, overflow=False )

		else:

			self.width, self.height = self.lcd.draw_text( self.text, self.x, self.y, self.font, overflow=False )
		'''

		if len(self.oldText) != len(self.text):
			print("diff length, clear whole screen")
			self.lcd.fill_rectangle_rel( self.x, self.y, self.width, 110, ( 0, 0, 0 ) )

		for i, letter in enumerate(self.text):

			if len(self.oldText) > 0 and len(self.oldText) >= i and self.oldText[i] != letter:
				# print("old letter: " + str(self.oldText[i]) + " = " + str(letter) + " @ " + str(i) )
				self.lcd.fill_rectangle_rel( self.x + ( i * 60 ), self.y, 60, 110, ( 0, 0, 0 ) )

			self.lcd.draw_text( letter, self.x + ( i * 60 ), self.y, self.font, overflow=False )

			self.width = self.x + ( i * 60 ) + 60 


	def setText( self, text ):
		# print( "Set text: " + str(text) )
		self.oldText = self.text
		self.text = text
		self.draw()
