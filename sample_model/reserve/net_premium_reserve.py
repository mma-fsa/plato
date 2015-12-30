from sample_model.annuity.life_contingent_annuity import LifeContingentAnnuity
from plato.core.decorator.submodel import submodel
from plato.core.decorator.column import column
from plato.core.model import Model

class NetPremiumReserve(Model):

    @submodel(data_context='policies')
    def policies(self, data_context, kwargs):        
        child_id = "%(plan_name)s_%(id)s" % data_context
        return LifeContingentAnnuity(child_id, **kwargs)
    
    def total_liability(self, t):
        return self.policies.liability(t)
    
    @column(data_context='stat_rate')
    def discount_rate(self): pass
    
    @column(automatically_call=True)
    def total_reserve(self, t):
        if t <= self.timestep.max:   
            return self.discount_rate() * self.total_reserve(t + 1) + \
                self.total_liability(t)                
        else:
            return 0
