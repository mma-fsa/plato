'''
Created on Aug 8, 2015

@author: mike
'''
from plato.core.service_locator import ServiceLocator
from plato.util.column_identifier_util import ColumnIdentifierUtil
from plato.core.decorator.impl.column import Column

class Model(object):

    __columns = None

    def __init__(self, identifier, data_context=None, parent_model=None,
                 service_locator=ServiceLocator()):
        self.initializing = True
        self.__identifier =  identifier
        self.__service_locator = service_locator        
        self.__data_context = data_context
        self.__parent_model = parent_model
        self.__columns = self.__setup_columns()
        self.initializing = False    
    
    def do_timestep(self, t):
        if self.__columns == None:
            raise ModelException('You must call super.__init__')
        for col in self.__columns.values():
            if Model.__is_auto_call_column(col):
                col(t)
    
    def __setup_columns(self):
        '''
            Find all the columns attached to this model and assign storage.            
        '''        
        column_id_util = ColumnIdentifierUtil(self)
        columns = dict()
        
        for col_name in dir(self):
            col = getattr(self, col_name)
            if Column.is_column(col):
                col_id = column_id_util.get_column_identifier(col)
                Column.get_metadata(col).storage = \
                    self.service_locator.get_storage(col_id)                                 
                columns[col_name] = col
                
        return columns
    
    @property
    def identifier(self):
        return self.__identifier 
    
    @property
    def parent_model(self):
        return self.__parent_model
    
    @property
    def data_context(self):
        return self.__data_context
    
    @property
    def service_locator(self):
        return self.__service_locator
        

class ModelException(Exception):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return repr(self.value)