'''
Created on Aug 8, 2015

@author: mike
'''

class Model(object):

    __columns = None

    def __init__(self, params):
        self.__columns = self.__get_columns()

    def startup(self, inforce):
        raise ModelException('You must implement startup in your model')
    
    def timestep_start(self, t):
        pass
    
    def do_timestep(self, t):
        if self.__columns == None:
            raise ModelException('You must call super.__init__')
        for col in self.__columns.values():
            if Model.__is_auto_call_column(col):
                col(t)
    
    def timestep_end(self, t):
        pass
    
    def shutdown(self):
        pass
    
    def __get_columns(self):
        columns = dict()
        for prop_name in dir(self):
            prop_val = getattr(self, prop_name)
            if Model.__is_column(prop_val):
                columns[prop_name] = prop_val
        return columns
    
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