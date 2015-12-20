from plato.core.model import Model
from plato.core.column import column
from plato.core.submodel import submodel
from test_model.illustrations.hybrid_annuity import HybridAnnuity,\
    DecrementedHybridAnnuity
from test_model.illustrations.period_certain_annuity import PeriodCertainAnnuity,\
    UnitizedPeriodCertainAnnuity
from test_model.illustrations.life_contingent_annuity import LifeContingentAnnuity,\
    DecrementedLifeContingentAnnuity
from plato.core.assumption import assumption

class PayoutReserveModel(Model):
    
    def __init__(self, **args):
        super(PayoutReserveModel, self).__init__(self, **args)

    def startup(self, data_context):
        pass

    @property
    @assumption(data_context='discount_rate')
    def discount_rate(self, rate):
        return rate

    @submodel(data_context='policies')    
    def policies(self, policy, model_args):
        plan_name = policy.plan_name

        if plan_name == 'hybrid':
            return DecrementedHybridAnnuity(**model_args)            

        elif plan_name == 'life_contingent':
            return DecrementedLifeContingentAnnuity(**model_args)

        elif plan_name == 'period_certain':
            return UnitizedPeriodCertainAnnuity(**model_args)
        
        raise ValueError('Unhandled plan_name: ' + plan_name)    
    
    @column(automatically_call=True)
    def reserve(self, t):
        return self.reserve_life_contingent(t) + self.reserve_annuity_certain(t)
    
    @column
    def reserve_life_contingent(self, t):
        res = self.policies.life_contingent_pmt(t)
        if t < self.t_end:
            res += self.discount_rate * self.reserve_life_contingent(t + 1)
        return res        
    
    @column
    def reserve_annuity_certain(self, t):
        res = self.policies.period_certain_pmt(t)
        if t < self.t_end:
            res += self.discount_rate * self.reserve_annuity_certain(t + 1)
        return res

