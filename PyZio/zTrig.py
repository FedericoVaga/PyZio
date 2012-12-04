"""
@author: Federico Vaga
@copyright: Federico Vaga 2012
@license: GPLv2
"""
import os

from .zObject import zObject
from .zAttribute import zAttribute

'''
This class describe the zio trigger object
'''
class zTrig(object, zObject):
    def __init__(self, path, name):
        zObject.__init__(self, path, name)
        
        for el in os.listdir(self.fullPath):
            if not self.isValidSysfsAttribute(el):
                continue
            newAttr = zAttribute(self.fullPath, el)
            self.attribute[el] = newAttr
