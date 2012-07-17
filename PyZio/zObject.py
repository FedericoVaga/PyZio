"""
@author: Federico Vaga
@copyright: Federico Vaga 2012
@license: GPLv2
"""

import os

class zObject():
    """Abstract class for all the zio object object"""
    def __init__(self, path, name):
        self.name = name
        self.path = path
        self.fullPath = os.path.join(self.path, self.name)
        self.attribute = {} # dictionary for attributes
        pass
    
    def isValidSysfsAttribute(self, name):
        """It verifies if name is a valid ZIO attribute name"""
        if name == "power" or name == "driver" or \
           name == "subsystem" or name == "uevent":
            # system sysfs attribute are invalid zio attribute
            return False
        return True
    
    def updateAttributes(self):
        """It updates the value of all device attributes"""
        for attr in self.attribute:
            self.attribute[attr].read()
        pass
    
    def __updateChildrenAttributes(self, children):
        """It updates the attributes of childern zObject"""
        for child in children:
            child.updateAttributes()
        pass
    
    def getName(self):
        """It returns the name of the zio object"""
        return self.attribute["name"].read()
    
    def isEnable(self):
        """It returns True if this zio device is enabled, False otherwise"""
        en = self.attribute["enable"].read()
        return (True if en == "1" else False)
    
    def enable(self):
        """It enables this zio device"""
        self.attribute["enable"].write("1")
        pass
    
    def disable(self):
        """It disables this zio device"""
        self.attribute["enable"].write("0")
        pass
