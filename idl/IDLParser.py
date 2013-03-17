#
# IDLParser is used to parse an idl file and keep the parsed 
# information.
#

import re
import os, os.path
import copy

import util


ON_PUSH = "(?s)([a-z]+)\s+(\w+)\s*{(.*)$"
ON_POP  = "(?s)([^{}]*?)}\s*;(.*)$"
ON_TYPE = "(?s)typedef\s+(.*?);(.*)$"
ON_VAR  = "(?s)(\w+)\s+(\w+)\s*;(.*)$"
ON_ATTR = "(?s)attribute\s+(\w+)\s+(\w+)\s*;(.*)$"
ON_FUNC = "(?s)(\w+)\s+(\w+)\s*\(([^)]*?)\)[^;]*?;(.*)$"

ON_SKIPS = ["(?s)//.*?\n(.*)$", "(?s)/\*.*?\*/(.*)$",
            "(?s)interface\s+\w+\s*;(.*)$",]

class IDLParser(object):

    def __init__(self, idl):
        if os.path.isfile(idl):
            self.__idl = open(idl).read()
        else:
            self.__idl = idl
        self.__stack = []
        self.__data  = {}

    def parse(self, s=None):
        if s == None:
            s = self.__idl
            self.debug("start parsing idl", util.DEBUG_VERBOSE)
        
        s = s.lstrip()

        #self.debug("processing string: %s"%(s))

        for skip in ON_SKIPS:
            m = re.match(skip, s)
            if m:
                self.parse(m.group(1))
                return

        m = re.match(ON_PUSH, s)
        if m:
            self.__push(m.group(1), m.group(2))
            self.parse(m.group(3))
            return

        m = re.match(ON_TYPE, s)
        if m:
            self.__processTypeDef(m.group(1))
            self.parse(m.group(2))
            return

        m = re.match(ON_ATTR, s)
        if m:
            self.__processAttr(m.group(1), m.group(2))
            self.parse(m.group(3))
            return

        m = re.match(ON_FUNC, s)
        if m:
            self.__processFunc(m.group(1), m.group(2), m.group(3))
            self.parse(m.group(4))
            return
        
        m = re.match(ON_VAR, s)
        if m:
            self.__processVar(m.group(1), m.group(2))
            self.parse(m.group(3))
            return

        m = re.match(ON_POP, s)
        if m:
            self.__pop(m.group(1))
            self.parse(m.group(2))
            return

        s = s.strip()
        if s != '':
            raise Exception("parse error: %s was not parsed!"%(s))

        if self.__stack:
            raise Exception("parse error: systax error, stack not empty: %s."%\
                            (self.__stack))

        self.debug("finish parsing idl", util.DEBUG_VERBOSE)


    ######################################################################
    # Internal methods used by parse.
    ######################################################################
    def __current(self):
        stack = copy.copy(self.__stack)
        cur = self.__data
        for item in stack:
            w, n = item.split(':')
            if not cur.has_key(w):
                cur[w] = {}
            cur = cur[w]
            if not cur.has_key(n):
                if w in ('struct', 'exception'):
                    cur[n] = []
                else:
                    cur[n] = {}
            cur = cur[n]

        self.debug("current stack: %s"%(self.__stack), util.DEBUG_VERBOSE)
        #self.debug("current data: %s"%(cur))
        return cur

    def __push(self, what, name):
        dict = self.__current()

        self.debug("current dict on push: %s"%(dict), util.DEBUG_VERBOSE)

        if not dict.has_key(what):
            dict[what] = {}

        dict = dict[what]
        if not dict.has_key(name):
            if what in ('struct', 'exception'):
                dict[name] = []
            else:
                dict[name] = {}
        
        self.debug("stack before push change: %s"%(self.__stack), util.DEBUG_VERBOSE)
        
        self.__stack.append("%s:%s"%(what, name))

    def __pop(self, content):
        content = content.strip()
        if content != '':
            self.debug("%s cannot be parsed!"%(content), util.DEBUG_ERROR)
        
        self.debug("stack before pop change: %s"%(self.__stack), util.DEBUG_VERBOSE)
        
        return self.__stack.pop()

    def __processTypeDef(self, typedef):
        dict = self.__current()
        name = typedef.split(" ")[-1]
        if not dict.has_key("typedef"):
            dict["typedef"] = []
        dict["typedef"].append(name)

    def __processAttr(self, what, name):
        dict = self.__current()
        if not dict.has_key("attribute"):
            dict["attribute"] = []
        dict["attribute"].append( {'type' : what,
                                   'name' : name} )
    
    def __processFunc(self, what, name, args):
        dict = self.__current()
        if not dict.has_key("function"):
            dict["function"] = []
        args = args.split(",")
        arg_list = []
        for arg in args:
            arg = arg.strip()
            if arg == '':
                continue
            m = re.match("(?:in|out)\s+(\w+)\s+(\w+)$", arg)
            if m:
                arg_list.append({'type' : m.group(1),
                                 'name' : m.group(2)})
            else:
                self.debug("arg %s was not parsed!"%(arg), util.DEBUG_ERROR)
        
        dict["function"].append( {'ret_type' : what,
                                  'name'     : name,
                                  'args'     : arg_list } )

    def __processVar(self, what, name):
        list = self.__current()
        list.append({'type':what,'name':name})


    ######################################################################
    # Prepare data for use with system class generation.
    ######################################################################
    def getSystems(self):
        return self.__prepareSystems(self.__data)

    def __prepareSystems(self, module_dict, namespace=''):
        sys_list = []
        if type(module_dict) == type({}):
            for k, v in module_dict.items():
                if k == 'module':
                    for m, b in module_dict[k].items():
                        sys_list += self.__prepareSystems(b,
                                namespace and "%s.%s"%(namespace, m) or m)

                elif k == 'interface':
                    for i, b in module_dict[k].items():
                        for f in v[i]['function']:
                            if f['name'] == 'authorize':
                                system_dict = {}
                                p = namespace.find('.')
                                ns_poa = namespace[:p] + '__POA' + namespace[p:]
                                system_dict['namespace']     = namespace
                                system_dict['name']          = i[2:]
                                system_dict['stub_imports']  = [ 'import ' + namespace,
                                                                 'import ' + ns_poa ]
                                system_dict['stub']          = ns_poa + '.' + i
                                system_dict['uid']           = namespace[len('core.'):] + '.' + i[2:]
                                system_dict['api']           = self.__getAPIList(v, namespace)
                                system_dict['factory'], system_dict['proxy_imports'] = \
                                        self.__getFactoryAndProxyList(v, namespace)
                                return [ system_dict ]

        return sys_list

    def __getAPIList(self, d, ns):
        api_list = []
        ns = ns[len('core.'):]
        for k, v in d.items():
            for f in d[k]['function']:
                if f['name'] == 'authorize':
                    break
            else:
                for f in d[k]['function']:
                    api_list.append( ns + '.' + k[2:] + '.' + f['name'] )
        return api_list

    def __getFactoryAndProxyList(self, d, ns):
        factory_list = []
        proxy_list   = []
        for k, v in d.items():
            for x in ('ListFactory', 'Factory', 'Constants'):
                if k[ -len(x) : ] == x:
                    factory_list.append( ( k[2:-len(x)], k[2:] ) )
                    if x == 'Constants':
                        p = None
                    else:
                        p = -len(x)
                    proxy_list.append( 'import systems' + ns[ len('core'): ] + '.' + k[2:p] 
                            + ' as ' + k[2:p]  )
                    break
        return factory_list, proxy_list

    def __str__(self):
        return self.__format_data(self.__data)

    def __format_data(self, d, level=0, indent=4):
        s = ''
        pad = ' '*indent*level
        
        if type(d) == type({}):
            s += "{" + "\n"
            for k, v in d.items():
                if type(v) in (type({}), type([])):
                    v = self.__format_data(v, level+1)
                else:
                    v = str(v)
                s += pad + "'%s' : %s\n" % (k, v)
            s += pad + "}" + "\n"
        elif type(d) == type([]):
            s += "[" + "\n"
            for v in d:
                if type(v) in (type({}), type([])):
                    v = self.__format_data(v, level+1)
                else:
                    v = str(v)
                s += pad + v + "\n"
            s += pad + "]" + "\n"
        else:
            s += pad + str(d) + "\n"
        
        return s

    debug = util.debug
