'''
Created on Aug 8, 2015

@author: mike
'''
from plato.core.decorator.impl.ModelFeature import ModelFeature

class Column(ModelFeature):
    
    def __init__(self, func, auto_call):
        super(Column, self).__init__(ColumnMetadata(func, auto_call))        
        self.call_self = None    
    
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
    def get_metadata(it):            
        if isinstance(it, Column):
            return ModelFeature.get_metadata(it)
        elif isinstance(it, ColumnBinding):
            return ModelFeature.get_metadata(it.column)
        else:
            return None    
    
    @staticmethod
    def get_column_name(col):
        try:
            return Column.get_metadata(col).inner_func.__name__
        except AttributeError:
            return None
        
class ColumnBinding(Column):
    
    def __init__(self, column, storage, model):
        self.__column = column
        self.__storage = storage
        self.__model = model
    
    def __call__(self, *args):        
        metadata = Column.get_metadata(self.__column)
        if args not in self.__storage:
            self.__storage[args] = metadata.inner_func(self.__model, *args)
        return self.__storage[args]
    
    @property
    def column(self):
        return self.__column    

from plato.core.metadata import Metadata
class ColumnMetadata(Metadata):
        
    def __init__(self, inner_func, automatically_call):
        super(ColumnMetadata, self).__init__('column', inner_func)
        self.__automatically_call = automatically_call

    @property
    def is_automatically_called(self):
        return self.__automatically_call    
