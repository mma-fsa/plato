'''
Created on Dec 18, 2015

@author: mike
'''
from plato.core.decorator.impl.column import Column
from _collections import defaultdict
from plato.core.metadata import Metadata
from plato.core.decorator.impl.ModelFeature import ModelFeature
from plato.util.data_context_navigator import DataContextNavigator

class SubModel(ModelFeature):

    def __init__(self, factory_function, data_context_property):
        super(SubModel, self).__init__(SubModelMetadata(factory_function))                    
        self.__data_context_property = data_context_property        
        self.__factory_function = factory_function        
    
    @property
    def data_context_property(self):
        return self.__data_context_property
    
    @staticmethod
    def is_submodel(it):
        metadata = SubModel.get_metadata(it)
        return False if metadata == None else metadata.type_descr == 'submodel'
    
    @staticmethod
    def get_factory_fn(submodel):
        return SubModel.get_metadata(submodel).inner_func
    
    def __call__(self, *args):
        raise 'Submodels are accessed like properties, not functions'
    
class SubModelMetadata(Metadata):
    
    def __init__(self, factory_func):
        super(SubModelMetadata, self).__init__('submodel', factory_func)        
    
class SubModelBinding(object):
    
    def __init__(self, submodel, parent_model):
        self.__getattr_lock = True
        self.__parent_model = parent_model        
        self.__submodel_list = []        
        self.__aggregators = self.__setup(parent_model, submodel)        
        self.__getattr_lock = False
    
    @staticmethod
    def __setup(parent_model, submodel):
        
        parent_data_ctx = parent_model.data_context
        factory_fn = SubModel.get_factory_fn(submodel)
        data_context_prop = submodel.data_context_property
        child_data_ctx = DataContextNavigator(parent_data_ctx)\
            .navigate(data_context_prop)
        
        try:
            data_context_iter = iter(child_data_ctx)
        except TypeError:
            data_context_iter = [child_data_ctx]
            
        # create a map of column names to submodel instances, so we can
        # efficently create aggregators once the loop is done, i.e.
        #  { 'column_name1': [ model_instance1, model_instance2, ...], ... }
        models_for_col_names = defaultdict(list)
        
        for data_context in data_context_iter:
            kwargs = dict(parent_model.ctor_kwargs)
            kwargs['data_context'] = data_context
            
            submodel = factory_fn(parent_model, data_context, kwargs)
            
            for col_name in submodel.columns.keys():
                models_for_col_names[col_name].append(submodel)
        
        # Aggregators apply an operation across many submodels, e.g. 
        # sum all columns of the submodels
        aggregators = {}        
        for col_name, models in models_for_col_names.iteritems():
            aggregators[col_name] = SubModelComputation(col_name, models)
        
        return aggregators
    
    def __getattribute__(self, name, getattr_lock='_SubModelBinding__getattr_lock'):
        
        locked = object.__getattribute__(self, getattr_lock)
        
        if not locked:
            value = None
            object.__setattr__(self, getattr_lock, True)
            if name in self.aggregators:
                value = self.aggregators[name]
            object.__setattr__(self, getattr_lock, False)
            
            if value != None:
                return value
        
        return object.__getattribute__(self, name) 
    
    def __iter__(self):
        return iter(self.__submodel_list)
    
    @property
    def aggregators(self):
        return self.__aggregators

class SubModelComputation():
    
    def __init__(self, column_name, models, reduce_fn=lambda x,y: x + y):
        self.__models = models
        self.__col_value_accessor = \
            SubModelComputation.__model_col_accessor(column_name)
        
        # can be any associative operator (e.g. addition)
        self.__reduce_fn = reduce_fn        
        self.__column_arg_applicators = self.__model_col_accessor(column_name)
    
    def __call__(self, *args, **kwargs):        
        column_call = self.__column_arg_applicators(args, kwargs)
        model_vals = map(column_call, self.__models)
        return reduce(self.__reduce_fn, model_vals)    
    
    @staticmethod
    def __model_col_accessor(col_name):        
        def col_argument_applicator(args, kwargs):                        
            def col_accessor(model):
                column = getattr(model, col_name)
                return column(*args, **kwargs)                
            return col_accessor
        return col_argument_applicator
    