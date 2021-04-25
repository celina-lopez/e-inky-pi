#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
from pynput.keyboard import Listener, Key
import math

# Waveshare e-ink specs 
CHAR_LENGTH =   32
LINES =         5

# Document directory
document_direc = os.path.join(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(
                os.path.realpath(__file__))))
    , 'documents')


def read_file(file):
    with open(os.path.join(document_direc, file), 'r') as reader:
            lines = []
            for line in reader:
                lines.append(line)
            return lines

def dupe(original_list):
    new_list = []
    for x in original_list:
        new_list.append(x)
    return new_list

class Display: 
    def __init__(self, lines):
        self.lines = lines

    def lineable(self):
        # Cut lines to fit on Waveshare screen
        new_lines = []
        for line in self.lines:
            iteration_num = math.ceil(len(line) / CHAR_LENGTH)
            for x in range(iteration_num):
                starting_pos = x * CHAR_LENGTH
                ending_pos = CHAR_LENGTH + starting_pos
                new_lines.append(line[starting_pos:ending_pos])
        return new_lines

    def max_display(self):
        return Display(self.lines[:LINES])


class Editor:
    def __init__(self, file):
        self.cursor = Cursor()
        self.buffer = Buffer(read_file(file))
        self.character = Character()
        self.history = []

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

    def on_release(self, key):
        pass

    def set_variables(self, char):
        self.buffer = self.buffer.insert(char, self.cursor.x, self.cursor.y)
        self.cursor = self.cursor.right(self.buffer)
        self.character = Character(char)

    def on_press(self, key):
        if hasattr(key, 'char'):
            self.save_snapshot()
            self.set_variables(str(key)[1])
        elif key == Key.space:
            self.set_variables(" ")
        elif key == Key.enter:
            self.set_variables("\n")
        elif key == Key.tab:
            self.restore_snapshot()
        elif key == Key.esc:
            return False
        elif key == Key.delete:
            self.save_snapshot()
            if self.cursor > 0:
                self.buffer = self.buffer.delete(self.cursor.x, self.cursor.y)
                self.cursor = self.cursor.left(self.buffer)
                self.character = Character()
        elif key == Key.enter:
            self.save_snapshot()
            self.buffer = self.buffer.split_line(self.cursor.x, self.cursor.y)
            self.cursor = self.cursor.down(self.buffer).move_to_y(0)
            self.character = Character("\n")
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

class Buffer:
    def __init__(self, lines):
        self.lines = lines

    def render(self):
        for line in self.lines:
            print(line + "\n")
            # view in console for now

    def insert(self, char, x, y):
        lines = dupe(self.lines)
        lines[x] = lines[x][:y] + char + lines[x][y:]
        return Buffer(lines)

    def delete(x,y):
        lines = dupe(self.lines)
        lines[x] = lines[x][:y - 1 ]  + lines[x][y:]
        return Buffer(lines)
    
    def split_line(x, y):
        lines = dupe(self.lines)
        lines[x] = [lines[x][:y]]  + [lines[x][y:]]
        return Buffer(lines)

class Cursor:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.x_max = 100
        self.y_max = 100

    def up(self, buff):
        return Cursor(self.x - 1, self.y).clamp(buff)

    def down(self, buff):
        return Cursor(self.x + 1, self.y).clamp(buff)

    def right(self, buff):
        return Cursor(self.x, self.y + 1).clamp(buff)

    def left(self, buff):
        return Cursor(self.x, self.y - 1).clamp(buff)

    def clamp(self, buff):
        x = max(min(self.x, self.line_height(buff)), 0)
        y = max(min(self.y, self.line_length(buff)), 0)
        return Cursor(x, y)

    def move_to_y(self, y):
        return Cursor(self.x, y)

    def line_length(self, buff):
        return len(buff.lines[self.x])

    def line_height(self, buff):
        return len(buff.lines)

class Character:
    def __init__(self, char=""):
        self.char = char

