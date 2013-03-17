#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

#######################################################################
#
# Copyright (c) 2005 Guoqiang Duan. All Rights Reserved.
#
#######################################################################

"""
Utility functions used in Generator. 

$Id: util.py 1652 2007-04-25 07:57:29Z duan $
"""

__version__='$Revision: 1652 $'[11:-2]
__author__ = "Duan Guoqiang (mattgduan@gmail.com)"


import types

DEBUG_ERROR   = -1
DEBUG_QUIET   = 0
DEBUG_NORMAL  = 1
DEBUG_VERBOSE = 2

_mode = DEBUG_NORMAL

FILL_WIDTH = 10

def debug(*args):
    """
    Used for writing debug message.
    """
    if not len(args) > 0:
        return
    
    #print _mode
    elif len(args) == 1 or type(args[0])==type(' '):
        if DEBUG_NORMAL <= _mode:
            print args[0]       
    elif hasattr(args[0], "__class__"):
        if len(args) > 1:
            tag = args[0].__class__.__name__
            if len(tag) < FILL_WIDTH:
                tag += " "*(FILL_WIDTH-len(tag))
            msg = "[%s]%s" % (tag,
                              args[1])
            if len(args) == 2:
                if DEBUG_NORMAL <= _mode:
                    print msg
            elif args[2] <= _mode:
                print msg               
    
    elif args[1] <= _mode:
        print args[0]


def load_class(module_name, class_name):
    mod = __import__(module_name)
    comps = module_name.split('.')
    for comp in comps[1:]:
        mod = getattr(mod, comp)
    if hasattr(mod, class_name):
        return getattr(mod, class_name)
    return None
