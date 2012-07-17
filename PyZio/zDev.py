"""
@author: Federico Vaga
@copyright: Federico Vaga 2012
@license: GPLv2
"""
import os

from .zObject import zObject
from .zAttribute import zAttribute
from .zCset import zCset

class zDev(object, zObject):
    """zDev class describe the zio_device object from the ZIO framework"""
    
    def __init__(self, path, name):
        zObject.__init__(self, path, name)
        self.cset = [] # list of csets child
        
        for el in os.listdir(self.fullPath):
            if not self.isValidSysfsAttribute(el):
                continue
            
            if os.path.isdir(os.path.join(self.fullPath, el)):
                # if a sysfs element is a directory, then is a cset
                newCset = zCset(self.fullPath, el)
                self.cset.append(newCset)
            else:
                # otherwise is an attribute
                newAttr = zAttribute(self.fullPath, el)
                self.attribute[el] = newAttr
        pass
    
    def refreshAttributes(self):
        self.updateAttributes()
        self.__updateChildrenAttributes(self.cset)
        pass