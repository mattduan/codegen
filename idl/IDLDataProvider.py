#
# DataProvider for IDL specific templates.
#

import util

import DataProvider
import idl.IDLParser as IDLParser


class IDLDataProvider(DataProvider.DataProvider):
    """
    IDLDataProvider provides DataObject containing idl specific
    variables.
    """

    def __init__(self, resources):
        DataProvider.DataProvider.__init__(self, resources)

    def generateDataObjects(self, resource):
        """
        Generate and return a DataObject.  Overrides parent.

        @param resource: A resource provided by IDLDataResource.

        @return: A list of DataObject object(s).
        """
        self.debug("input resource: %s"%(resource), util.DEBUG_VERBOSE)
        
        if not isinstance(resource, IDLParser.IDLParser):
            self.debug("%s is not an instance of IDLParser.", util.DEBUG_ERROR)
            return None

        return self._generateDataObjects(resource)

    def _generateDataObjects(self, resource):
        """
        A delegate method for specific templates. It is the real work for 
        generating DataObjects.
        """
        self.debug("must be overrided by child.", util.DEBUG_ERROR)
        return []
