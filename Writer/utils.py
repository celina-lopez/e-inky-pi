#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
import os

def read_file(file):
    document_direc = os.path.join(
        os.path.dirname(
            os.path.dirname(
                os.path.dirname(
                    os.path.realpath(__file__))))
        , 'documents')

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