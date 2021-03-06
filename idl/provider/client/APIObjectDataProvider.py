#
# DataProvider for APIObjectTemplate.
#

import util

import idl.IDLDataProvider as IDLDataProvider


class APIObjectDataProvider(IDLDataProvider.IDLDataProvider):
    """
    APIObjectDataProvider provides DataObject containing client-side 
    APIObject info.
    """

    def __init__(self, resources):
        IDLDataProvider.IDLDataProvider.__init__(self, resources)

    def addVars(self, data_object, resource):
        """
        Add vars to data_object.  Overrides parent.

        @param data_object: A DataObject instance.
        @param resource: A DataResource instance.

        @return: A DataObject object.
        """
        self.debug("input DataObject: %s"%(data_object), util.DEBUG_VERBOSE)
        
        # TODO: add vars

        
        self.debug("return DataObject: %s"%(data_object), util.DEBUG_VERBOSE)
        
        return data_object
