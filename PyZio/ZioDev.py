"""
@author: Federico Vaga
@copyright: Federico Vaga 2012
@license: GPLv2
"""
import os

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
        for el in os.listdir(self.fullpath):
            if not self.is_valid_sysfs_element(el): # Skip if invalid element
                continue
            if os.path.isdir(os.path.join(self.fullpath, el)): # Subdirs are csets
                newcset = ZioCset(self.fullpath, el)
                self.cset.append(newcset)
            else: # otherwise is an attribute
                self.attribute[el] = ZioAttribute(self.fullpath, el)

        self.obj_children.extend(self.cset) # Update the zObject children list
