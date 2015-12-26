'''
Created on Dec 22, 2015

@author: mike
'''

class ColumnIdentifier(str):
    
    def __new__(self, col_id, column):
        obj = str.__new__(self, col_id)
        obj.column = column
        return obj
        