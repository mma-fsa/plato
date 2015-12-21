'''
Created on Dec 18, 2015

@author: mike
'''
from plato.core.model import Model
from plato.core.decorator import assumption.assumption
from plato.core.decorators import column.column

class LifeDecrementModel(Model):
    
    def __init__(self, model_args):
        Model.__init__(self, **model_args)
    
    @property
    @assumption(name='mortality_table', type=dict)
    def mortality_table(self, mort_tbl):
        return mort_tbl
            
    @column
    def survival_decrement(self, t):
        pass
    
    @column
    def surrender_decrement(self, t):
        pass
    
    @column
    def death_decremenet(self ,t):
        pass
 
    
    