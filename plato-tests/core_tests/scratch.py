'''
Created on Aug 8, 2015

@author: mike
'''
import unittest


class Descriptor(object):

    def __init__(self):
        self._name = ''

    def __get__(self, instance, owner):
        print "Getting: %s" % self._name
        return self._name

    def __set__(self, instance, name):
        print "Setting: %s" % name
        self._name = name.title()

    def __delete__(self, instance):
        print "Deleting: %s" %self._name
        del self._name

class Person(object):
    name = Descriptor()
    
    def __getattribute__(self, *args, **kwargs):
        return object.__getattribute__(self, *args, **kwargs)

if __name__ == "__main__":
    mike = Person()
    mike.name = 'footo'
    mike.tootoo
