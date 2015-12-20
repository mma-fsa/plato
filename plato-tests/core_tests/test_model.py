'''
Created on Aug 8, 2015

@author: mike
'''
import unittest
from plato.core_tests.models.test_model import TestModel

class Test(unittest.TestCase):
    
    def test_model_timestep_auto_calls(self):    
        model = TestModel()   
        max_timestep = 3
        for t in xrange(0, max_timestep):
            model.do_timestep(t)
            model.do_timestep(t)
            model.do_timestep(t)
                        
        self.assertEquals(model.va_calls, max_timestep)
        self.assertEquals(model.av_calls, max_timestep)
        self.assertEquals(model.fb_calls, len(model.funds) * max_timestep)
        self.assertEquals(model.fa_calls, max_timestep)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()