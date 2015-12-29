'''
Created on Aug 9, 2015

@author: mike
'''
import os
from plato.util.config import ConfigReader
from plato.core.storage.in_memory_storage_repository import InMemoryStorageRepository

class ServiceLocator(object):

    def __init__(self, storage_repository=None):        
        self.__storage_repository = storage_repository if storage_repository \
            else InMemoryStorageRepository()
        
    def get_storage(self, storage_identifier):
        return self.__storage_repository.get_storage(storage_identifier);
    
    