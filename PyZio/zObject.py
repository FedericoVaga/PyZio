"""
@author: Federico Vaga
@copyright: Federico Vaga 2012
@license: GPLv2
"""

import os

'''
zObject
This class handle a generic object. It is an abstract class
'''
class zObject():
    def __init__(self, path, name):
        self.name = name
        self.path = path
        self.fullPath = os.path.join(self.path, self.name)
        self.attribute = {} # dictionary for attributes
        self.obj_children = []
        self.invalidAttributes = ["power", "driver", "subsystem", "uevent"]
        pass

    '''
    isValidSysfsAttribute
    It returns if a sysfs name is valid or not
    '''
    def isValidSysfsAttribute(self, name):
        for a in self.invalidAttributes:
            if name == a:
                return False
        return True

    '''
    updateAttributes
    It updates the attributes within this object
    '''
    def updateAttributes(self):
        for attr in self.attribute:
            self.attribute[attr].read()
        pass
    
    '''
    updateChildrenAttributes
    It updates the attributes within the children of this object
    '''
    def updateChildrenAttributes(self):
        for child in self.obj_children:
            child.updateAttributes()
        pass
    
    '''
    updateAllAttributes
    It updates the attributes within this object and all attributes in the
    children objects
    '''
    def updateAllAttributes(self):
        self.updateAttributes()
        self.updateChildrenAttributes()
        pass

    '''
    getName
    It returns the name of the object
    '''
    def getName(self):
        return self.attribute["name"].read()

    '''
    isEnable
    It returns True if this object is enabled, False otherwise
    '''
    def isEnable(self):
        en = self.attribute["enable"].read()
        return (True if en == "1" else False)

    '''
    enable
    It enables the object.
    '''
    def enable(self):
        self.attribute["enable"].write("1")
        pass

    '''
    disable
    It disable the object.
    '''
    def disable(self):
        self.attribute["enable"].write("0")
        pass
