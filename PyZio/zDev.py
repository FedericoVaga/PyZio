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
    """zDev class describe the zio_device object from the ZIO framework. It
    inherits from zObject"""

    def __init__(self, path, name):
        """Constructor for zDev class. It calls the __init__ function
        from zObject for a generic initialization; then it looks for attributes
        and csets in its directory"""

        # Generic initialization
        zObject.__init__(self, path, name)
        # list of cset children
        self.cset = []
        # Look into directory for cset and attributes
        for el in os.listdir(self.fullPath):
            # Skip if invalid element
            if not self.isValidSysfsElement(el):
                continue

            # if a valid sysfs element is a directory, then it is a cset
            if os.path.isdir(os.path.join(self.fullPath, el)):
                newCset = zCset(self.fullPath, el)
                self.cset.append(newCset)
            # otherwise is an attribute
            else:
                self.attribute[el] = zAttribute(self.fullPath, el)

        # Update the zObject children list
        self.obj_children.extend(self.cset)
