'''
Created on Aug 8, 2015

@author: mike
'''

class SubmodelArray(object):
    '''
    classdocs
    '''
    def __init__(self, submodel_type, size):
        pass
    
    def __getattribute__(self, *args, **kwargs):                
        return object.__getattribute__(self, *args, **kwargs)
