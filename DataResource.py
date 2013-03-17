#######################################################################
#
# Copyright (c) 2005 Guoqiang Duan. All Rights Reserved.
#
#######################################################################

"""
DataResource is used by DataProvider to get resources. It contains the
basic resource dict and makes some necessary resources, e.g. database 
handler, file handler, etc.

$Id: DataResource.py 1652 2007-04-25 07:57:29Z duan $
"""

__version__='$Revision: 1652 $'[11:-2]
__author__ = "Duan Guoqiang (mattgduan@gmail.com)"


import util


class DataResource(object):
    """
    The base DataResource class.
    """

    def __init__(self, config):
        self.config = config

    def resource(self):
        return self.config

    debug = util.debug
