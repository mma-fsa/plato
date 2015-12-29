'''
Created on Dec 19, 2015

@author: mike
'''
from __future__ import print_function
import yaml, os
import importlib
from plato.core.storage.in_memory_storage_repository import InMemoryStorageRepository
from plato.core.service_locator import ServiceLocator


class ModelRunner(object):
    
    def __init__(self, config_location, logfile):
        self.__logfile = logfile
        self.__config_location = os.path.abspath(config_location)
        self.__read_config(config_location)
    
    def __get_input(self):
        try: 
            input_file = self.config['input']['file']
        except KeyError as e: 
            raise ConfigKeyError(e)
        
        wd = self.__config_location
        if not os.path.isabs(input_file):            
            input_file = os.path.abspath(os.path.join(wd, input_file))
        
        if not os.path.isfile(input_file):
            raise Exception('Cannot locate input file: ' + input_file)
        
        with open(input_file, 'r') as ipt_stream:
            return yaml.load(ipt_stream)
    
    def __get_main_model_instance(self, data_context, svc_loc):
        
        try: 
            model_config = self.config['model']
            module_name = model_config['module']
            class_name = model_config['class']
            identifier = model_config['identifier']            
        except KeyError as e: 
            raise ConfigKeyError(e)
        
        try:
            module = importlib.import_module(module_name)
        except ImportError as e:
            raise Exception('Unable to import module: ' + module_name)
        
        try:            
            cls = getattr(module, class_name)
        except AttributeError as e:
            raise Exception('Unable to find class in module: ' + class_name)
        
        return cls(identifier, data_context=data_context, 
                   service_locator=svc_loc)        
    
    def __get_output_writer(self):
        
        try: 
            output_config = self.config['output']
            module_name = output_config['module']
            class_name = output_config['class']
            args = output_config['args']
        except KeyError as e:
            raise ConfigKeyError(e)
        
        try:
            module = importlib.import_module(module_name)
        except ImportError as e:
            raise Exception('Unable to import module: ' + module_name)
        
        try:            
            cls = getattr(module, class_name)
        except AttributeError as e:
            raise Exception('Unable to find class in module: ' + class_name)
        
        return cls(args)
        
    def run(self):
        
        self.log("Configuring model...")
        
        self.log("\tinput")
        data_context = self.__get_input()
        self.log("\tstorage")
        storage_repo = InMemoryStorageRepository()
        self.log("\tservice locator")
        svc_loc = ServiceLocator(storage_repo)
        self.log("\tmain model")
        main_model = self.__get_main_model_instance(data_context, svc_loc)
        
        try:
            time_params = self.config['run']['timestep']
            ts_min = time_params['min']
            ts_max = time_params['max']
        except KeyError as e:
            raise ConfigKeyError(e)
        
        self.log("Running model from %(ts_min)s to %(ts_max)s" % locals())
        for t in xrange(ts_min, ts_max + 1):
            self.log("\t%s" % t)
            main_model.do_timestep(t)
        self.log("\tdone")
        
        self.log("Creating output writer...")
        output_writer = self.__get_output_writer()        
        self.log("Writing output...")
        output_writer.write(storage_repo.column_storage)

    def __read_config(self, config_location):
        config_file = os.path.join(config_location, 'config.yaml')
        if not os.path.isfile(config_file):
            raise Exception('Expected config file at: ' + config_file)
        
        with open(config_file, 'r') as cfg_file:
            self.__config = yaml.load(cfg_file)
            
    def log(self, *objs):
        print("LOG: ", *objs, file=self.__logfile)

    @property
    def config(self):
        return self.__config

class ConfigKeyError(Exception):
    def __init__(self, keyError, msg='Config file missing required section: '):
        super(ConfigKeyError, self).__init__(msg + str(keyError))
    