'''
Created on Dec 20, 2015

@author: mike
'''
import unittest
import types
from plato.core.decorator.impl.column import Column, ColumnMetadata


class ColumnTest(unittest.TestCase):

    def testIsColumn(self):
        col = Column(lambda x: x, False)
        self.assertTrue(Column.is_column(col.__call__)) 
        self.assertFalse(Column.is_auto_call(col.__call__))

    def testIsAutoCallColumn(self):
        col = Column(lambda x: x, True)
        self.assertTrue(Column.is_column(col.__call__))
        self.assertTrue(Column.is_auto_call(col.__call__))
        
    def testGetMetadata(self):
        col = Column(lambda x: x, True)
        metadata = Column.get_metadata(col.__call__)
        self.assertIsInstance(metadata, ColumnMetadata, \
                              'Expected column metadata')
        
    def testColumnCall(self):
        
        def func_factory():
            func_factory.call_count = 0
            def column_body(self):
                func_factory.call_count +=  1
                return 'called ' + str(func_factory.call_count)
            return column_body
        
        storage = {}
        col = Column(func_factory(), True, storage)
        
        col_result = col()
        self.assertEqual(col_result, 'called 1', \
                         'unexpected value: ' + col_result)
        self.assertTrue(func_factory.call_count == 1)
        
        col_result2 = col()
        self.assertEqual(col_result2, 'called 1', \
                         'unexpected value: ' + col_result2)
        self.assertTrue(func_factory.call_count == 1)
        
    def testColumnCallArguments(self):
        
        def func_factory():
            func_factory.call_count = 0
            def column_body(self, t):
                func_factory.call_count +=  1
                return t * 10
            return column_body
        
        storage = {}
        col = Column(func_factory(), True, storage)
        
        results = [col(3), col(1), col(1), col(2), col(1), col(2)]
        expected_results = [30, 10, 10, 20, 10, 20]
        
        self.assertEqual(expected_results, results)
        self.assertEqual(func_factory.call_count, 3)
        self.assertEqual({(1,): 10, (2,): 20, (3,): 30}, storage)
    
    
    def testColumnCallMultipleArguments(self):
        
        def func_factory():
            func_factory.call_count = 0
            def column_body(self, x, y):
                func_factory.call_count +=  1
                return x * 10 + y
            return column_body
        
        storage = {}
        col = Column(func_factory(), True, storage)
        
        results = [col(1, 3), col(1, 2), col(3, 3), col(1, 3), col(2, 1), \
                   col(3, 3)]
        expected_results = [13, 12, 33, 13, 21, 33]
        
        self.assertEqual(expected_results, results)
        self.assertEqual(func_factory.call_count, 4)
        self.assertEqual({(1,3): 13, (1,2): 12, (3,3): 33, (2,1):21}, storage)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testIsColumn']
    unittest.main()
    