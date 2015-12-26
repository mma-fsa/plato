'''
Created on Dec 22, 2015

@author: mike
'''
import unittest
from plato.util.data_context_navigator import DataContextNavigator


class DataContextNavigatorTest(unittest.TestCase):


    def testDataContextNavigatorDict(self):
                
        dc = {'foo': 'bar',
              'this': [1,2,3], 
              'that': {'wat': 1, 'err': {'ha':'ja'}}}
        
        dcn = DataContextNavigator(dc)
        
        self.assertEqual(dcn.navigate('.'), dc)
        self.assertEqual(dcn.navigate('foo'), 'bar')
        self.assertEqual(dcn.navigate('this'), [1,2,3])
        self.assertEqual(dcn.navigate('that'), {'wat': 1, 'err': {'ha':'ja'}})
        self.assertEqual(dcn.navigate('that.err'), {'ha':'ja'})
        self.assertEqual(dcn.navigate('that.err.ha'), 'ja')

    def testDataContextNavigatorObj(self):
        
        dc = TestObj1()
        
        dcn = DataContextNavigator(dc)
        
        self.assertEqual(dcn.navigate('foo'), dc.foo)
        self.assertEqual(dcn.navigate('foo.that'), dc.foo.that)
        self.assertEqual(dcn.navigate('foo.err'), dc.foo.err)
        self.assertEqual(dcn.navigate('foo.err.ha'), 'ja')
        self.assertEqual(dcn.navigate('bar'), dc.bar)        
        self.assertEqual(dcn.navigate('bar.who'), dc.bar.who)
        
    
class TestObj1:
    
    def __init__(self):
        self.foo = TestObj2() 
        self.bar = TestObj3()
        
class TestObj2:    
    that = 'wat'
    err = {'ha': 'ja'}

class TestObj3:

    def __init__(self):
        self.nest = TestObj2()
    
    @property
    def who(self):
        return 'me'

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()