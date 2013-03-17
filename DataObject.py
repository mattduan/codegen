#######################################################################
#
# Copyright (c) 2005 Guoqiang Duan. All Rights Reserved.
#
#######################################################################

"""
DataObject is just a dictionary with only a name attribute and rooms 
for other hooks.

$Id: DataObject.py 11 2005-12-24 09:13:33Z duan $
"""

__version__='$Revision: 11 $'[11:-2]
__author__ = "Duan Guoqiang (mattgduan@gmail.com)"


import util

class DataObject(dict):
    """
    DataObject is_a dict.
    """
    
    def __init__(self):
        dict.__init__(self)
        self.__name_vars = {'name':''}
        self.__path_vars = {'path':''}

    def getNameVars(self):
        return self.__name_vars
    
    def setNameVars(self, vars):
        assert type(vars) == type({})
        self.__name_vars = vars

    name_vars = property(getNameVars, setNameVars)

    def getPathVars(self):
        return self.__path_vars

    def setPathVars(self, vars):
        assert type(vars) == type({})
        self.__path_vars = vars

    path_vars = property(getPathVars, setPathVars)

    def __setitem__(self, key, value):
        """
        All items in a DataObject are lists.
        """
        if type(value) in (type([]), type(())):
            dict.__setitem__(self, key, value)
        elif dict.has_key(self, key):
            v = dict.get(self, key, [])
            if v:
                v.append(value)
            else:
                dict.__setitem__(self, key, [value])
        else:
            dict.__setitem__(self, key, [value])
    
    def DataSets(self, padding):
        """
        A set of data dict filtered by specified padding.

        @return: A list of dicts.
        """
        length    = 0
        data_sets = []
        for k in self.keys():
            if k.startswith(padding) and \
                                k[len(padding):].find(".")==-1:
                key = k.replace(padding, "")
                v_list = self[k]
                if not length:
                    length = len(self[k])
                if length != len(self[k]):
                    self.debug("Wrong size in DataObject for padding "
                               "'%s' when creating DataSet"%(padding),
                               util.DEBUG_ERROR)
                    return None
                for i in range(length):
                    if len(data_sets) != length:
                        data_sets.append({})
                    data_sets[i][key] = v_list[i]
        
        return data_sets
        
    debug = util.debug 
