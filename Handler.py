#######################################################################
#
# Copyright (c) 2005 Guoqiang Duan. All Rights Reserved.
#
#######################################################################

"""
Handler is used to handle output string.
"""

__version__='$Revision: 1709 $'[11:-2]
__author__ = "Duan Guoqiang (mattgduan@gmail.com)"


import os
import util


class BaseHandler(object):

    def __init__(self):
        object.__init__(self)
    
    def handle(self, content, config={}):
        self.debug("try to handle data with config: %s"%(config))

    debug = util.debug


class SimpleHandler(BaseHandler):

    def handle(self, content, config={}):
        #print config
        print os.path.join(config['path'], config['filename'])
        print content

