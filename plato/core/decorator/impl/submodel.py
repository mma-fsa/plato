'''
Created on Dec 18, 2015

@author: mike
'''

class SubModel(object):

    def __init__(self, factory_function, data_context_property):
        self.__submodel_list = []
        self.__parent_model = factory_function.__self__
        self.__data_context = self.__parent_model        
        data_context_iter = None
        try:
            data_context_iter = iter(self.__data_context)
        except TypeError:
            data_context_iter = [self.__data_context]
        for data_context in data_context_iter:
            self.__submodel_list.append(factory_function(data_context))    
    
    def __getitem__(self):
        pass
    
    def __get__(self, name):
        pass
    
    def __set__(self, name):
        pass
    
    @staticmethod
    def get_ctor_args(model):
        return dict()