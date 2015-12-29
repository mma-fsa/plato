'''
Created on Dec 20, 2015

@author: mike
'''
from plato.core.service_locator import ServiceLocator
from plato.core.storage.in_memory_storage_repository import InMemoryStorageRepository
from collections import defaultdict

class ModelSetupUtility(object):

    def __init__(self, params):
        pass
    
    @staticmethod
    def setup_service_locator(storage=None):
        storage = storage if storage != None else defaultdict(dict)
        storage_repository = InMemoryStorageRepository(storage)
        service_locator = ServiceLocator(storage_repository=storage_repository)
        return {'storage':storage, 'storage_repository': storage_repository,\
                'service_locator': service_locator}
    
    @staticmethod
    def setup_test_model(model_class, identifier='sample_model', 
                         data_context={}, parent_model=None,
                         service_locator=ServiceLocator(),
                         test=None):
        
        model = None
        if test != None:
            model = model_class(identifier, data_context=data_context,
                          parent_model=parent_model,
                          service_locator=service_locator,
                          test=test)
        else:  
            model = model_class(identifier, data_context=data_context,
                          parent_model=parent_model,
                          service_locator=service_locator)
        
        return model



