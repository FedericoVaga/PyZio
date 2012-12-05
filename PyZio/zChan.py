"""
@author: Federico Vaga
@copyright: Federico Vaga 2012
@license: GPLv2
"""
import os
import copy
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

        # Inspect all files and directory
        for el in os.listdir(self.fullPath):
            # Skip if the element it is not valid
            if not self.isValidSysfsAttribute(el):
                continue
            # If the element is "buffer" then create a zBuf instance
            if el == "buffer":
                self.buffer = zBuf(self.fullPath, el)
                continue
            # If the element is "current_control" then create a zCtrl instance
            if el == "current_control":
                self.curctrl = zCtrl(os.path.join(self.fullPath, el))
                continue
            # Otherwise it is a generic attribute
            newAttr = zAttribute(self.fullPath, el)
            self.attribute[el] = newAttr

        self.interface = zCharDevice(self)
        pass

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


    def readData(self, updateCtrl, unpackData):
        """If the channel is enabled, it reads data from the device"""
        if self.isEnable():
            return self.interface.readData()
        return -errno.EPERM

    def writeData(self, data):
        """If the channel is enabled, it writes data to the device"""
        if self.isEnable():
            self.interface.writeData(data)
        return -errno.EPERM

    def readCtrl(self, updateCtrl, unpackData):
        """If the channel is enabled, it reads data from the device"""
        if self.isEnable():
            return self.interface.readCtrl()

    def writeCtrl(self, ctrl):
        """If the channel is enabled, it writes data to the device"""
        if self.isEnable():
            self.interface.writeCtrl(ctrl)
