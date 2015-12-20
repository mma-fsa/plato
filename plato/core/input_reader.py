'''
Created on Aug 9, 2015

@author: mike
'''

from plato.core.impl.input_reader import InputReader as InputReaderImpl

def InputReader(input_type=None, input_key=None):            
    def wrapper(inner_func):
        return InputReaderImpl(inner_func, input_type, input_key)
    return wrapper
