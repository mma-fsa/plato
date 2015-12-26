'''
Created on Dec 20, 2015

@author: mike
'''
import collections

class InMemoryStorageRepository(object):
    
    def __init__(self, storage=None):
        self.column_storage = storage if storage != None \
            else collections.defaultdict(dict)
    
    def get_storage(self, column_identifier):
        return self.column_storage[column_identifier]
