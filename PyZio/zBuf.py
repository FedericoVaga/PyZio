"""
@author: Federico Vaga
@copyright: Federico Vaga 2012
@license: GPL
"""
import os

from .zObject import zObject
from .zAttribute import zAttribute

class zBuf(object, zObject):
    """This class describe the zio_bi object from the ZIO framework"""
    def __init__(self, path, name):
        zObject.__init__(self, path, name)
        
        for el in os.listdir(self.fullPath):
            if not self.isValidSysfsAttribute(el):
                continue
            
            newAttr = zAttribute(self.fullPath, el)
            self.attribute[el] = newAttr
        pass
