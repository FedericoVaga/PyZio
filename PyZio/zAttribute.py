"""
@author: Federico Vaga
@copyright: Federico Vaga 2012
@license: GPLv2
"""

import os
import sys

class zAttribute(object):
    """This class handle a single ZIO attribute. It allow only two operations:
    read and write. This class check if the attribute permission and return
    error if you are doing not permitted operations"""

    def __init__(self, path, name):
        self.name = name
        self.path = path
        self.fullPath = os.path.join(path, name)
        #print("Attribute found: " + self.fullPath)


    def isReadable(self):
        return os.access(self.fullPath, os.R_OK)

    def isWritable(self):
        return os.access(self.fullPath, os.W_OK)


    def getValue(self):
        """It reads the sysfs file of the attribute and it returns the value"""

        with open(self.fullPath, "r") as f:
            try:
                return f.read().rstrip("\n\r")
            except IOError as e:
                print("I/O error({0}): {1}".format(e.errno, e.strerror))
            except:
                print("Unexpected error:", sys.exc_info()[0])
                raise

    def setValue(self, val):
        """It writes the sysfs attribute with val."""

        w = str(val)
        with open(self.fullPath, "w") as f:
            try:
                f.write(w)
            except IOError as e:
                print("I/O error({0}): {1}".format(e.errno, e.strerror))
            except:
                print("Unexpected error:", sys.exc_info()[0])
                raise
