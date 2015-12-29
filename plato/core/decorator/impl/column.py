'''
Created on Aug 8, 2015

@author: mike
'''
from plato.core.decorator.impl.ModelFeature import ModelFeature

class Column(ModelFeature):
    
    def __init__(self, func, auto_call, data_context=False):
        super(Column, self).__init__(ColumnMetadata(func, auto_call, 
                                                    data_context))        
        self.call_self = None    
    
    def __get__(self, call_self, type=None):        
        return ColumnCall(self, call_self)
    
    @staticmethod
    def is_auto_call(it):
        try:
            return Column.get_metadata(it).is_automatically_called 
        except AttributeError:
            return False

    @staticmethod
    def is_column(it):
        metadata = Column.get_metadata(it)
        return False if metadata == None else metadata.type_descr == 'column'
    
    @staticmethod
    def get_column(it):
        '''
            TODO: This should maybe be handled with inheiritance, or 
            a common interface.
        '''
        if isinstance(it, Column):
            return it
        elif isinstance(it, ColumnCall):
            return it.column                    
        else:
            return None
    
    @staticmethod
    def get_metadata(it):
        column = Column.get_column(it)
        return None if column == None else ModelFeature.get_metadata(column)
    
    @staticmethod
    def get_column_name(col):
        try:
            return Column.get_metadata(col).inner_func.__name__
        except AttributeError:
            return None

class ColumnCall(object):
    
    def __init__(self, column, call_self):
        self.__column = column
        self.__call_self = call_self
        self.__func = Column.get_metadata(column).inner_func
    
    def __call__(self, *args):
        return self.func(self.call_self, *args)
        
    @property
    def column(self):
        return self.__column
    
    @property
    def func(self):
        return self.__func
    
    @property
    def call_self(self):
        return self.__call_self
        
class BoundColumnCall(ColumnCall):
    
    def __init__(self, column, storage, model):
        super(BoundColumnCall, self).__init__(column, model)        
        self.__storage = storage
    
    def __call__(self, *args):        
        if args not in self.__storage:
            self.__storage[args] = super(BoundColumnCall, self).__call__(*args)    
        return self.__storage[args]  
    
    def set_value(self, args, value):
        try: iter(args)
        except TypeError: args = [args]
        
        self.__storage[tuple(args)] = value

from plato.core.metadata import Metadata
class ColumnMetadata(Metadata):
        
    def __init__(self, inner_func, automatically_call, data_context):
        super(ColumnMetadata, self).__init__('column', inner_func)
        self.__automatically_call = automatically_call
        self.__data_context = data_context

    @property
    def is_automatically_called(self):
        return self.__automatically_call    

    @property
    def uses_data_context(self):
        return self.__data_context != False and self.data_context != None

    @property
    def data_context(self):
        return self.__data_context
