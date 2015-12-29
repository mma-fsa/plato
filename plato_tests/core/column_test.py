'''
Created on Dec 20, 2015

@author: mike
'''
import unittest
from plato.core.decorator.impl.column import Column, ColumnMetadata,\
    BoundColumnCall


class ColumnTest(unittest.TestCase):

    def testIsColumn(self):
        col = Column(lambda x: x, False)
        self.assertTrue(Column.is_column(col)) 
        self.assertFalse(Column.is_auto_call(col))

    def testIsAutoCallColumn(self):
        col = Column(lambda x: x, True)
        self.assertTrue(Column.is_column(col))
        self.assertTrue(Column.is_auto_call(col))
        
    def testGetMetadata(self):
        col = Column(lambda x: x, True)
        metadata = Column.get_metadata(col)
        self.assertIsInstance(metadata, ColumnMetadata, \
                              'Expected column metadata')
        
    def testNoArgBoundColumn(self):
                        
        storage = {}
        model = object()
        
        def get_col_fn(unit_test, expected_model):
            get_col_fn.call_count = 0
            def column_fn(self):                
                get_col_fn.call_count += 1
                # check that argument passed in is the model                
                unit_test.assertEqual(expected_model, self)                                            
                return 100
            
            return column_fn
        
        # Setup a function to memoize
        column_fn = get_col_fn(self, model)
        
        # Setup the Column
        column = Column(column_fn, True)
        
        # Setup the ColumnBinding, maps a column to it's storage
        # and provides a callable interface
        column_binding = BoundColumnCall(column, storage, model)
        
        # Call the column        
        self.assertEqual(get_col_fn.call_count, 0)
        column_binding()
        self.assertEqual(get_col_fn.call_count, 1)
        self.assertEqual({tuple() : 100}, storage)
        
        # subsequent calls should have no effect
        for i in xrange(1, 10):
            column_binding()
            self.assertEqual({tuple() : 100}, storage)
            self.assertEqual(get_col_fn.call_count, 1)
            
    def testSingleArgBoundColumn(self):
        
        storage = {}
        model = object()
        
        def get_col_fn(unit_test, expected_model):
            get_col_fn.call_count = 0
            def column_fn(self, t):
                # check that argument passed in is the model
                get_col_fn.call_count += 1                
                unit_test.assertEqual(expected_model, self)                                            
                return 100 * t 
            return column_fn
        
        # Setup a function to memoize
        column_fn = get_col_fn(self, model)
        
        # Setup the Column
        column = Column(column_fn, True)
        
        # Setup the ColumnBinding, maps a column to it's storage
        # and provides a callable interface
        column_binding = BoundColumnCall(column, storage, model)
        
        # Call the column        
        self.assertEqual(get_col_fn.call_count, 0)
        column_binding(2)
        self.assertEqual(get_col_fn.call_count, 1)
        self.assertEqual({(2,) : 200}, storage)
        
        # Call column again
        column_binding(3)
        self.assertEqual(get_col_fn.call_count, 2)
        self.assertEqual({(2,) : 200, (3,) : 300}, storage)
        
        # subsequent calls should have no effect
        for i in xrange(1, 10):
            column_binding(2)
            column_binding(3)
            self.assertEqual(get_col_fn.call_count, 2)
            self.assertEqual({(2,) : 200, (3,) : 300}, storage)
        
        # Call column again
        column_binding(4)
        self.assertEqual(get_col_fn.call_count, 3)
        self.assertEqual({(2,) : 200, (3,) : 300, (4,):400},  storage)
        
    def testMultiArgBoundColumn(self):
        
        storage = {}
        model = object()
        
        def get_col_fn(unit_test, expected_model):
            get_col_fn.call_count = 0
            def column_fn(self, t, s):
                # check that argument passed in is the model
                get_col_fn.call_count += 1                
                unit_test.assertEqual(expected_model, self)                                            
                return 100 * t + s
            return column_fn
        
        # Setup a function to memoize
        column_fn = get_col_fn(self, model)
        
        # Setup the Column
        column = Column(column_fn, True)
        
        # Setup the ColumnBinding, maps a column to it's storage
        # and provides a callable interface
        column_binding = BoundColumnCall(column, storage, model)
        
        # Call the column        
        self.assertEqual(get_col_fn.call_count, 0)
        column_binding(2, 0)
        self.assertEqual(get_col_fn.call_count, 1)
        self.assertEqual({(2, 0) : 200}, storage)
        
        # Call column again
        column_binding(3, 1)
        self.assertEqual(get_col_fn.call_count, 2)
        self.assertEqual({(2, 0) : 200, (3, 1) : 301}, storage)
        
        # subsequent calls should have no effect
        for i in xrange(1, 10):
            column_binding(2, 0)
            column_binding(3, 1)
            self.assertEqual(get_col_fn.call_count, 2)
            self.assertEqual({(2, 0) : 200, (3, 1) : 301}, storage)
        
        # Call column again
        column_binding(3, 0)
        self.assertEqual(get_col_fn.call_count, 3)
        self.assertEqual({(2, 0) : 200, (3, 1) : 301, (3, 0): 300}, storage)
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testIsColumn']
    unittest.main()
    