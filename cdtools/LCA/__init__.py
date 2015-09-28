# -*- coding: utf-8 -*-
# cdtools -- a python library for cascading community detection on networks
# @author: Jean-Gabriel Young <jean.gabriel.young@gmail.com>
#
# cdtools/LCA/__init__.py -- Init script of the LCA submodule.

# Notes on LCA:
#   The Clique Percolation Algorithm was introduced by Y.Y. Ahn et al. in
#
#       "Link communities reveal multiscale complexity in networks"
#        Nature 466, 761–764 (2010)
#
#   We use a modified version of the official c++ implementation which is
#   available under a free GNU license. It is somewhat slower and bulkier than
#   the official version, but it has the crucial advantage of being able to
#   handle arbitrary edge lists (non-contiguous integers)
#
#   Bugs and other inquiries regarding this algorithm can be sent to me OR
#   the original authors.
#
#   The full source (and license) is copied in
#       [..]/cascading_detection/cdtools/LCA/src/
#   for convenience, but can also be obtained from
#       https://github.com/bagrow/linkcomm
#       https://github.com/jg-you/linkcomm

from .detection import Detect

__all__ = [Detect]
