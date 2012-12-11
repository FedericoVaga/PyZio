"""
@author: Federico Vaga
@copyright: Federico Vaga 2012
@license: GPLv2
"""
import os
import errno

from .zObject import zObject
from .zAttribute import zAttribute
from .zBuf import zBuf
from .zCtrl import zCtrl
from .zCharDevice import zCharDevice

class zChan(object, zObject):
    """zChan class describe the zio_channel object from the ZIO framework. It
    inherits from zObject"""

    def __init__(self, path, name):
        """Constructor for zChan class. It calls the __init__ function
        from zObject for a generic initialization; then it looks for attributes
        and buffer in its directory"""
        zObject.__init__(self, path, name)
        self.currCtrl = None
        self.buffer = None
        self.interfaceType = None

        # Inspect all files and directory
        for el in os.listdir(self.fullPath):
            # Skip if the element it is not valid
            if not self.isValidSysfsElement(el):
                continue
            # If the element is "buffer" then create a zBuf instance
            if el == "buffer":
                self.buffer = zBuf(self.fullPath, el)
                continue
            # If the element is "current_control" then create a zCtrl instance
            if el == "current_control":
                self.curctrl = zCtrl(os.path.join(self.fullPath, el))
                continue
            if el == "zio-cdev":
                self.interfaceType = "cdev" # Init later, we need attributes
                continue
            # Otherwise it is a generic attribute
            newAttr = zAttribute(self.fullPath, el)
            self.attribute[el] = newAttr

        # Update the zObject children list
        self.obj_children.append(self.buffer)
        if self.interfaceType == None:
            print("No interface available for " + self.fullPath)
        elif self.interfaceType == "cdev":
            # Set the interface to use (at the moment only Char Device)
            self.interface = zCharDevice(self)
        elif self.interfaceType == "socket":
            pass

    def isInterleaved(self):
        return True if self.name == "chani" else False

    def updateBuffer(self):
        """It updates the buffer object for this channel. If user change the
        current buffer from cset, then channel instance of the buffer must be
        updated"""
        self.buffer = zBuf(self.fullPath, "buffer")


    def getCurrentCtrl(self):
        """It gets the current control. It is only a wrapper of the setCtrl
        method of zCtrl; user can use directly that method"""
        self.currCtrl.getCtrl()

    def setCurrentCtrl(self):
        """It set the current control. User should edit self.currCtrl before
        call this function."""
        if self.currCtrl.isValid():
            self.currCtrl.setCtrl()
        return -errno.EINVAL

