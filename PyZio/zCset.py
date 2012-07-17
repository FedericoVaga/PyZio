"""
@author: Federico Vaga
@copyright: Federico Vaga 2012
@license: GPLv2
"""
import os

from .zObject import zObject
from .zAttribute import zAttribute
from .zChan import zChan
from .zTrig import zTrig

class zCset(object, zObject):
    """This class describe the zio_cset object from the ZIO framework"""

    def __init__(self, path, name):
        """
        - set up name and patch of cset in sysfs tree
        - retrieve cset attributes
        - retrieve cset's channels
        - retrieve trigger
        """
        zObject.__init__(self, path, name)
        self.chan = [] # list of channels child
        self.trigger = None
        
        for el in os.listdir(self.fullPath):
            if not self.isValidSysfsAttribute(el):
                continue
            
            if el == "trigger":
                self.trigger = zTrig(self.fullPath, el)
                continue
            
            if os.path.isdir(os.path.join(self.fullPath, el)):
                # if a sysfs element is a directory, then is a channel
                newChan = zChan(self.fullPath, el)
                self.chan.append(newChan)
            else:
                # otherwise is an attribute
                newAttr = zAttribute(self.fullPath, el)
                self.attribute[el] = newAttr
    
    def refreshAttributes(self):
        """update the value of all cset attribute"""
        self.updateAttributes()
        self.__updateChildrenAttributes(self.chan)
        self.__updateChildrenAttributes(self.trigger)
        pass
    
    def getCurrentBuffer(self):
        """get the current buffer for all channels within this device"""
        return self.attribute["current_buffer"].read()
    
    def setCurrentBuffer(self, bufType):
        """set the current buffer for all channels within this device"""
        self.attribute["current_buffer"].write(bufType)
        for chan in self.chan:
            chan.updateBuffer();
    
    def getCurrentTrigger(self):
        """get the current trigger for this cset"""
        return self.attribute["current_trigger"].read()
    
    def setCurrentTrigger(self, trigType):
        """Set the current trigger for this cset"""
        self.attribute["current_trigger"].write(trigType)
        fullPath = self.trigger.path;
        self.trigger = zTrig(fullPath, "trigger")