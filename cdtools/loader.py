# -*- coding: utf-8 -*-
# cdtools -- a python library for cascading community detection on networks
# @author: Jean-Gabriel Young <jean.gabriel.young@gmail.com>
#
# cdtools/loader.py -- load and save networks and clusters files.
from .utilities import Group
from sortedcontainers import SortedList


def LoadNumberFile(path):
    '''
        Read the content of a files of number as a list
        of lists (of string).
    '''
    fileContent = open(path, 'r').read().split("\n")
    fileContent = [fileContent[idx].split()
                   for idx in range(0, len(fileContent) - 1)]
    return SortedList([list(Group(x)) for x in fileContent])


def StripOutput(line):
    '''
        A SortedList of tuples comes with *a lot* of useless decorations.
        This function strips 'em all.
    '''
    line = str(line)
    line = line.replace("(", "").replace(")", "")  # Delete brackets
    line = line.replace("[", "").replace("]", "")  # Delete square brackets
    line = line.replace(",", "")  # Delete commas
    return line


def SaveSortedList(sortedListOfTuples, path):
    '''
        Write a SortedList of tuple (pairs) to a file.
    '''
    with open(path, 'w') as f:
        for line in sortedListOfTuples:
            f.write(StripOutput(line) + "\n")
