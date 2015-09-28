# -*- coding: utf-8 -*-
# cdtools -- a python library for cascading community detection on networks
# @author: Jean-Gabriel Young <jean.gabriel.young@gmail.com>
#
# cdtools/GCE/__init__.py -- Init script of the GCE submodule.

# Notes on GCE:
#   GCE was introduced by Conrad. Lee et al. in
#
#       "Detecting highly overlapping community structure by 
#        greedy clique expansion"
#        arXiv:1002.1827  (2010)
#
#   Bugs and other inquiries regarding this algorithm can be sent to
#   the original author.
#
#   The source code was modified to fix includes bugs.
#   (see graph_loading.cpp)
#
#   Official website:
#       https://sites.google.com/site/greedycliqueexpansion/
#
#   The full source is copied in
#       [..]cascading_detection/cdtools/GCE/bin/
#   for convenience, but can also be obtained from
#       https://sites.google.com/site/greedycliqueexpansion/
#           benchmarking---datasets-and-tools/GCEimpl_r2011-11-06.tgz

from .detection import Detect

__all__ = [Detect]
