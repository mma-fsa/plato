'''
Created on Aug 9, 2015

@author: mike
'''
from plato.core.service_locator import ServiceLocator

class CSVInput(object):

    def __init__(self, filename):        
        self.filename = filename        
        self.__input = None
    
    @property
    def input(self):
        if not self.__input:
            self.__input = self.__read_input(self.filename)
        return self.__input
    
    @property 
    def iter(self):
        return self.input
    
    def __read_input(self, filename):
        import csv, os
        if not os.path.exists(filename):
            raise Exception('File does not exist: ' + filename)
        with open(self.filename) as csvfile:        
            return [row for row in csv.DictReader(csvfile)]
        
    @staticmethod
    def new_from_input_key(input_key, service_locator=ServiceLocator()):
        return CSVInput(service_locator.get_path_for_input_key(input_key))
