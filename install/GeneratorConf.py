"""
GeneratorConf
=============

This file defines the configurations to setup and run the Generator.

It contains a list of tasks needed to be done by the Generator. Each
task specification is specified by a list of variables in a dictionary.
Each dictionary has these configuration variables:

    "TEMPLATE"      - the specific Template class used.
    "DATA_PROVIDER" - the specific DataProvider class used.
    "DATA_RESOURCE" - the specific DataResource class used.
    "HANDLER"       - the specific Handler class used.
    * all above variables are tuples with module and class names

    "RESOURCES"     - a list of dicts each of which is used to init a
                      DataResource instance.
    "SAVE_PATH"     - where to save the generated codes.
"""

TASKS = [
  {
    "NAME"          : "Test",
    
    "TEMPLATE"      : ("Template", "Template"),
    "DATA_PROVIDER" : ("DataProvider", "DataProvider"),
    "DATA_RESOURCE" : ("DataResource", "DataResource"),
    "HANDLER"       : ("Handler", "BaseHandler"),

    "RESOURCES"     : [],
    "SAVE_PATH"     : "out",
  },

]
