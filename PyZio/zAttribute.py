"""
@author: Federico Vaga
@copyright: Federico Vaga 2012
@license: GPLv2
"""

import os
import sys
import errno

class zAttribute(object):
    """This class handle a single ZIO attribute. It allow only two operations:
    read and write. This class check if the attribute permission and return
    error if you are doing not permitted operations"""

    def __init__(self, path, name):
        self.name = name
        self.path = path
        self.fullPath = os.path.join(path, name)
        self.value = self.__read(self.fullPath)

        self.readable = True if os.access(self.fullPath, os.R_OK) else False
        self.writable = True if os.access(self.fullPath, os.W_OK) else False
        pass

    def getValue(self):
        """It reads the sysfs file of the attribute and it store the value in
        self.value. It returns also the read value."""
        if not self.readable:
            return -errno.EPERM

        val = self.__read(self.fullPath)
        if val >= 0:
            self.value = val
        return val

    def setValue(self, val):
        """It writes the sysfs attribute with the val parameter. If no
        error occurs, it stores the new value in self.value."""
        if not self.writable:
            return -errno.EPERM

        err = self.__write(self.fullPath, val)
        if err == 0:
            self.value = val
        return err


    def __read(self, path, val):
        """ The function read from the sysfs file a value and it returns
        immediatly. This function handle exception"""
        with open(path, "r") as f:
            try:
                val = f.read().rstrip("\n\r")
                return val
            except IOError as e:
                print("I/O error({0}): {1}".format(e.errno, e.strerror))

            except:
                print("Unexpected error:", sys.exc_info()[0])
                raise

    def __write(self, path, val):
        """The function convert the value into string and it write on the
        sysfs file. It does not matter if val is an integer or a string, this
        function always convert to string before writing. This function handle
        the exception."""
        w = str(val)
        with open(path, "w") as f:
            try:
                f.write(w)
            except IOError as e:
                print("I/O error({0}): {1}".format(e.errno, e.strerror))
                return -e.errno
            except:
                print("Unexpected error:", sys.exc_info()[0])
                return -2
        #self.read() # Theorically useless
        return 0
