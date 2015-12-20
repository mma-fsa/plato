'''
Created on Aug 9, 2015

@author: mike
'''
import unittest
import os
from plato.util.config import ConfigReader

class TestConfig(unittest.TestCase):

    def test_config(self):        
        cwd = os.getcwdu()
        config_file = os.path.join(cwd, 'config.xml')
        results = ConfigReader(config_file).config
        self.assertEqual(results['bond_input'], r'C:\foo\bar\bonds.csv')
        self.assertEqual(results['other_input'], r'C:\foo\bar\others.csv')
        self.assertEqual(results['bond_ouput'], r'C:\thud\whack\bonds.csv')
        self.assertEqual(results['other_output'], r'C:\thud\whack\others_out.csv')        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()