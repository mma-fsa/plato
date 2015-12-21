'''
Created on Dec 20, 2015

@author: mike
'''

class ColumnIdentifierUtil(object):
    
    def __init__(self, model):
        model_identifiers = []
        curr_model = model
        while curr_model != None:
            model_identifiers.append(model.identifier)
            curr_model = curr_model.parent_model
        model_identifiers.reverse()
        self.__model_identifier = '.'.join(model_identifiers) + '#' 

    def get_column_identifier(self, column):                        
        return self.__model_identifier + column.__name__
