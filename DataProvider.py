#######################################################################
#
# Copyright (c) 2005 Guoqiang Duan. All Rights Reserved.
#
#######################################################################

"""
DataProvider uses DataResources to generate DataObject list for 
templates.

$Id: DataProvider.py 94 2006-01-18 06:43:53Z duan $
"""

__version__='$Revision: 94 $'[11:-2]
__author__ = "Duan Guoqiang (mattgduan@gmail.com)"


import DataResource
import util


class DataProvider(object):
    """
    DataProvider base class.
    """
    
    def __init__(self, resources):
        self.__resources = []
        self.addResources(resources)

    def getResources(self):
        return self.__resources
    
    def addResources(self, resources):
        if type(self.__resources) != type([]):
            self.__resources = [self.__resources]
            
        if type(resources) == type([]):
            for res in resources:
                assert issubclass(res.__class__, DataResource.DataResource), \
                            "DataResource class is required."
            self.__resources += resources
        else:
            assert issubclass(resources.__class__, DataResource.DataResource), \
                            "DataResource class is required."
            self.__resources.append(resources)
    
    def setResources(self, resources):
        self.__resources = resources

    def provide(self):
        """
        Provide a list of DataObjects.
        """
        self.debug("calling provide ...", util.DEBUG_VERBOSE)

        do_list = []
        for resource in self.__resources:
            res = resource.resource()
            if not res:
                continue
            do_list += self.generateDataObjects(res)
        
        self.debug("provide generate %s data object."%(len(do_list)), 
                   util.DEBUG_VERBOSE)
        return do_list

    def generateDataObjects(self, resource):
        """
        Generate a list of DataObjects based on one resource.

        @param resource: A resource provided by the DataResource instance.

        @return: A list of DataObject objects.
        """
        self.debug("DataProvider.DataObject has to be overrided "
                   "and implemented by child!")
        return []
        
    debug = util.debug
