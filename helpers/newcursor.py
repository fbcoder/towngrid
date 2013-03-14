#!/usr/bin/env python
import pygame
from pygame.locals import *

class CursorType:
	normal = 0
	destruct = 1
	question = 2
	build = 3
	
def setCursor(mode=CursorType.normal):
	hotspot = (0,0)
	thickarrow_strings = ""
	if mode == CursorType.normal:
		thickarrow_strings = (            #sized 24x24
			 #"XXXXXXXXXXXXXXXXXXXXXXXX"
			  "XXXXXXXXXXXXXXXXXXXXXX  ",
			  "XX...................XX ",
			  "XX....................XX",
			  "XX....................XX",
			  "XX...................XX ",
			  "XX.......XXXXXXXXXXXXX  ",
			  "XX........XX            ",
			  "XX.........XX           ",
			  "XX..........XX          ",
			  "XX...........XX         ",
			  "XX............XX        ",
			  "XX....X........XX       ",
			  "XX....XXX.......XX      ",
			  "XX....XXXX.......XX     ",
			  "XX....XX XX......XX     ",
			  "XX....XX  XX.....XX     ",
			  "XX....XX   XX....XX     ",
			  "XX....XX    XXXXXXX     ",
			  "XX....XX                ",
			  "XX....XX                ",
			  "XX....XX                ",
			  "XX....XX                ",
			  " XX..XX                 ",
			  "   XX                   ")			
	if mode == CursorType.build:
		thickarrow_strings = (            #sized 24x24
			  "XXXXXXXXXXXXXXXXXXXXXXXX",
			  "XX....X...X...X...X...XX",
			  "XX....X...X...X...X...XX",
			  "XX....................XX",
			  "XX....................XX",
			  "XX....XXXXXXXXXXXXXXXXXX",
			  "XX....XX                ",
			  "XX....XX                ",
			  "XX....XX                ",
			  "XX....XX                ",
			  "XX....XX                ",
			  "XX....XX                ",
			  "XX....XX                ",
			  "XX....XX                ",
			  "XX....XX                ",
			  "XX....XX                ",
			  "XX....XX                ",
			  "XX....XX                ",
			  "XX....XX                ",
			  "XX....XX                ",
			  "XX....XX                ",
			  "XX....XX                ",
			  "XX....XX                ",
			  "XXXXXXXX                ")
			 #"                        "
	elif mode == CursorType.destruct:
		thickarrow_strings = (            #sized 24x24
			 #"XXXXXXXXXXXXXXXXXXXXXXXX"
			  "XX                      ",
			  "X.XX                    ",
			  "X..XX                   ",
			  " X...X                  ",
			  "  X..X                  ",
			  "   XX                   ",
			  "     X                  ",
			  "    XXXXXXX             ",
			  "   X..X...XX            ",
			  "    XXXXXXXX            ",
			  "     X......X           ",
			  "      X......X          ",
			  "       X......X         ",
			  "        X......X        ",
			  "         X......X       ",
			  "          X......X      ",
			  "           X......X     ",
			  "            X......X    ",
			  "             X......X   ",
			  "              X......X  ",
			  "               X......X ",
			  "                X......X",
			  "                 X.....X",
			  "                  XXXXXX")
			 #"                        "
	elif mode == CursorType.question:
		thickarrow_strings = (            #sized 24x24
			 #"XXXXXXXXXXXXXXXXXXXXXXXX"
			  "       XXXXXXXXXXX      ",
			  "     XX...........XX    ",
			  "   XX..............XX   ",
			  "  XX....XXXXXXXX.....XX ",
			  " XX....XXX     XX.....XX",
			  " XX....XX       XX....XX",
			  "  XX....XX      XX....XX",
			  "   XX....XX    XX....XX ",
			  "    XXXXXXX   XX....XX  ",
			  "             XX....XX   ",
			  "            XX....XX    ",
			  "           XX....XX     ",
			  "           XX....XX     ",
			  "           XX....XX     ",
			  "           XX....XX     ",
			  "           XX....XX     ",
			  "           XX....XX     ",
			  "           XX....XX     ",
			  "           XX....XX     ",
			  "      XXXXXXX....XXXXXX ",
			  "        XX.........XX   ",
			  "          XX.....XX     ",
			  "            XX.XX       ",
			  "              X         ")
			 #"                        "
		hotspot=(12,23)
			 
			 
	datatuple, masktuple = pygame.cursors.compile( thickarrow_strings,black='.', white='X', xor='o')
	pygame.mouse.set_cursor( (24,24), hotspot, datatuple, masktuple )
