'''
Created on Aug 9, 2015

@author: mike
'''
import unittest
from models.test_model import TestModel

class MockServiceLocator(object):
    _calls = []
    def get_path_for_input_key(self, input_key):
        import os
        self._calls.append(input_key)
        return os.path.join(os.getcwd(), 'input', 'test.csv')

class TestInputReader(unittest.TestCase):

    def test_input_reader(self):
        mock_service_locator = MockServiceLocator()
        model = TestModel(mock_service_locator)
        submodels = model.input_models
        self.assertEqual(len(mock_service_locator._calls), 1)
        self.assertEqual(mock_service_locator._calls[0], 'my_input_key')
        self.assertEqual(len(model.input_models), 3)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()