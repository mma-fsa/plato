'''
Created on Dec 20, 2015

@author: mike
'''
import unittest

from plato_tests.test_utils.model_setup_utility import ModelSetupUtility
from plato.core.model import Model
from plato.core.decorator.column import column
from _collections import defaultdict

class ModelColumnsTest(unittest.TestCase):

    def testEmptyModelConstruction(self):
        model = ModelSetupUtility.setup_test_model(EmptyModel)
        self.assertTrue(model)
         
    def testModelColumnCalls(self):                
        svc_loc_setup = ModelSetupUtility.setup_service_locator()
        svc_loc = svc_loc_setup['service_locator']
        storage = svc_loc_setup['storage']
        model = ModelSetupUtility.setup_test_model(ColumnModel, \
            service_locator=svc_loc)
         
        # Check that storage was allocated correctly
        self.assertTrue(model)
        self.assertTrue(len(storage.keys()) == 2)
        self.assertIn('test_model#timestep_column', storage)
        self.assertIn('test_model#two_dimensional_column', storage)
         
        self.assertEqual(model.timestep_column_calls, 0)
        self.assertEqual(model.two_dimensional_column_calls, 0)
         
        # Check that columns are called only once for each argument
        self.assertEqual(model.two_dimensional_column(2, 3), 302)
        self.assertEqual(model.two_dimensional_column(2, 3), 302)
        self.assertEqual(model.two_dimensional_column(2, 3), 302)
         
        self.assertEqual(model.timestep_column_calls, 0)
        self.assertEqual(model.two_dimensional_column_calls, 1)
        self.assertEqual(storage['test_model#timestep_column'], {})
        self.assertEqual(storage['test_model#two_dimensional_column'], \
                        {(2,3) : 302})
         
        # Check that additional calls work correctly
        self.assertEqual(model.two_dimensional_column(3, 3), 303)
        self.assertEqual(model.two_dimensional_column(2, 4), 402)
        self.assertEqual(model.two_dimensional_column(2, 3), 302)
         
        self.assertEqual(model.timestep_column_calls, 0)
        self.assertEqual(model.two_dimensional_column_calls, 3)
        self.assertEqual(storage['test_model#timestep_column'], {})        
        self.assertEqual(storage['test_model#two_dimensional_column'], \
                        {(2,3) : 302, (3,3):303, (2,4): 402})

        
        def testMultipleModels(self):
             
            svc_loc_setup = ModelSetupUtility.setup_service_locator()
            svc_loc = svc_loc_setup['service_locator']
            storage = svc_loc_setup['storage']
             
            model1 = ModelSetupUtility.setup_test_model(DataAndColumnModel,
                                                       service_locator=svc_loc,
                                                       identifier='model1')
             
            # Check that storage as allocated correctly for model 1
            model1.base_val = 10
            self.assertTrue(len(storage.keys()) == 2)
            self.assertIn('model1#timestep_column', storage)
            self.assertIn('model1#two_dimensional_column', storage)
            self.assertEqual(storage['model1#timestep_column'], {})
            self.assertEqual(storage['model1#two_dimensional_column'], {})
             
            model2 = ModelSetupUtility.setup_test_model(DataAndColumnModel,
                                                       service_locator=svc_loc,
                                                       identifier='model2')            
             
            # Check that storage has been allocated for model 2 and that
            # model 1's storage is still intact
            model2.base_val = 20
            self.assertTrue(len(storage.keys()) == 4)
            self.assertIn('model1#timestep_column', storage)
            self.assertIn('model1#two_dimensional_column', storage)
            self.assertIn('model2#timestep_column', storage)
            self.assertIn('model2#two_dimensional_column', storage)
             
            for i in xrange(1, 3):
                model1.timestep_column(i)
             
            model3 = ModelSetupUtility.setup_test_model(DataAndColumnModel,
                                                       service_locator=svc_loc,
                                                       identifier='model3')
            model3.base_val = 30
             
            # Check that storage has been allocated for model 3 and that
            # model 1 and 2's storage is still intact
            model2.base_val = 20
            self.assertTrue(len(storage.keys()) == 6)
            self.assertIn('model1#timestep_column', storage)
            self.assertIn('model1#two_dimensional_column', storage)
            self.assertIn('model2#timestep_column', storage)
            self.assertIn('model2#two_dimensional_column', storage)
            self.assertIn('model3#timestep_column', storage)
            self.assertIn('model3#two_dimensional_column', storage)
             
            for i in xrange(1, 5):
                model2.timestep_column(i)
                model1.timestep_column(i)
             
            for i in xrange(1, 5):
                model3.timestep_column(i)
            

class EmptyModel(Model):
    pass

class ColumnModel(Model):
    
    timestep_column_calls = 0
    two_dimensional_column_calls = 0
    
    property = 'foo'
    
    @column
    def timestep_column(self, t):
        return 10 * t
    
    @column
    def two_dimensional_column(self, x, y):
        self.two_dimensional_column_calls += 1
        return x + 100 * y
    
    def member_function(self, t):
        self.timestep_column_calls += 1
        return 100.0
    
    @staticmethod
    def static_function(self, x, y):
        return 2 * x + y


class DataAndColumnModel(ColumnModel):
    
    def __init__(self, *args, **kwargs):
        self.__base_val = 0
        super(ColumnModel, self).__init__(*args, **kwargs)
        
    @property
    def base_val(self):
        return self.__base_val
    
    @base_val.setter
    def base_val(self, value):
        self.__base_val = value
        
    @column
    def timestep_column(self, t):
        return self.base_val + ColumnModel.timestep_column(self, t)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()