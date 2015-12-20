'''
Created on Dec 20, 2015

@author: mike
'''
import os
import yaml

class ConfigDirectoryReader(object):
    
    @staticmethod
    def read_config_directory(config_dir_path):
        
        if not os.path.isdir(config_dir_path):
            raise ValueError("Invalid config directory: " + config_dir_path)
        
        config = dict()
        input_file_path = os.path.join(config_dir_path, 'input.yaml')
        if not os.path.isfile(input_file_path):
            raise Exception('Missing input file: ' + input_file_path)
        with open(input_file_path, 'r') as stream:
            config['input'] = yaml.load(stream)    
        
        output_filter_path = os.path.join(config_dir_path, 'output_filter.yaml')
        if not os.path.isfile(output_filter_path):
            raise Exception('Missing output filter: ' + output_filter_path)
        with open(output_filter_path, 'r') as stream:
            config['output_filter'] = yaml.load(stream)    
    
        return config
        