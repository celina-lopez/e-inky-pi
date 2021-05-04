#!/usr/bin/python
# -*- coding:utf-8 -*-

class Cursor:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.x_max = 5
        self.y_max = 32

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
