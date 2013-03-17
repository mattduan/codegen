"""
PyUnit TestCase for Generator.
"""

import unittest
import sets
import StringIO,sys

# more imports
import deep.modules.code_generator.Generator as Generator


# test fixture
class TestGenerator(unittest.TestCase):
    
   def setUp(self):
       self.__gen=Generator.Generator()
   def tearDown(self):
       self.__gen=None
       
   def testprocess(self):
       str="[Generator ]####### PROCESS START #######\n"
       str+="[Generator ]==== start one task for 'Test' ====\n"
       str+="[Generator ]==== finish one task for 'Test' ====\n"
       str+="[Generator ]####### PROCESS END #######\n"
       stdout=sys.stdout
       sys.stdout=file=StringIO.StringIO()
       self.__gen.process()
       sys.stdout=stdout
       self.assertEquals(file.getvalue(),str)
    
   def test_class_boundary(self):
       """Make sure the test covers every method in a Generator class."""
       base_set = sets.Set()
       for base in Generator.Generator.__bases__:
           base_set |= sets.Set(dir(base)) 
           
       tested = sets.Set(['__module__', '__doc__', '__init__', 'process', 'debug'])
                          
       all_dir = tested | base_set

       self.assertEquals(all_dir, sets.Set(dir(Generator.Generator))) 

       
if __name__=="__main__":
    unittest.main()
       
       


