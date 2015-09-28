# -*- coding: utf-8 -*-
# cdtools -- a python library for cascading community detection on networks
# @author: Jean-Gabriel Young <jean.gabriel.young@gmail.com>
#
# cdtools/CPA/__init__.py -- Init script of the CPA submodule.

# Notes on CPA:
#   The Clique Percolation Algorithm was introduced by G. Palla et al. in
#
#       "Uncovering the overlapping community structure
#        of complex networks in nature and society"
#        Nature 435, 814–818 (2005)
#
#   We use the official CPA implementation which requires a (free)
#   license, which is *not* provided with cdtools, for obvious reasons.
#   To use this module, one must request a license [1] and save it in
#
#       [..]/cascading_detection/cdtools/CPA/license/
#
#   Do not forget to configure the license in 
# 
#       [..]/cascading_detection/cdtools/CPA/CPA_conf.yml
# 
#   Bugs and other inquiries regarding this algorithm in particular should be
#   sent to the authors of CFinder as well.
#
#   [1] Contact information:
#           Email: CFinder@hal.elte.hu
#           Website: http://CFinder.org

from .detection import Detect

__all__ = [Detect]
