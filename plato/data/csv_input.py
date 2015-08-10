'''
Created on Aug 9, 2015

@author: mike
'''
class CSVInput(object):

    def __init__(self, filename):
        self.filename = filename
        self.__input = None
    
    @property
    def input(self):
        if not self.__input:
            self.__input = self.__read_input(self.filename)
        return self.__input
            
    def __read_input(self, filename):
        import csv
        with open(self.filename) as csvfile:        
            return [row for row in csv.DictReader(csvfile)]
