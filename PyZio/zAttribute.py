"""
@author: Federico Vaga
@copyright: Federico Vaga 2012
@license: GPL
"""

import os

class zAttribute(object):
    def __init__(self, path, name):
        self.name = name
        self.path = path
        self.fullPath = os.path.join(path, name)
        self .value = self.__read(self.fullPath)
        
        self.readable = True if os.access(self.fullPath, os.R_OK) else False
        self.writable = True if os.access(self.fullPath, os.W_OK) else False
        pass
    
    def read(self):
        self.value = self.__read(os.path.join(self.path, self.name))
        return self.value
        pass
    
    def write(self, val):
        err = self.__write(os.path.join(self.path, self.name), val)
        if err != -1:
            self.value = val
        pass
    
    def __read(self, path):
        f = open(path, "r")
        val = f.read().rstrip("\n\r")
        f.close()
        return val
    
    def __write(self, path, val):
        w = str(val)
        f = open(path, "w")
        f.write(w)
        self.read()
        pass