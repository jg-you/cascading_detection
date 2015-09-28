# -*- coding: utf-8 -*-
# cdtools -- a python library for cascading community detection on networks
# @author: Jean-Gabriel Young <jean.gabriel.young@gmail.com>
#
# cdtools/utilities.py -- handy functions for cdtools.
from os import makedirs, path
from shutil import rmtree
from re import sub

def Group(lst):
    for i in range(0, len(lst), 2):
        a = int(lst[i])
        b = int(lst[i + 1])
        if a < b:
            yield (a, b)
        else:
            yield (b, a)


def Uniquify(seq):
    '''
        Remove duplicates from a list.
    '''
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


def MakeDir(path):
    ''' Small wrapper around os.makedirs that makes it ignore error.'''
    try:
        makedirs(path, 0o755)
    except OSError:
        pass


def PreparePaths(basePath):
    ''' Prepare output paths for an algorithm.'''
    rmtree(path.join(basePath, "clusters"), ignore_errors=True)
    rmtree(path.join(basePath, "edgelists"), ignore_errors=True)
    rmtree(path.join(basePath, "statistics"), ignore_errors=True)
    MakeDir(path.join(basePath, "clusters"))
    MakeDir(path.join(basePath, "edgelists"))
    MakeDir(path.join(basePath, "statistics"))


def DeleteCommas(path):
    '''Delete commas from a file '''
    with open(path, 'r') as f:
        content = f.read()
    with open(path, 'w') as f:
        f.write(content.replace(',', ' '))


def DeleteComments(path):
    '''Delete comment from a file '''
    with open(path, 'r') as f:
        content = f.read()
    with open(path, 'w') as f:
        f.write(sub("#.*\n", "", content))


def drange(start, stop, step):
    '''
        Floating range.
        Less precise than scipy.arange, but doesn't require a huge library.
        http://stackoverflow.com/a/477610/1851837
    '''
    r = start
    while r < stop:
        yield r
        r += step
