'''
Created on Dec 22, 2015

@author: mike
'''
import unittest
from plato.core.model import Model
from plato.core.decorator.submodel import submodel
from plato_tests.test_utils.model_setup_utility import ModelSetupUtility
from plato.core.decorator.column import column


class SubmodelTest(unittest.TestCase):

    def testSubmodelAggregationCalls(self):
        
        dc = {'foo':'bar', 'wat': 13,\
              'child': [{'id': 1, 'val': 100},
                        {'id': 2, 'val': 200},
                        {'id': 3, 'val': 300},
                        {'id': 4, 'val': 400},
                        {'id': 5, 'val': 500},
                        {'id': 6, 'val': 600},
                        {'id': 7, 'val': 700},
                        {'id': 8, 'val': 800},
                        {'id': 9, 'val': 900}]}
                        
        parent = ModelSetupUtility.setup_test_model(ParentModel,\
            'parent', data_context=dc, test=self)
        
        self.assertEqual(parent.child_model.value(), 4500)
        self.assertEqual(parent.child_model.arg_value(100), 4500 + 9 * 200)


class ParentModel(Model):
    
    child_model_ctor_calls = 0
    
    def __init__(self, identifier, data_context=None, parent_model=None,
                 service_locator=None, test=None):
        self.__test = test
        super(ParentModel, self).__init__(identifier, \
            data_context=data_context, parent_model=parent_model,
            service_locator=service_locator)        
    
    @property
    def test(self):
        return self.__test
    
    @submodel(data_context='child')
    def child_model(self, data, kwargs):
        
        self.child_model_ctor_calls += 1
        
        self.test.assertIn('id', data)
        self.test.assertIn('val', data)
        self.test.assertEquals(data['id'] * 100, data['val'])
        
        return ChildModel('child_model_' + str(data['id']), **kwargs)

class ChildModel(Model):
    
    def id(self):
        return self.data_context['id']
    
    @column
    def value(self):
        return self.data_context['val']
    
    @column
    def arg_value(self, t):
        return self.data_context['val'] + t * 2

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()