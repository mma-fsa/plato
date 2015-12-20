'''
Created on Dec 18, 2015

@author: mike
'''
from plato.core.model import Model
from test_model.units.PolicyUnits import PolicyUnit

class PeriodCertainAnnuity(Model):
    def __init__(self, params):
        pass

class UnitizedPeriodCertainAnnuity(PeriodCertainAnnuity, PolicyUnit):
    pass
