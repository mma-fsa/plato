'''
Created on Dec 20, 2015

@author: mike
'''
from plato.core.decorator.impl.column import Column
from inspect import getargspec
from plato.util.column_identifier import ColumnIdentifier

class ColumnIdentifierUtil(object):
    
    def __init__(self, model):
        model_identifiers = []
        curr_model = model
        while curr_model != None:
            model_identifiers.append(curr_model.identifier)
            curr_model = curr_model.parent_model
        model_identifiers.reverse()
        self.__model_identifier = '.'.join(model_identifiers) + '#'
    
    def get_column_identifier(self, column):
        col_id = self.__model_identifier + Column.get_column_name(column)
        metadata = {'args': getargspec(Column.get_metadata(column).inner_func)}                             
        return ColumnIdentifier(col_id, column, metadata)
    