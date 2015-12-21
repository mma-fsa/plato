
class Metadata(object):

    def __init__(self, type_descr, inner_func):
        self.__inner_func = inner_func
        self.__type_descr = type_descr
        
    @property
    def type_descr(self):
        return self.__type_descr
    
    @property
    def inner_func(self):
        return self.__inner_func
