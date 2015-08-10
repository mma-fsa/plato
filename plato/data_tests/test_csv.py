'''
Created on Aug 9, 2015

@author: mike
'''
import unittest
import os
from plato.data.csv_input import CSVInput

class TestCSV(unittest.TestCase):


    def test_csv(self):
        cwd = os.getcwdu()
        input_file = os.path.join(cwd, 'test.csv')
        data = CSVInput(input_file).input
        self.assertEquals(len(data), 3)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()