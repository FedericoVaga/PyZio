"""
@author: Federico Vaga
@copyright: Federico Vaga 2012
@license: GPLv2
"""

import os

class zObject():
    """This class handle a generic ZIO object. It is an abstract class"""
    def __init__(self, path, name):
        self.name = name
        self.path = path
        self.fullPath = os.path.join(self.path, self.name)
        self.attribute = {} # dictionary for attributes
        self.obj_children = []
        self.invalidAttributes = ["power", "driver", "subsystem", "uevent"]
        print("Object found: " + self.fullPath)

    def isValidSysfsElement(self, name):
        """It returns if a sysfs name is valid or not"""
        for a in self.invalidAttributes:
            if name == a:
                return False
        return True


    def updateAttributes(self):
        """It updates the attributes within this object"""
        for attr in self.attribute:
            self.attribute[attr].getValue()

    def updateChildrenAttributes(self):
        """It updates the attributes within the children of this object"""
        for child in self.obj_children:
            child.updateAttributes()

    def updateAllAttributes(self):
        """It updates the attributes within this object and all attributes in the
        children objects"""
        self.updateAttributes()
        self.updateChildrenAttributes()


    def getName(self):
        """It returns the name of the object"""
        return self.attribute["name"].getValue()


    def isEnable(self):
        """It returns True if this object is enabled, False otherwise"""
        en = self.attribute["enable"].getValue()
        return (True if en == "1" else False)

    def enable(self):
        """It enables the object."""
        self.attribute["enable"].setValue("1")

    def disable(self):
        """It disable the object."""
        self.attribute["enable"].setValue("0")
