
import sys

import util
import DataResource
import IDLParser

from hwmodules.util.Trace import traceBack


class IDLDataResource(DataResource.DataResource):
    """
    IDL DataResource class is a factory class which generates IDLParser
    from a config dict.
    """

    def __init__(self, config):
        DataResource.DataResource.__init__(self, config)

    def resource(self):
        """
        Factory method to generate an IDLParser object.
        
        @return: An IDLParser object.
        """
        if type(self.config) != type({}) or \
                not self.config.has_key("idl"):
            self.debug("incorrect data resource: %s" % (self.config),
                       util.DEBUG_ERROR)
            return None

        self.debug( "trying to parse idl '%s'" %(self.config["idl"]),
                    util.DEBUG_VERBOSE )
        
        ip = IDLParser.IDLParser(self.config["idl"])

        try:
            ip.parse()
        except:
            self.debug("exception while parsing idl. %s" % (traceBack()),
                       util.DEBUG_ERROR)
            return None

        self.debug( "idl was parsed successfully", util.DEBUG_VERBOSE )

        return ip

    debug = util.debug

