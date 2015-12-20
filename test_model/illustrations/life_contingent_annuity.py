'''
Created on Dec 18, 2015

@author: mike
'''
from plato.core.model import Model
from test_model.units.LifeDecrement import LifeDecrement

class LifeContingentAnnuity(Model):

    def __init__(self, params):
        pass

class DecrementedLifeContingentAnnuity(LifeContingentAnnuity, LifeDecrement):
    
    def __init__(self, params):
        pass