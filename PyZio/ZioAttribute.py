"""
@author: Federico Vaga
@copyright: Federico Vaga 2012
@license: GPLv2
"""
from PyZio.ZioUtil import is_readable, is_writable
import os

class ZioAttribute:
    """
    This class handle a single ZIO attribute. It allow only two operations:
    read and write. All methods do not handle exception, so the pass to higher
    class that must handle errors.
    """

    def __init__(self, path, name):
        self.name = name
        self.path = path
        self.fullpath = os.path.join(path, name)

    def is_readable(self):
        """
        It returns if the attribute is readable
        """
        return is_readable(self.fullpath)

    def is_writable(self):
        """
        It returns if the attributes is writable
        """
        return is_writable(self.fullpath)

    def get_value(self):
        """
        It reads the sysfs file of the attribute and it returns the value
        """
        with open(self.fullpath, "r") as f:
            return f.read().rstrip("\n\r")

    def set_value(self, val):
        """
        It writes the sysfs attribute with val.
        """
        with open(self.fullpath, "w") as f:
            f.write(str(val))

