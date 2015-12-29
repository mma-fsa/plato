'''
Created on Dec 22, 2015

@author: mike
'''
import unittest
from plato.core.model import Model
from plato_tests.test_utils.model_setup_utility import ModelSetupUtility
from plato.core.decorator.column import column
from plato.util.column_identifier_util import ColumnIdentifierUtil


class Test(unittest.TestCase):


    def testSingleModelGetColumnId(self):
        
        m = ModelSetupUtility.setup_test_model(TestModel, 'test_model_1')
        util = ColumnIdentifierUtil(m)
        col_id = util.get_column_identifier(m.some_test_col)
        
        self.assertEqual(col_id, 'test_model_1#some_test_col')
    
    def testNestedModelGetColumnId(self):
        
        parent_model = ModelSetupUtility.setup_test_model(TestModel, \
                                                          'parent_model')
        
        child_model = ModelSetupUtility.setup_test_model(TestModel, \
            'child_model', parent_model=parent_model)
        
        util = ColumnIdentifierUtil(child_model)
        col_id = util.get_column_identifier(child_model.some_test_col)
        
        self.assertEqual(col_id, 'parent_model.child_model#some_test_col')

class TestModel(Model):
    
    @column
    def some_test_col(self, t):
        pass

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testGetColumnId']
    unittest.main()