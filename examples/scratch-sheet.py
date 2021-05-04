#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

LINE_STEP =     20
CHAR_WIDTH =    10

import logging
from waveshare_epd import epd2in9
from Writer.writer import Editor, Display
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

logging.basicConfig(level=logging.DEBUG)

try:
    epd = epd2in9.EPD()
    logging.info("init and Clear")
    epd.init(epd.lut_full_update)
    epd.Clear(0xFF)
    
    font18 = ImageFont.truetype(os.path.join(picdir, 'fontgoogle.ttf'), 18)
    
    logging.info("Begin writer app (•ө•)")
    epd.init(epd.lut_partial_update)    
    epd.Clear(0xFF)
    Himage = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(Himage)
    # have line height in display

    line_height = 0
    character_width = CHAR_WIDTH

    def drawing(char):
        draw.text((character_width, line_height), char, font = font18, fill = 0)
        character_width += CHAR_WIDTH
        epd.display(epd.getbuffer(Himage))

    edit = Editor("sample.txt", drawing)
    edit.run()
    
    logging.info("Clear...")
    epd.init(epd.lut_full_update)
    epd.Clear(0xFF)
    
    logging.info("Goto Sleep...")
    epd.sleep()
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd2in9.epdconfig.module_exit()
    exit()
