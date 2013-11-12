"""
@author: Federico Vaga
@copyright: Federico Vaga 2012
@license: GPLv2
"""
import os
from os.path import join, isdir
from PyZio.ZioObject import ZioObject
from PyZio.ZioAttribute import ZioAttribute
from PyZio.ZioCset import ZioCset

class ZioDev(ZioObject):
    """It describes the zio_device object from the ZIO framework. It
    inherits from zObject"""

    def __init__(self, path, name):
        """It calls the __init__ function from zObject for a generic
        initialization; then it looks for attributes and csets in its
        directory. All valid directory are csets, and all valid files are
        attributes. The list of object children is equal to the list of channel
        set"""
        ZioObject.__init__(self, path, name)
        self.cset = [] # List of children cset
        for tmp in os.listdir(self.fullpath):
            if not self.is_valid_sysfs_element(tmp): # Skip if invalid element
                continue
            if isdir(join(self.fullpath, tmp)): # Subdirs are csets
                newcset = ZioCset(self.fullpath, tmp)
                self.cset.append(newcset)
            else: # otherwise is an attribute
                self.attribute[tmp] = ZioAttribute(self.fullpath, tmp)

        self.obj_children.extend(self.cset) # Update the zObject children list
