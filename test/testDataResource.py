"""
PyUnit TestCase for DataResource.
"""

import unittest
import sets
# more imports
import deep.modules.code_generator.DataResource as DataResource


# test fixture
class TestDataResource(unittest.TestCase):
    
   def setUp(self):
       self.__data=DataResource.DataResource({})
   def tearDown(self):
       self.__data=None
       
   def test__init__(self):
       self.assertEquals({},self.__data.config)
   
   def testresource(self):
       self.assertEquals({},self.__data.resource())
       
   def test_instance_boundary(self):
       """Make sure the test covers every method in a DataResource instance."""
       tmpl = DataResource.DataResource(['zxh'])

       tested = sets.Set(['__module__', '__doc__', '__init__', 'resource'])

       all_dir = tested | sets.Set(dir(tmpl))

       self.assertEquals(all_dir, sets.Set(dir(self.__data)))
    
   def test_class_boundary(self):
       """Make sure the test covers every method in a DataResource class."""
       base_set = sets.Set()
       for base in DataResource.DataResource.__bases__:
           base_set |= sets.Set(dir(base))  
           
       tested = sets.Set(['__module__', '__doc__','__dict__', '__weakref__', 
                          '__init__', 'resource'])
                          
       all_dir = tested | base_set

       self.assertEquals(all_dir, sets.Set(dir(DataResource.DataResource)))
       
if __name__=="__main__":
    unittest.main()
       
       
