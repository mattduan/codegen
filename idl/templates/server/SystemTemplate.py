#
# Template for server side System class.
#

import Template


class SystemTemplate(Template.Template):
    """
    SystemTemplate defines template of System class.
    """

    template = """\
        # %(singleton_class)s
        %(singleton_var)s = %(singleton_module)s.%(singleton_class)s(self,
                        logger=self.logger)
        self.poa.bind_context(%(singleton_var)s)
        
"""
    keys = ['singleton_module', 'singleton_class', 'singleton_var']
    name_format = "%(name)s.py"

    def __init__(self):
        Template.Template.__init__(self,
                                   prefix = StartSystemTemplate(),
                                   suffix = EndSystemTemplate())

class StartSystemTemplate(Template.Template):
    
    template = """\
class _%(name)s(BaseSystem.BaseSystem):

    def __init__(self, server):
        BaseSystem.BaseSystem.__init__(self, 
                                       '%(uid)s',
                                       '',
                                       server)

    def Signature(self, username, password,
                        factory_xlass=%(name)sSignatureFactory):
        """'"""'"""
        Override parent.
        """'"""'"""
        return BaseSystem.BaseSystem.Signature(self, username, password,
                        factory_xlass=factory_xlass)

    def activate(self, servant):
        """'"""'"""
        Bind objects to corresponding context.
        """'"""'"""
        # Bind itself
        self.poa.bind_context(servant)

"""
    keys = ['name', 'uid']

    def __init__(self):
        Template.Template.__init__(self,
                                   prefix = SignatureFactoryTemplate())


class EndSignatureFactoryTemplate(Template.Template):
    
    template = """'%(api)s',
                """
    keys = ['api']
    pre_string = """\
    def get_acl(self, username, password):
        return ["""
    post_string = """]


"""
    

class SignatureFactoryTemplate(Template.Template):

    template = """\
# %(name)s ACL implementation
class %(name)sSignatureFactory(Signature.SignatureFactory):

"""
    keys = ['name']

    def __init__(self):
        Template.Template.__init__(self,
                                   prefix = ImportsTemplate(),
                                   suffix = EndSignatureFactoryTemplate())


class ImportsTemplate(Template.Template):

    template = """\
%(stub_import)s
"""
    keys = ['stub_import']
    pre_string = """\

import BaseSystem
import SystemObject
import Signature

# stubs
"""
    post_string = "\n"


    def __init__(self):
        Template.Template.__init__(self,
                                   suffix = HBLImportsTemplate() )


class HBLImportsTemplate(Template.Template):

    template = """\
%(hbl_proxy_import)s
"""
    keys = ['hbl_proxy_import']
    pre_string = """\
# hbl proxies
"""
    post_string = "\n"


class EndSystemTemplate(Template.Template):
    
    template = """\
    def deactivate(self):
        pass


class %(name)s(%(parent_stub_class)s):

    def __init__(self, server):
        self._object = _%(name)s(server)

    def authorize(self, username, password):
        return self._object.authorize(username, password)

    def startup(self):
        self._object.activate(self)

    def reload(self):
        self._object.deactivate()
        self._object.activate(self)

    def cleanup(self):
        self._object.deactivate()

    def __del__(self):
        self._object.__del__()
        self = None

"""
    keys = ['name', 'parent_stub_class']

