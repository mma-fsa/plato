'''
Created on Dec 29, 2015

@author: mike
'''
from plato.core.model import Model
from plato.core.decorator.column import column

class LifeContingentAnnuity(Model):

    @column(data_context='pmt')
    def payment(self): pass
    
    @column(data_context=True)
    def period_certain_months(self): pass
    
    @column(data_context=True)
    def mortality(self, attained_age): pass        
    
    @column(data_context=True)
    def units(self, t):
        return self.units(t - 1)
    
    @column(automatically_call=True)
    def liability(self, t):
        return self.units(t) * self.payment()
    