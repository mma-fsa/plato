'''
Created on Aug 9, 2015

@author: mike
'''
import os
from plato.util.config import ConfigReader

class ServiceLocator(object):

    __config_key_cache = {}

    def __init__(self, root_dir=os.getcwd()):
        self.root_dir = root_dir
    
    def get_path_for_input_key(self, input_key):
        config_keys = self.__config_keys
        if not input_key in config_keys:
            err_msg = "Unable to locate input_key: '%(key)'" % {'key':input_key}
            raise Exception(err_msg)            
        return config_keys[input_key]
    
    @property
    def __config_keys(self):
        cache = self.__config_key_cache 
        config_path = os.path.join(self.root_dir, 'config.xml')                    
        if not config_path in cache:        
            if not os.path.exists(config_path):
                raise Exception('Config file not found: ' + config_path)
            cache[config_path] = ConfigReader(config_path).config
        return cache[config_path]
