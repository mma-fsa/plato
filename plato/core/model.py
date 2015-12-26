'''
Created on Aug 8, 2015

@author: mike
'''
from plato.core.service_locator import ServiceLocator
from plato.util.column_identifier_util import ColumnIdentifierUtil
from plato.core.decorator.impl.column import Column, ColumnBinding
from plato.core.decorator.impl.submodel import SubModel, SubModelBinding

class ModelImpl(object):

    __columns = None

    def __init__(self, identifier, data_context=None, parent_model=None,
                 service_locator=ServiceLocator()):                        
        self.__getattr_lock = True
        self.__identifier =  identifier
        self.__service_locator = service_locator        
        self.__data_context = data_context
        self.__parent_model = parent_model                
        self.__columns = dict()
        self.__submodels = dict()
        self.__setup_columns()  
        self.__getattr_lock = False
        
    
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

        for prop_name in dir(self):
            prop = getattr(self, prop_name)
            
            if Column.is_column(prop):
                col_name = prop_name
                col = prop                
                col_storage_id = column_id_util.get_column_identifier(col)
                storage = self.service_locator.get_storage(col_storage_id)                
                self.columns[col_name] = ColumnBinding(col, storage, self)
        
            elif SubModel.is_submodel(prop):
                submodel_name = prop_name
                submodel = prop
                self.submodels[submodel_name] = SubModelBinding(submodel, self)            

    
    def __getattribute__(self, name, getattr_lock='_ModelImpl__getattr_lock'):
                
        locked = object.__getattribute__(self, getattr_lock)
        
        # guard against infinite recursion (self.submodels triggers recursion)
        if not locked:
            object.__setattr__(self, getattr_lock, True)            
            value = None
            if name in self.columns:
                value = self.columns[name]            
            elif name in self.submodels:
                value = self.submodels[name]
            object.__setattr__(self, getattr_lock, False)
            
            if value != None:
                return value            
        
        return object.__getattribute__(self, name)

    @property
    def columns(self):
        return self.__columns
    
    @property
    def submodels(self):
        return self.__submodels
    
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

# wrapper to required to store the kwargs
class Model(ModelImpl):
    
    def __init__(self, *args, **kwargs):
        self.__ctor_args = args
        self.__ctor_kwargs = kwargs
        super(Model, self).__init__(*args, **kwargs)        
        
    @property
    def ctor_args(self):
        return self.__ctor_args
    
    @property
    def ctor_kwargs(self):
        return self.__ctor_kwargs

class ModelException(Exception):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return repr(self.value)