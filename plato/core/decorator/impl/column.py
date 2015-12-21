'''
Created on Aug 8, 2015

@author: mike
'''

class Column(object):
    
    def __init__(self, func, automatically_call, storage=None):
        self.metadata = ColumnMetadata(func, automatically_call, storage)
        self.call_self = None
    
    def __call__(self, *args):
        col_storage = self.metadata.storage
        if args not in col_storage:
            col_storage[args] = \
             self.metadata.inner_func(self.call_self, *args)
        return col_storage[args]
    
    def __get__(self, obj, objtype):
        self.call_self = obj
        return self.__call__    
    
    @staticmethod
    def is_column(it):
        metadata = Column.get_metadata(it)
        return False if metadata == None else metadata.type_descr == 'column'    
    
    @staticmethod
    def is_auto_call(it):
        try:
            return Column.get_metadata(it).is_automatically_called 
        except AttributeError:
            return False

    @staticmethod
    def get_metadata(col):
        try:
            return col.__self__.metadata
        except AttributeError:
            return None
    
    @staticmethod 
    def __inspect_functor(col, expr):
        try:
            return expr(Column.get_column_metadata(col))
        except AttributeError:
            return False

from plato.core.metadata import Metadata
class ColumnMetadata(Metadata):
        
    def __init__(self, inner_func, automatically_call, storage=None):
        super(ColumnMetadata, self).__init__('column', inner_func)
        self.__automatically_call = automatically_call
        self.__storage = storage

    @property
    def is_automatically_called(self):
        return self.__automatically_call
    
    @property 
    def storage(self):
        return self.__storage

    @storage.setter
    def storage(self, value):
        self.__storage = value
