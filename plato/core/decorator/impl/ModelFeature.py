class ModelFeature(object):
    
    def __init__(self, metadata):
        self.__metadata = metadata
    
    @property
    def metadata(self):
        return self.__metadata
    
    @staticmethod
    def get_metadata(it):
        try:
            return it.metadata
        except AttributeError:
            return None    

    @staticmethod 
    def __inspect_functor(it, expr):
        try:
            return expr(ModelFeature.get_metadata(it))
        except AttributeError:
            return False