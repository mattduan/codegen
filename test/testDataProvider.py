"""
PyUnit TestCase for DataProvider.
"""

import unittest
import StringIO, sys
import sets
# more imports
import codegen.DataProvider as DataProvider
import codegen.DataResource as DataResource


# test fixture
class TestDataProvider(unittest.TestCase):   
    
   def setUp(self):
       self.__dr=DataResource.DataResource({})
       self.__data=DataProvider.DataProvider(self.__dr)
   def tearDown(self):
       self.__data=None
       self.__dr=None
   
   def test__init__(self):
       self.assert_(issubclass(self.__data.__class__,object))
       self.assertEquals(self.__data._DataProvider__resources,[self.__dr])
       
   def testgetResources(self):
       self.assertEquals(self.__data._DataProvider__resources,self.__data.getResources())
       
   def testaddResources(self):
       tmp=DataResource.DataResource({'zxh':''})
       self.__data.addResources(tmp)
       self.assert_(tmp in self.__data._DataProvider__resources)
   
   def testsetResources(self):
       self.__data.setResources('zxh')
       self.assertEquals(self.__data._DataProvider__resources,'zxh')
   
   def testprovide(self):
       self.assertEquals([],self.__data.provide())
       
   def testgenerateDataObjects(self):
       stdout=sys.stdout
       sys.stdout=file=StringIO.StringIO()
       self.assertEquals([],self.__data.generateDataObjects(['']))
       sys.stdout=stdout 
       self.assertEquals("[DataProvider]DataProvider.DataObject has to be overrided "
                   "and implemented by child!\n",file.getvalue())     
       
   def test_instance_boundary(self):
       """Make sure the test covers every method in a DataProvider instance."""
       tmp=DataResource.DataResource({'zxh':''})
       tmpl = DataProvider.DataProvider(tmp)

       tested = sets.Set(['__module__', '__doc__', '__init__', 'getResources', 
                          'addResources', 'setResources',  'provide',  'generateDataObjects'])

       all_dir = tested | sets.Set(dir(tmpl))

       self.assertEquals(all_dir, sets.Set(dir(self.__data)))
    
   def test_class_boundary(self):
       """Make sure the test covers every method in a DataProvider class."""
       base_set = sets.Set()
       for base in DataProvider.DataProvider.__bases__:
           base_set |= sets.Set(dir(base))  
           
       tested = sets.Set(['__module__', '__doc__',   '__dict__', '__weakref__',
                           '__init__', 'getResources', 'addResources', 'setResources',
                            'provide', 'generateDataObjects', 'debug'])
                          
       all_dir = tested | base_set

       self.assertEquals(all_dir, sets.Set(dir(DataProvider.DataProvider)))
       
if __name__=="__main__":
    unittest.main()
       
       


