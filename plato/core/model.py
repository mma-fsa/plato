'''
Created on Aug 8, 2015

@author: mike
'''
from plato.util.service_locator import ServiceLocator

class Model(object):

    __columns = None

    def __init__(self, identifier, data_context=None, parent_model=None,
                 service_locator=ServiceLocator()):
        self.initializing = True
        self.__identifier =  identifier
        self.__service_locator = service_locator
        self.__columns = self.__get_columns()
        self.__data_context = data_context
        self.__parent_model = parent_model
        self.initializing = False    
    
    def do_timestep(self, t):
        if self.__columns == None:
            raise ModelException('You must call super.__init__')
        for col in self.__columns.values():
            if Model.__is_auto_call_column(col):
                col(t)
    
    def __get_columns(self):
        columns = dict()
        for prop_name in dir(self):
            prop_val = getattr(self, prop_name)
            if Model.__is_column(prop_val):
                columns[prop_name] = prop_val
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
    
    @staticmethod
    def __is_column(it):
        return Model.__inspect_functor(it, \
                                       lambda metadata:\
                                       metadata.type_descr == 'column')
    
    @staticmethod
    def __is_auto_call_column(it):
        return Model.__inspect_functor(it, \
                                       lambda metadata:\
                                       metadata.is_automatically_called)
    
    @staticmethod 
    def __inspect_functor(col, expr):
        try:
            return expr(col.__self__.plato_metadata)
        except AttributeError:
            return False

class ModelException(Exception):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return repr(self.value)