'''
Created on Aug 8, 2015

@author: mike
'''

from plato.core.model import Model
from plato.core.column import Column

class TestModel(Model):
    
    av_calls = 0
    va_calls = 0
    fb_calls = 0
    fa_calls = 0
    
    funds = ['SPX', 'NDX', 'RUS']
    
    def __init__(self):
        super(TestModel, self).__init__(self)
    
    @Column(automatically_call=True)
    def account_value(self, t):
        self.av_calls += 1
        fa_balance = self.fixed_account(t)
        va_balance = self.variable_account(t)        
        return fa_balance + va_balance
    
    @Column(automatically_call=False)
    def variable_account(self, t):
        self.va_calls += 1        
        balances = [self.fund_balance(t, fund_name) \
                    for fund_name in self.funds]
        return reduce(lambda x,y: x + y, balances) 
    
    @Column
    def fund_balance(self, t, fund_name):
        self.fb_calls += 1
        val = 0.0
        if fund_name == 'SPX':
            val = pow(1.01, t) * 100.0
        elif fund_name == 'NDX':
            val = pow(1.005, t) * 200.0
        elif fund_name == 'RUS':
            val = pow(1.075, t) * 15.0
        return val
    
    @Column 
    def fixed_account(self, t):
        self.fa_calls += 1
        return pow(1.005, t) * 50.0