"""
PyUnit TestCase for util.
"""

import unittest
import StringIO,sys

# more imports
import codegen.util as util

# test fixture
class Testutil(unittest.TestCase):
    
   def setUp(self):
       pass
   def tearDown(self):
       pass
   def testdebug(self):
       t=[]
       stdout=sys.stdout
       sys.stdout=file=StringIO.StringIO()
       util.debug("debug test1")
       util.debug("debug test2",1)
       util.debug(t,"debug test3")
       sys.stdout=stdout
       self.assertEquals(file.getvalue(),
                          'debug test1\ndebug test2\n[list      ]debug test3\n')
      
       
   def testload_class(self):
       self.assertEquals(unittest.TestCase,util.load_class("unittest", "TestCase"))
       
if __name__=="__main__":
    unittest.main()
       
       


