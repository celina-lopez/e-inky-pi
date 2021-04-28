#!/usr/bin/python
# -*- coding:utf-8 -*-

from Writer.utils import dupe

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

    def delete(self, x, y):
        lines = dupe(self.lines)
        lines[x] = lines[x][:y - 1 ]  + lines[x][y:]
        return Buffer(lines)
    
    def split_line(self, x, y):
        lines = dupe(self.lines)
        lines[x] = [lines[x][:y]] 
        lines.append([lines[x][y:]])
        return Buffer(lines)
