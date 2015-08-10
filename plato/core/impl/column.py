'''
Created on Aug 8, 2015

@author: mike
'''

class Column(object):
    def __init__(self, func, automatically_call, aggregator):
        self.plato_metadata = ColumnMetadata(func, automatically_call, \
                                             aggregator)
    
    def __call__(self, *args):
        col_storage = self.plato_metadata.storage
        if args not in col_storage:
            col_storage[args] = \
             self.plato_metadata.inner_func(self.call_self, *args)
        return col_storage[args]
    
    def __get__(self, obj, objtype):
        self.call_self = obj
        return self.__call__

from plato.core.base.metadata import Metadata
class ColumnMetadata(Metadata):
        
    def __init__(self, inner_func, automatically_call, aggregator):
        super(ColumnMetadata, self).__init__('column', inner_func, {})
        self.__automatically_call = automatically_call
        self.__aggregator = aggregator

    @property
    def is_automatically_called(self):
        return self.__automatically_call
    
    @property 
    def aggregator(self):
        return self.__aggregator
