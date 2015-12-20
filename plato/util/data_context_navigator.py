'''
Created on Dec 18, 2015

@author: mike
'''

class DataContextNavigator(object):

    def __init__(self, data_context):
        self.__data_context = data_context
    
    def navigate(self, property_str):
        curr_obj = self.__data_context
        for prop in property_str.split('.'):
            if prop:
                curr_obj = getattr(curr_obj, prop)
        return curr_obj
 
        