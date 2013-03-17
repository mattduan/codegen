"""
PyUnit TestCase for Handler.
"""

import unittest
import StringIO,sys

# more imports
import codegen.Handler as Handler


# test fixture
class TestHandler(unittest.TestCase):
    
   def setUp(self):
       self.__bh=Handler.BaseHandler()
       self.__sh=Handler.SimpleHandler()
   def tearDown(self):
       self.__bh=None
       self.__sh=None
   
   def test__init__(self):
       self.assert_(issubclass(self.__bh.__class__,object))
       
   def testBasehandle(self):
       stdout=sys.stdout
       sys.stdout=file=StringIO.StringIO()
       self.__bh.handle('')
       sys.stdout=stdout
       self.assertEquals("[BaseHandler]try to handle data with config: {}\n",
                          file.getvalue())
       
       
   def testSimpleHandler_handle(self):
       self.assert_(issubclass(Handler.SimpleHandler,Handler.BaseHandler))
   
   def testSimpleHandle(self):
       stdout=sys.stdout
       sys.stdout=file=StringIO.StringIO()
       self.__sh.handle('zxh',{'path':'/home/zxh','filename':'domain'})
       sys.stdout=stdout
       self.assertEquals(file.getvalue(),"/home/zxh/domain\nzxh\n")
      
       
if __name__=="__main__":
    unittest.main()
       
       


