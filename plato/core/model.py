'''
Created on Aug 8, 2015

@author: mike
'''
from plato.core.service_locator import ServiceLocator
from plato.util.column_identifier_util import ColumnIdentifierUtil
from plato.core.decorator.impl.column import Column, BoundColumnCall
from plato.core.decorator.impl.submodel import SubModel, SubModelBinding
from plato.util.data_context_navigator import DataContextNavigator

class ModelImpl(object):

    __columns = None

    def __init__(self, identifier, data_context=None, parent_model=None,
                 service_locator=ServiceLocator()):                                        
        self.__getattr_lock = True        
        if identifier.find('.') > -1 or identifier.find('#') > -1:
            raise Exception('Identifier cannot contain "." or "#": ' +
                            identifier)
                    
        self.__identifier =  identifier
        self.__service_locator = service_locator       
        self.__data_context = data_context
        self.__parent_model = parent_model                
        self.__columns = dict()
        self.__submodels = dict()
        self.__setup_columns()
        self.__setup_data_context()
        self.__getattr_lock = False
        
    
    def do_timestep(self, t):        
        if self.__columns == None:
            raise ModelException('You must call super.__init__')
        
        for col in self.columns.values():
            metadata = Column.get_metadata(col)
            if metadata.is_automatically_called:
                col(t)
        
        for submodel in self.submodels.value():
            submodel.do_timestep(t)

    def __setup_columns(self):
        '''
            Find all the columns attached to this model and assign storage.            
        '''        
        column_id_util = ColumnIdentifierUtil(self)

        for prop_name in dir(self):
            
            try:            
                prop = getattr(self, prop_name)
            except AttributeError:
                # property has not been initialized yet, ignore and continue
                continue
            
            if Column.is_column(prop):
                column = Column.get_column(prop)
                col_name = prop_name                                
                col_storage_id = column_id_util.get_column_identifier(column)
                storage = self.service_locator.get_storage(col_storage_id)                
                self.columns[col_name] = BoundColumnCall(column, storage, self)
        
            elif SubModel.is_submodel(prop):
                submodel_name = prop_name
                submodel = prop
                self.submodels[submodel_name] = SubModelBinding(submodel, self)            

    def __setup_data_context(self):
        
        dc = self.data_context
        dc_navigator = DataContextNavigator(dc)        
        for col_name, col in self.columns.iteritems():
            metadata = Column.get_metadata(col)            
            if metadata.uses_data_context:
                
                dc_prop = col_name if metadata.data_context == True else\
                    metadata.data_context                
                try: column_context = dc_navigator.navigate(dc_prop)
                except (AttributeError, KeyError):
                    raise Exception('Unable to bind data_context for column'
                                     '%(col_name)s: %(dc_prop)s'
                                     '\n\t data_context = %(dc)s' % locals())
                                    
                for args, val in column_context.iteritems():
                    col.set_value(args, val)        
    
    def __getattribute__(self, name, getattr_lock='_ModelImpl__getattr_lock'):
                
        locked = object.__getattribute__(self, getattr_lock)
        
        # guard against infinite recursion (self.<prop> triggers recursion)
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