#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os

from pynput.keyboard import Listener, Key
from Writer.utils import read_file
from Writer.buffer import Buffer
from Writer.key_actions import OnPress
from Writer.cursor import Cursor
import math

# Waveshare e-ink specs 
CHAR_LENGTH     =   32
LINES           =   5 
LINE_STEP       =   20
CHAR_WIDTH      =   10
EPD_HEIGHT      =   128
EPD_WIDTH       =   296

class Display: 
    def __init__(self, lines):
        self.lines = lines

    def lineable(self):
        # when starting the raspberry pi, show viewable lines
        new_lines = []
        for line in self.lines:
            iteration_num = math.ceil(len(line) / CHAR_LENGTH)
            for x in range(iteration_num):
                starting_pos = x * CHAR_LENGTH
                ending_pos = CHAR_LENGTH + starting_pos
                new_lines.append(line[starting_pos:ending_pos])
        return new_lines

    def max_display(self, x):
        return self.lineable()[x: x + LINES]

# epd = false for debugger!
class Editor:
    def __init__(self, file, draw, image, font, epd=False):
        self.cursor = Cursor()
        self.buffer = Buffer(read_file(file))
        self.character = Character()
        self.history = []
        self.draw = draw
        self.image = image
        self.font = font
        self.epd = epd

    def render(self):
        self.buffer.render()

    def run(self):
        with Listener(
            on_press=self.on_press,
            on_release=self.on_release,
        ) as listener:
            self.render()
            for _ in range(10):
                if not listener.running:
                    break
            listener.join()

    def save_snapshot(self):
        self.history.append([self.buffer, self.cursor, self.character]) 

    def restore_snapshot(self):
        self.buffer, self.cursor, self.character = self.history.pop()

    def display_epd(self):
        if self.epd:
            self.epd.display(self.epd.getbuffer(self.image))
        else:
            self.image.show()

    def on_release(self, key):
        if hasattr(key, 'char'):
            coordinates = (self.cursor.y * CHAR_WIDTH, self.cursor.x * LINE_STEP)
            self.draw.text(coordinates, self.character.char, font = self.font, fill = 0)
        elif key == Key.tab:
            # rerender whole screen
            self.draw.rectangle((0, 0, EPD_HEIGHT, EPD_WIDTH), fill = 255)
            num = 0
            for line in Display(self.buffer.lines).max_display(0):
                self.draw.text((num * CHAR_WIDTH, num * LINE_STEP), line, font = self.font, fill = 0)
                num += 1
        elif key == Key.enter:
            # delete this debugger
            self.display_epd()

        if self.epd:
            self.display_epd()

    def on_press(self, key):
        keyable = OnPress(self)
        if hasattr(key, 'char'):
             [self.buffer, self.cursor, self.character] = keyable.actions['char'](str(key)[1])
        elif key in [Key.space, Key.tab, Key.esc, Key.delete, Key.enter]:
            [self.buffer, self.cursor, self.character] = keyable.actions[key]()
        elif key == Key.up:
            self.cursor = self.cursor.up(self.buffer)
        elif key == Key.down:
            self.cursor = self.cursor.down(self.buffer)
        elif key == Key.right:
            self.cursor = self.cursor.right(self.buffer)
        elif key == Key.left:
            self.cursor = self.cursor.left(self.buffer)
        else:
            return

class Character:
    def __init__(self, char=""):
        self.char = char

    def new(self, char):
        return Character(char)

