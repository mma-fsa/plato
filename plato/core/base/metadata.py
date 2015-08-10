
class Metadata(object):

    def __init__(self, type_descr, inner_func, storage):
        self.__inner_func = inner_func
        self.__type_descr = type_descr
        self.__storage = storage 
        
    @property
    def type_descr(self):
        return self.__type_descr
    
    @property
    def inner_func(self):
        return self.__inner_func
    
    @property 
    def storage(self):
        return self.__storage