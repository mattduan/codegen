#
# DataProvider for SystemTemplate.
#

import os.path

import util

import DataObject
import idl.IDLDataProvider as IDLDataProvider


class SystemDataProvider(IDLDataProvider.IDLDataProvider):
    """
    SystemDataProvider provides DataObject containing server-side 
    System info.
    """

    def __init__(self, resources):
        IDLDataProvider.IDLDataProvider.__init__(self, resources)

    def _generateDataObjects(self, resource):
        """
        Generate and add vars to data_object.  Overrides parent.

        @param resource: A resource provided by IDLDataResource.

        @return: A list of DataObject objects.
        """
        do_list = []
        systems = resource.getSystems()
        for system in systems:
            do = DataObject.DataObject()

            # add vars
            do['root.prefix.prefix.name'] = system['name']
            do['root.prefix.name']        = system['name']
            do['root.suffix.name']        = system['name']
            do['root.prefix.uid']         = system['uid']
            do['root.suffix.parent_stub_class'] = system['stub']
            
            stub_imports = system.get('stub_imports', [])
            for si in stub_imports:
                do['root.prefix.prefix.prefix.stub_import'] = si
            proxy_imports = system.get('proxy_imports', [])
            for pi in proxy_imports:
                do['root.prefix.prefix.prefix.suffix.hbl_proxy_import'] = pi
            apis = system.get('api', [])
            for api in apis:
                do['root.prefix.prefix.suffix.api'] = api
            singletons = system.get('factory', [])
            for s in singletons:
                mod, cls = s[0], s[1]
                var = cls.lower()
                do['root.singleton_module'] = mod
                do['root.singleton_class']  = cls
                do['root.singleton_var']    = var
            
            # path/name
            #path = os.path.join(system['namespace'].split('.'))
            path = system['namespace'].replace('.', '/')
            do.path_vars = {'path' : path}
            do.name_vars = {'name' : system['name']}

            self.debug("add DataObject: %s"%(do), util.DEBUG_VERBOSE)
            do_list.append(do)
        
        return do_list
