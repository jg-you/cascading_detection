# -*- coding: utf-8 -*-
# cdtools -- a python library for cascading community detection on networks
# @author: Jean-Gabriel Young <jean.gabriel.young@gmail.com>
#
# cdtools/statistics.py -- provides statistics on network and cluster files.
from .utilities import Uniquify


def UniqueCount(filePath):
    '''
        Return the number of unique occurence of an ID in a file.
    '''
    return len(Uniquify(open(filePath, 'r').read().split()))


def EdgeCount(filePath):
    '''
        Return the number of unique occurence of an ID in a file.
    '''
    return len(open(filePath, 'r').read().split("\n"))
