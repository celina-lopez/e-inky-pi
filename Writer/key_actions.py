#!/usr/bin/python
# -*- coding:utf-8 -*-

from pynput.keyboard import Listener, Key

class OnPress:
    def __init__(self, editor):
        self.editor = editor
        self.actions = {
            "char": lambda char: self.normal_addition(char),
            Key.space: lambda: self.normal_addition(" "),
            Key.tab: lambda: self.editor.restore_snapshot(),
            Key.esc: lambda: self.exit_editor(),
            Key.delete: lambda: self.delete(),
            Key.enter: lambda: self.enter(),
        }

    def normal_addition(self, char):
        buff = self.editor.buffer.insert(char, self.editor.cursor.x, self.editor.cursor.y)
        cursor = self.editor.cursor.right(buff)
        character = self.editor.character.new(char)
        return [buff, cursor, character]

    def exit_editor(self):
        return False

    def delete(self):
        if self.editor.cursor > 0:
            buff = self.editor.buffer.delete(self.editor.cursor.x, self.editor.cursor.y)
            cursor = self.editor.cursor.left(buff)
            character = self.editor.character.new("")
        return [buff, cursor, character]
    
    def enter(self):
        buff = self.editor.buffer.split_line(self.editor.cursor.x, self.editor.cursor.y)
        cursor = self.editor.cursor.down(buff).move_to_y(0)
        character = self.editor.character.new("\n")
        return [buff, cursor, character]