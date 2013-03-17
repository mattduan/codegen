#######################################################################
#
# Copyright (c) 2005 Guoqiang Duan. All Rights Reserved.
#
#######################################################################

"""
Generator is the controller class to generate code.

$Id: Generator.py 1709 2007-05-06 17:01:46Z duan $
""" 

__version__='$Revision: 1709 $'[11:-2]
__author__ = "Duan Guoqiang (mattgduan@gmail.com)"


import os
import util

import GeneratorConf


class Generator:
    
    def __init__(self):
        pass

    def process(self):
        assert hasattr(GeneratorConf, "TASKS")
        self.debug("####### PROCESS START #######")
        for task in GeneratorConf.TASKS:
            self.debug("==== start one task for '%s' ====" \
                            % (task.get("NAME", "--")))
            tpx = util.load_class(task["TEMPLATE"][0],
                                 task["TEMPLATE"][1])
            drx = util.load_class(task["DATA_RESOURCE"][0],
                                 task["DATA_RESOURCE"][1])
            dpx = util.load_class(task["DATA_PROVIDER"][0],
                                 task["DATA_PROVIDER"][1])
            hdx = util.load_class(task["HANDLER"][0], task["HANDLER"][1])
            
            resources = []
            for rdict in task["RESOURCES"]:
                resources.append(drx(rdict))

            provider = dpx(resources)
            template = tpx()
            handler  = hdx()
            
            do_list = provider.provide()
            for do in do_list:
                if not template.validate(do):
                    continue
                path, filename, content = template.output(do)
                out_path = task.get("SAVE_PATH", 'out')
                path = os.path.join(out_path, path)
                h_config = { 'filename'    : filename,
                             'content'     : content,
                             'path'        : path,
                             'data_object' : do }
                handler.handle(content, h_config)
            
            self.debug("==== finish one task for '%s' ====" \
                            % (task.get("NAME", "--")))
    
        self.debug("####### PROCESS END #######")
        
    debug = util.debug
