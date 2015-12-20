'''
Created on Aug 9, 2015

@author: mike
'''
import xml.etree.ElementTree as ET

class ConfigReader(object):
    def __init__(self, filename):
        self.filename = filename
        self.__config = None
    
    def __read_config(self, filename):
        import os
        tree = ET.parse(filename)
        root = tree.getroot()
        paths = {}
        for path_group in root.iter('pathGroup'):
            root_path = path_group.attrib['path']
            for path in path_group.iter('path'):
                key = path.attrib['key']
                subpath = path.attrib['subpath']                
                paths[key]= os.path.join(root_path, subpath)
        return paths
    
    @property
    def config(self):
        if not self.__config:
            self.__config = self.__read_config(self.filename)
        return self.__config
    