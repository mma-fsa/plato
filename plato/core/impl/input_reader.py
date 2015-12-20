'''
Created on Aug 9, 2015

@author: mike
'''

class InputReader(object):
    def __init__(self, func, input_type, input_key):
        self.plato_metadata = InputReaderMetadata(func)
        self.__input_type = input_type
        self.__input_key = input_key
        self.__is_called = False
    
    def __call__(self, *args):
        raise NotImplementedError('Input reader should be treated as a ' + 
                                  'property, not a method call')
    
    def __get__(self, obj, objtype):                
        storage = self.plato_metadata.storage
        model = obj
        # hack to defer loading when model calls __get_columns()
        if model.initializing:
            return None     
        if not self.__is_called:        
            service_locator = model.service_locator
            input_iter = self.__input_type.new_from_input_key(self.__input_key, 
                                                 service_locator).iter
            for i in input_iter: 
                storage.append(self.plato_metadata.inner_func(model, i))
            self.__is_called = True
            
        return storage

from plato.core.base.metadata import Metadata
class InputReaderMetadata(Metadata):
    
    def __init__(self, inner_func):
        super(InputReaderMetadata, self).__init__('input_reader', inner_func,
                                                  [])
        self.__inner_func = inner_func
    