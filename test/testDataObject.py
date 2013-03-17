"""
PyUnit TestCase for DataObject.
"""

import unittest
import sets

# more imports
import codegen.DataObject as DataObject


# test fixture
class TestDataObject(unittest.TestCase):
    
   def setUp(self):
       self.__data=DataObject.DataObject()
   def tearDown(self):
       self.__data=None
   
   def test__init__(self):
       self.assert_(issubclass(self.__data.__class__,dict))
       self.assertEquals(self.__data._DataObject__name_vars,{'name':''})
       self.assertEquals(self.__data._DataObject__path_vars,{'path':''})
       
   def testgetNameVars(self):
       self.assertEquals(self.__data._DataObject__name_vars,self.__data.getNameVars())
       
   def testsetNameVars(self):
       self.assertRaises(AssertionError,self.__data.setNameVars,"zxh")
       self.__data.setNameVars({'zxh':''})
       self.assertEquals(self.__data._DataObject__name_vars,{'zxh':''})
 
   def testgetPathVars(self):
       self.assertEquals(self.__data._DataObject__path_vars,self.__data.getPathVars())
       
   def testsetPathVars(self):
       self.assertRaises(AssertionError,self.__data.setPathVars,"zxh")
       self.__data.setPathVars({'zxh':''})
       self.assertEquals(self.__data._DataObject__path_vars,{'zxh':''})
       
   def test__setitem__(self):
       self.__data.__setitem__('zxh','tt')
       self.assertEquals(['tt'],self.__data['zxh'])
       
   def testDataSets(self):
       self.assertEquals(self.__data.DataSets('zxh'),[])
       self.__data.__setitem__('zxh',['tt','ss'])
       self.assertEquals(self.__data.DataSets('z'),[{'xh':'tt'},{'xh':'ss'}])
       
   def test_instance_boundary(self):
       """Make sure the test covers every method in a DataObject instance."""
       tmpl = DataObject.DataObject()

       tested = sets.Set(['__module__', '__doc__', '__init__', '__setitem__','getNameVars', 
                          'setNameVars', 'getPathVars',  'setPathVars',  'DataSets'])

       all_dir = tested | sets.Set(dir(tmpl))

       self.assertEquals(all_dir, sets.Set(dir(self.__data)))
    
   def test_class_boundary(self):
       """Make sure the test covers every method in a DataObject class."""
       base_set = sets.Set()
       for base in DataObject.DataObject.__bases__:
           base_set |= sets.Set(dir(base))  
           
       tested = sets.Set(['__module__', '__doc__', '__dict__',  '__weakref__', 
                          '__init__', '__setitem__', 'getNameVars', 'setNameVars', 
                          'getPathVars', 'setPathVars', 'DataSets', 'path_vars', 
                          'name_vars', 'debug'])
                          
       all_dir = tested | base_set

       self.assertEquals(all_dir, sets.Set(dir(DataObject.DataObject)))
       
if __name__=="__main__":
    unittest.main()
       
       


