#######################################################################
#
# Copyright (c) 2005 Guoqiang Duan. All Rights Reserved.
#
#######################################################################

"""
Template class is used to define a template for one output file.

$Id: Template.py 11 2005-12-24 09:13:33Z duan $
"""

__version__='$Revision: 11 $'[11:-2]
__author__ = "Duan Guoqiang (mattgduan@domainect.cn)"


import string

import DataObject
import util


class Template(object):
    """
    The base class for all templates.
    """
    
    parent       = None
    prefix       = None
    suffix       = None

    # expected to be specific
    template     = ""
    pre_string   = ""
    post_string  = ""
    keys         = []
    path_format  = "%(path)s"
    name_format  = "%(name)s"

    def __init__(self, prefix=None, suffix=None):
        self.setPrefix(prefix)
        self.setSuffix(suffix)
   
    def setPrefix(self, prefix):
        """
        Set the prefix template.
        """
        if not prefix: 
            self.prefix = None
            self.debug("set prefix to None", util.DEBUG_VERBOSE)
        else:
            assert issubclass(prefix.__class__, Template)
            prefix.parent = self
            self.prefix = prefix
            self.debug("relation created: %s --prefix-> %s"\
                       %(self.__class__.__name__, prefix.__class__.__name__),
                       util.DEBUG_VERBOSE)
    
    def setSuffix(self, suffix):
        """
        Set the suffix template.
        """
        if not suffix:
            self.suffix = None
            self.debug("set suffix to None", util.DEBUG_VERBOSE)
        else:
            assert issubclass(suffix.__class__, Template)
            suffix.parent = self
            self.suffix = suffix
            self.debug("relation created: %s --suffix-> %s"\
                       %(self.__class__.__name__, suffix.__class__.__name__),
                       util.DEBUG_VERBOSE)
        
    def validate(self, data):
        """
        Confirm the data match what defined in the template.

        @param data: A DataObject instance.

        @return: 1 - success; 0 - failure
        """
        if not self.parent:
            self.debug("try to validate data")

        # instance
        if not isinstance(data, DataObject.DataObject):
            self.debug("%s is not a DataObject."%(str(data)), util.DEBUG_ERROR)
            return 0
        
        if not self.parent:
            self.debug("\t%s" % (str(data)), util.DEBUG_VERBOSE)
        
        # values
        data_sets = data.DataSets(self.__padding())
        if data_sets == None:
            self.debug("DataSet is not in right format", util.DEBUG_ERROR)
            return 0
        
        # keys
        if data_sets != []:
            data_keys = data.keys()
            required_keys = self._keys()
            for k in required_keys:
                if k not in data_keys:
                    self.debug("%s is required, but not defined in %s"\
                               %(k, data.__class__.__name__), 
                               util.DEBUG_ERROR)
                    return 0
        
        # cascade validation to children
        if self.prefix:
            if not self.prefix.validate(data):
                return 0
        if self.suffix:
            if not self.suffix.validate(data):
                return 0
        
        if not self.parent:
            self.debug("validation succeed")
        
        return 1

    def output(self, data):
        """
        Return the formated filename and template.

        @param data: A DataObject instance.
        
        @return: A list (path, filename, content)
        """
        assert isinstance(data, DataObject.DataObject)
        
        self.debug("start output")
        
        path = self.path_format % (data.path_vars)
        filename  = self.name_format % (data.name_vars)
        contents = []
        data_sets = data.DataSets(self.__padding())
        for ds in data_sets:
            self.debug("get dataset %s."%(ds), util.DEBUG_VERBOSE)
            contents.append(self.template % ds)
        content = ''.join(contents)

        content = '%s%s%s' % (self.pre_string, content, self.post_string)

        pre  = self.prefix and self.prefix.output(data)[2] or ''
        post = self.suffix and self.suffix.output(data)[2] or ''

        content = pre + content + post
        
        if not self.parent:
            self.debug("generated filename '%s'"%(filename), util.DEBUG_VERBOSE)
            self.debug("generated content:\n%s%s%s"%("="*70, content, "="*70),
                       util.DEBUG_VERBOSE)

        self.debug("end output")

        return (path, filename, content)

    def __padding(self):
        """
        Return a list keys with dotted conversion.
        """
        paddings = []
        
        c = self
        p = c.parent
        while p:
            if p.prefix is c:
                self.debug("prefix added", util.DEBUG_VERBOSE)
                paddings.insert(0, "prefix")
            elif p.suffix is c:
                self.debug("suffix added", util.DEBUG_VERBOSE)
                paddings.insert(0, "suffix")
            else:
                self.debug("no prefix/suffix was found (child: %s, parent: %s)"\
                            %(c.__class__.__name__, p.__class__.__name__), 
                            util.DEBUG_NORMAL)
            c = p
            p = c.parent
        paddings.insert(0, "root")
        if paddings:
            paddings.append("")
        
        return string.join(paddings, ".")
    
    def _keys(self):
        """
        Return a list keys with dotted conversion.
        """
        padding = self.__padding()
        ckeys = []
        for k in self.keys:
            ckeys.append("%s%s"%(padding, k))
        return ckeys

    def build_keys(self):
        """
        Return all keys needed in the template.
        """
        p_keys = self.prefix and self.prefix.build_keys() or []
        s_keys = self.suffix and self.suffix.build_keys() or []
        return p_keys + self._keys() + s_keys
    
    debug = util.debug
