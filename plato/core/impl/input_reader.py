'''
Created on Aug 9, 2015

@author: mike
'''

class InputReader(object):
    def __init__(self, func, ipt_iter, obj_type):
        self.__ipt_iter = ipt_iter
        self.__obj_type = obj_type
        self.plato_metadata = InputReaderMetadata(func)
    
    def __call__(self, *args):
        storage = self.plato_metadata.storage
        for i in self.__ipt_iter:
            storage.append(self.__obj_type(**i))
        
    
    def __get__(self, obj, objtype):
        self.call_self = obj
        return self.__call__
    
        
from plato.core.base.metadata import Metadata
class InputReaderMetadata(Metadata):
    
    def __init__(self, inner_func):
        super(InputReaderMetadata, self).__init__('input_reader', inner_func, \
                                                  [])
        self.__inner_func = inner_func
    