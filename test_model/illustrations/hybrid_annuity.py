'''
Created on Dec 18, 2015

@author: mike
'''
from test_model.units.LifeDecrement import LifeDecrement
from plato.core.model import Model
class HybridAnnuity(Model):
    
    def __init__(self, params):
        pass

class DecrementedHybridAnnuity(HybridAnnuity, LifeDecrement):
    
    def __init__(self, params):
        pass
