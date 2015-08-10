'''
Created on Aug 8, 2015
2
@author: mike
'''
import unittest
from plato.core_tests.models.test_model import TestModel

class TestColumn(unittest.TestCase):

    def test_single_arg_column(self):         
        model = TestModel()
        results = [model.fixed_account(10) for i in xrange(0,100)]
        expected_results = 100 * [pow(1.005, 10) * 50.0]
        self.assertEqual(results, expected_results, 'results not equal')
        self.assertEqual(model.fa_calls, 1, 'called too many times')
        self.assertEqual(model.va_calls, 0, 'called too many times')
        self.assertEqual(model.fb_calls, 0, 'called too many times')
        self.assertEqual(model.av_calls, 0, 'called too many times')
        
    def test_multiple_arg_columns(self):
        model = TestModel()        
        results = [model.fund_balance(10, 'NDX') for i in xrange(0,100)]
        expected_results = 100 * [pow(1.005, 10) * 200.0]
        self.assertEqual(results, expected_results, 'results not equal')
        self.assertEqual(model.fa_calls, 0, 'called too many times')
        self.assertEqual(model.va_calls, 0, 'called too many times')
        self.assertEqual(model.fb_calls, 1, 'called too many times')
        self.assertEqual(model.av_calls, 0, 'called too many times')
    
    def test_nested_columns(self):
        pass

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()