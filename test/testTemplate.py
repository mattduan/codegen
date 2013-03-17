"""
PyUnit TestCase for Template.
"""

import unittest
import sets
import StringIO,sys

# more imports
import codegen.Template as Template
import codegen.DataObject as DataObject

# test fixture
class TestTemplate(unittest.TestCase):
    
   def setUp(self):
       self.__temp=Template.Template()
       self.__data=DataObject.DataObject()
   def tearDown(self):
       self.__temp=None
       self.__data=None
       
   def test__init__(self):
       self.assertEquals(self.__temp.prefix,None)
       self.assertEquals(self.__temp.suffix,None)
        
   def testsetPrefix(self):
       self.assertRaises(AssertionError,self.__temp.setPrefix,' ')
       self.__temp.setPrefix(self.__temp)
       self.assertEquals(self.__temp.prefix,self.__temp)
       
       
   def testsetSuffix(self):
       self.assertRaises(AssertionError,self.__temp.setSuffix,' ')
       self.__temp.setSuffix(self.__temp)
       self.assertEquals(self.__temp.suffix,self.__temp)
       
   def test__padding(self):
       self.assertEquals(self.__temp._Template__padding(),'root.')
       tpl=Template.Template(suffix=self.__temp)
       self.assertEquals(self.__temp._Template__padding(),'root.suffix.')
       
   def testvalidate(self):
       str='[Template  ]try to validate data\n'
       str+='[Template  ] is not a DataObject.\n'
       stdout=sys.stdout
       sys.stdout=file=StringIO.StringIO()
       self.assertEquals(self.__temp.validate(''),0)
       sys.stdout=stdout
       self.assertEquals(file.getvalue(),str)
       self.__data.setNameVars({'root.z':'zxh'})
       self.__temp.keys=['z','x','h']
       self.assertEquals(self.__temp.validate(self.__data),1)
              
   def testoutput(self):
       self.assertRaises(AssertionError,self.__temp.output,'')
       self.assertEquals(self.__temp.output(self.__data),('','',''))
       
   def test_keys(self):
       self.__temp.keys=['z','x','h']
       self.assertEquals(self.__temp._keys(),['root.z','root.x','root.h'])
       
   def testbuild_keys(self):
       self.__temp.keys=['z','x','h']
       self.assertEquals(self.__temp.build_keys(),['root.z','root.x','root.h'])
       
   def test_instance_boundary(self):
       """Make sure the test covers every method in a Template instance."""
       tmpl = Template.Template(self.__temp)

       tested = sets.Set(['__module__', '__doc__', '__init__', 'setPrefix', 
                           'setSuffix',  'validate', 'output', '_keys','build_keys'])

       all_dir = tested | sets.Set(dir(tmpl))

       self.assertEquals(all_dir, sets.Set(dir(self.__temp)))
    
   def test_class_boundary(self):
       """Make sure the test covers every method in a Template instance."""
       base_set = sets.Set()
       for base in Template.Template.__bases__:
           base_set |= sets.Set(dir(base))  
           
       tested = sets.Set(['__module__', '__doc__', '__dict__', '__weakref__',
                           '__init__', '_Template__padding','setPrefix', 'setSuffix', 
                           'validate','output', '_keys', 'build_keys','suffix', 
                           'prefix','pre_string', 'post_string', 'parent', 
                           'template', 'keys', 'path_format', 'name_format', 'debug'])

       all_dir = tested | base_set

       self.assertEquals(all_dir, sets.Set(dir(Template.Template)))
             
       
             
if __name__=="__main__":
    unittest.main()
       
       

