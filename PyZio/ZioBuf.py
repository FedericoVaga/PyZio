"""
@author: Federico Vaga
@copyright: Federico Vaga 2012
@license: GPLv2
"""
import os

from PyZio.ZioObject import ZioObject
from PyZio.ZioAttribute import ZioAttribute

class ZioBuf(ZioObject):
    """This class describe the zio_bi object from the ZIO framework. It
    inherits from zObject"""

    def __init__(self, path, name):
        """It calls the __init__ functionfrom zObject for a generic
        initialization; then it looks for attributes in its directory: all
        valid files within its directory are buffers's attributes"""
        ZioObject.__init__(self, path, name)
        self.__flush_attr = None
        # Inspect all files and directory
        for tmp in os.listdir(self.fullpath):
            # Skip if the element it is not valid
            if not self.is_valid_sysfs_element(tmp):
                continue
            # All the valid element are attributes
            self.attribute[tmp] = ZioAttribute(self.fullpath, tmp)

    def flush(self):
        """
        It does 'flush' on the buffer
        """
        if "flush" in self.attribute:
            self.attribute["flush"].set_value(1)
