"""
@author: Federico Vaga
@copyright: Federico Vaga 2012
@license: GPLv2
"""
import os

from .zObject import zObject
from .zAttribute import zAttribute

class zTrig(object, zObject):
    """zChan class describe the zio_channel object from the ZIO framework. It
    inherits from zObject"""

    def __init__(self, path, name):
        """Constructor for zTrig class. It calls the __init__ function
        from zObject for a generic initialization; then it looks for attributes
        in its directory"""
        zObject.__init__(self, path, name)
        # Inspect all files and directory
        for el in os.listdir(self.fullPath):
            # Skip if the element it is not valid
            if not self.isValidSysfsAttribute(el):
                continue
            # All the valid element are attributes
            self.attribute[el] = zAttribute(self.fullPath, el)
