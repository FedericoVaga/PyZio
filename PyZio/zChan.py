"""
@author: Federico Vaga
@copyright: Federico Vaga 2012
@license: GPLv2
"""
import os
from stat import ST_MODE

from .zObject import zObject
from .zAttribute import zAttribute
from .zBuf import zBuf
from .zCtrl import zCtrl
from .zData import zData
from .zConfig import zio_cdev_path

class zChan(object, zObject):
    '''
    Constructor
    - set up name and patch of cset in sysfs tree
    - retrieve channel attributes
    - retrieve buffer
    '''
    def __init__(self, path, name):
        zObject.__init__(self, path, name)
        self.curctrl = None
        self.buffer = None
        
        cdev_prefix = ""
        for el in os.listdir(self.fullPath):
            if not self.isValidSysfsAttribute(el):
                continue
            
            if el == "buffer":
                self.buffer = zBuf(self.fullPath, el)
                continue
            
            if el == "current_control":
                self.curctrl = zCtrl(self.fullPath, el)
                continue
            
            newAttr = zAttribute(self.fullPath, el)
            self.attribute[el] = newAttr
            
            # this is for char device interface
            if el == "cdev_prefix":
                cdev_prefix = newAttr.read()
        
        # the following for the char device interface
        # Set if this channel is for input or output
        zmode = oct(os.stat(zio_cdev_path + cdev_prefix + "ctrl")\
                    [ST_MODE])[-3:]
        self.isOutput = True if zmode == 222 else False
        # Set source for control and data
        self.ctrlcdev = zCtrl(zio_cdev_path, cdev_prefix + "ctrl")
        self.datacdev = zData(zio_cdev_path, cdev_prefix + "data", \
                              self.ctrlcdev)
        pass
    
    def refreshAttributes(self):
        self.updateAttributes()
        self.__updateChildrenAttributes(self.buffer)
        pass
    
    def updateBuffer(self):
        """It updates the buffer object for this channel. If user change the
        current buffer from cset, all the buffer instance within channels must
        be update"""
        self.buffer = zBuf(self.fullPath, "buffer")
        pass
    
    def pullData(self, updateCtrl, unpackData):
        """It pulls data from the device. At the moment only char device
        interface is supported"""
        if self.isEnable():
            return self.datacdev.readData(updateCtrl, unpackData)
        return None
        pass
    
    def pushData(self):
        """It pushes data to the device. At the moment only char device
        interface is supported"""
        if self.isEnable():
            self.datacdev.writeData()
        pass