'''
Created on Dec 20, 2015

@author: mike
'''
import unittest

from plato_tests.test_utils.model_setup_utility import ModelSetupUtility
from plato.core.model import Model
from plato.core.decorator.column import column

class ModelColumnsTest(unittest.TestCase):

    def testEmptyModelConstruction(self):
        model = ModelSetupUtility.setup_test_model(EmptyModel)
        self.assertTrue(model)
        
    def testColumnModel(self):
        
        svc_loc_setup = ModelSetupUtility.setup_service_locator()
        svc_loc = svc_loc_setup['service_locator']
        storage = svc_loc_setup['storage']
        model = ModelSetupUtility.setup_test_model(ColumnModel, \
            service_locator=svc_loc)
        
        self.assertTrue(model)
        self.assertTrue(len(storage.keys()) == 2)
        self.assertIn('test_model#timestep_column', storage)
        self.assertIn('test_model#two_dimensional_column', storage)

class EmptyModel(Model):
    pass

class ColumnModel(Model):
    
    property = 'foo'
    
    @column
    def timestep_column(self, t):
        return 10 * t
    
    @column
    def two_dimensional_column(self, x, y):
        return x + 100 * y
    
    def member_function(self, t):
        return 100.0
    
    @staticmethod
    def static_function(self, x, y):
        return 2 * x + y


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()