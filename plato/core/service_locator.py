'''
Created on Aug 9, 2015

@author: mike
'''
import os
from plato.util.config import ConfigReader
from plato.core.storage.in_memory_storage_repository import InMemoryStorageRepository

class Timestep(object):
    def __init__(self, min=0, max=360):
        self.__min = int(min)
        self.__max = int(max)
    
    @property
    def max(self):
        return self.__max
    
    @property
    def min(self):
        return self.__min
    
class ServiceLocator(object):

    def __init__(self, storage_repository=None, default_timestep=Timestep()):        
        self.__storage_repository = storage_repository if storage_repository \
            else InMemoryStorageRepository()
        self.__default_timestep = default_timestep
        
    def get_storage(self, storage_identifier):
        return self.__storage_repository.get_storage(storage_identifier);
    
    @property
    def default_timestep(self):
        return self.__default_timestep

    