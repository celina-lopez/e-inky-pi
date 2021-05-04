#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')

if os.path.exists(libdir):
    sys.path.append(libdir)


LINE_STEP 	=   20
CHAR_WIDTH 	=   10
EPD_HEIGHT 	=	128
EPD_WIDTH 	=  	296

import logging
from Writer.writer import Editor, Display
from PIL import Image,ImageDraw,ImageFont
import traceback

logging.basicConfig(level=logging.DEBUG)

try:    
    font18 = ImageFont.truetype(os.path.join(picdir, 'fontgoogle.ttf'), 18)
    
#  start
    Himage = Image.new('1', (EPD_HEIGHT, EPD_WIDTH), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(Himage)

    edit = Editor("sample.txt", draw, Himage, font18)
    edit.run()
            
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    exit()
