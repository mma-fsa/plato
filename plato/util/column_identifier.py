'''
Created on Dec 22, 2015

@author: mike
'''

class ColumnIdentifier(str):
    
    def __new__(self, col_id, column, metadata=None):
        obj = str.__new__(self, col_id)
        obj.metadata = {} if metadata == None else metadata
        obj.column = column
        return obj
        