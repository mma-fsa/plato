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

        
    def testMultipleModelColumnCalls(self):
         
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
        model2.base_val = 20
         
        # Check that storage has been allocated for model 2 and that
        # model 1's storage is still intact
        
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
        
        self.assertTrue(len(storage) == 6)
        self.assertEqual(storage['model1#two_dimensional_column'], {})
        self.assertEqual(storage['model1#timestep_column'],
                          {(1,): 20, (2,): 30, (3,): 40, (4,): 50})
        
        self.assertEqual(storage['model2#two_dimensional_column'], {})
        self.assertEqual(storage['model2#timestep_column'],
                          {(1,): 30, (2,): 40, (3,): 50, (4,): 60})
        
        self.assertEqual(storage['model3#two_dimensional_column'], {})
        self.assertEqual(storage['model3#timestep_column'], {})
         
        for i in xrange(1, 5):
            model2.timestep_column(i)
            model3.timestep_column(i)            
            model1.timestep_column(i)
        
        model3.timestep_column(5)
        
        self.assertTrue(len(storage) == 6)    
        self.assertEqual(storage['model1#two_dimensional_column'], {})
        self.assertEqual(storage['model1#timestep_column'],
                          {(1,): 20, (2,): 30, (3,): 40, (4,): 50})
        
        self.assertEqual(storage['model2#two_dimensional_column'], {})
        self.assertEqual(storage['model2#timestep_column'],
                          {(1,): 30, (2,): 40, (3,): 50, (4,): 60})
        
        self.assertEqual(storage['model3#two_dimensional_column'], {})
        self.assertEqual(storage['model3#timestep_column'], 
                         {(1,): 40, (2,): 50, (3,): 60, (4,): 70, (5,): 80})
                
                
    def testModelColumnCalls(self):                
        svc_loc_setup = ModelSetupUtility.setup_service_locator()
        svc_loc = svc_loc_setup['service_locator']
        storage = svc_loc_setup['storage']
        model = ModelSetupUtility.setup_test_model(ColumnModel, \
            service_locator=svc_loc)
           
        # Check that storage was allocated correctly
        self.assertTrue(model)
        self.assertTrue(len(storage.keys()) == 2)
        self.assertIn('sample_model#timestep_column', storage)
        self.assertIn('sample_model#two_dimensional_column', storage)
           
        self.assertEqual(model.timestep_column_calls, 0)
        self.assertEqual(model.two_dimensional_column_calls, 0)
           
        # Check that columns are called only once for each argument
        self.assertEqual(model.two_dimensional_column(2, 3), 302)
        self.assertEqual(model.two_dimensional_column(2, 3), 302)
        self.assertEqual(model.two_dimensional_column(2, 3), 302)
           
        self.assertEqual(model.timestep_column_calls, 0)
        self.assertEqual(model.two_dimensional_column_calls, 1)
        self.assertEqual(storage['sample_model#timestep_column'], {})
        self.assertEqual(storage['sample_model#two_dimensional_column'], \
                        {(2,3) : 302})
           
        # Check that additional calls work correctly
        self.assertEqual(model.two_dimensional_column(3, 3), 303)
        self.assertEqual(model.two_dimensional_column(2, 4), 402)
        self.assertEqual(model.two_dimensional_column(2, 3), 302)
           
        self.assertEqual(model.timestep_column_calls, 0)
        self.assertEqual(model.two_dimensional_column_calls, 3)
        self.assertEqual(storage['sample_model#timestep_column'], {})        
        self.assertEqual(storage['sample_model#two_dimensional_column'], \
                        {(2,3) : 302, (3,3):303, (2,4): 402})
        
    
    def testModelDataContext(self):                
        
        dc = {'timestep_column': {1: 10, (2,) : 30},
              'two_dimensional_column': {(1,2) : 3, (4,5): 6},
              'ignore_column': {(1,2) : 999, (4,5): 899} }
                        
        svc_loc_setup = ModelSetupUtility.setup_service_locator()
        svc_loc = svc_loc_setup['service_locator']
        
        model = ModelSetupUtility.setup_test_model(IgnoreColumnModel, \
            service_locator=svc_loc, data_context=dc)
        
        self.assertEqual(model.timestep_column(1), 10)
        self.assertEqual(model.timestep_column(2), 30)
        self.assertEqual(model.timestep_column(3), 30)
        self.assertEqual(model.timestep_column(3), 30)
        self.assertEqual(model.timestep_column(1), 10)
        self.assertEqual(model.timestep_column(2), 30)
        self.assertEqual(model.timestep_column_calls, 1)
        
        self.assertEqual(model.two_dimensional_column(1, 2), 3)
        self.assertEqual(model.two_dimensional_column(4, 5), 6)
        self.assertEqual(model.two_dimensional_column(1, 1), 101)
        self.assertEqual(model.two_dimensional_column(1, 2), 3)
        self.assertEqual(model.two_dimensional_column(4, 5), 6)
        self.assertEqual(model.two_dimensional_column(1, 1), 101)
        self.assertEqual(model.two_dimensional_column_calls, 1)
        
        self.assertEqual(model.ignore_column(1, 2), 4)
        self.assertEqual(model.ignore_column(4, 5), 13)
        

class EmptyModel(Model):
    pass

class ColumnModel(Model):
    
    def __init__(self, *args, **kwargs):        
        self.__timestep_column_calls = 0        
        super(ColumnModel, self).__init__(*args, **kwargs)
        self.__two_dimensional_column_calls = 0        
    
    @property
    def timestep_column_calls(self):
        return self.__timestep_column_calls
    
    @property
    def two_dimensional_column_calls(self):
        return self.__two_dimensional_column_calls
    
    @column
    def timestep_column(self, t):
        self.__timestep_column_calls += 1
        return 10 * t
    
    @column
    def two_dimensional_column(self, x, y):
        self.__two_dimensional_column_calls += 1
        return x + 100 * y
    
    def member_function(self, t):
        return 100.0
    
    @staticmethod
    def static_function(self, x, y):
        return 2 * x + y

class IgnoreColumnModel(ColumnModel):
    
    @column(data_context=False)
    def ignore_column(self, t, s):
        return 2 * t + s

class DataAndColumnModel(ColumnModel):
    
    def __init__(self, *args, **kwargs):
        self.__base_val = 0
        super(DataAndColumnModel, self).__init__(*args, **kwargs)
        
    @property
    def base_val(self):
        return self.__base_val
    
    @base_val.setter
    def base_val(self, value):
        self.__base_val = value
        
    @column
    def timestep_column(self, t):
        return self.base_val + \
            super(DataAndColumnModel, self).timestep_column(t)

if __name__ == "__main__":
    unittest.main()