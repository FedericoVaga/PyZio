"""
@author: Federico Vaga
@copyright: Federico Vaga 2012
@license: GPLv2
"""
import os, logging

class ZioObject(object):
    """
    It handles a generic ZIO object. It is an abstract class that export
    generic functions and attributes suitable for every objects.
    """

    def __init__(self, path, name):
        self.name = name
        self.path = path
        self.fullpath = os.path.join(self.path, self.name)
        self.attribute = {}     # Dictionary for boject's attributes
        self.obj_children = []  # List of children attributes
        self.invalid_attrs = ["power", "driver", "subsystem", "uevent"]

        logging.debug("new %s %s", self.__class__.__name__, self.fullpath)

    def is_valid_sysfs_element(self, name):
        """
        It returns if a sysfs name is valid or not
        """
        return not name in self.invalid_attrs

    def get_name(self):
        """
        It returns the name of the object
        """
        return self.attribute["name"].get_value()

    def is_enable(self):
        """
        It returns True if this object is enabled, False otherwise
        """
        en = self.attribute["enable"].get_value()
        return (True if en == "1" else False)


    def enable(self, status = True):
        """
        It enables the object. It raise IO exception if the user cannot
        enable the object. You can use this function also to disable an
        object by setting the optional parameter 'status' to 'False'.
        """
        val = 1 if status else 0
        self.attribute["enable"].set_value(val)

    def disable(self, status = True):
        """
        It disable the object. It raise IO exception if the user cannot
        enable the object. You can use this function also to enable an
        object by setting the optional parameter 'status' to 'True'.
        """
        val = 0 if status else 1
        self.attribute["enable"].set_value(val)
