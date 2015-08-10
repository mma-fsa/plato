'''
Created on Aug 9, 2015

@author: mike
'''
from plato.data.csv_input import CSVInput
from plato_alm.asset.bond.bond_cashflow import BondCashflow
from plato.core.input_reader import InputReader
from plato.core.submodel import SubmodelArray

class AssetModel(object):

    def __init__(self, config):
        self.__config = config
        self.__bonds = None
    
    @SubmodelArray
    @InputReader(input_type=CSVInput, obj_type=BondCashflow)
    def bond_input(self):
        pass
    
    