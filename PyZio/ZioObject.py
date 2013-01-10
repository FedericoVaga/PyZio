"""
@author: Federico Vaga
@copyright: Federico Vaga 2012
@license: GPLv2
"""
import os

class ZioObject:
    """It handles a generic ZIO object. It is an abstract class"""

    def __init__(self, path, name):
        self.name = name
        self.path = path
        self.fullpath = os.path.join(self.path, self.name)
        self.attribute = {} # Dictionary for boject's attributes
        self.obj_children = [] # List of children attributes
        self.invalid_attrs = ["power", "driver", "subsystem", "uevent"]

    def is_valid_sysfs_element(self, name):
        """It returns if a sysfs name is valid or not"""
        return not name in self.invalid_attrs

    def get_name(self):
        """It returns the name of the object"""
        return self.attribute["name"].get_value()

    def is_enable(self):
        """It returns True if this object is enabled, False otherwise"""
        en = self.attribute["enable"].get_value()
        return (True if en == "1" else False)

    def enable(self):
        """It enables the object. It raise IO exception if the user cannot
        enable the object"""
        self.attribute["enable"].set_value(1)

    def disable(self):
        """It disable the object. It raise IO exception if the user cannot
        enable the object"""
        self.attribute["enable"].set_value(0)
