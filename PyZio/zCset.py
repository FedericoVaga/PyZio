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

'''
This class describe the zio_cset object from the ZIO framework
'''
class zCset(object, zObject):
    '''
    - set up name and patch of cset in sysfs tree
    - retrieve cset attributes
    - retrieve cset's channels
    - retrieve trigger
    '''
    def __init__(self, path, name):
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
        
        # Creates the list of cset children
        self.obj_children.append(self.trigger)
        self.obj_children.extend(self.chan)
    
    
    '''
    getCurrentBuffer
    It returns the current buffer for all channels within this device
    '''
    def getCurrentBuffer(self):
        return self.attribute["current_buffer"].read()

    '''
    setCurrentBuffer
    It sets the current buffer for all channels within this cset. Then update
    the buffer for each channel
    '''
    def setCurrentBuffer(self, bufType):
        self.attribute["current_buffer"].write(bufType)
        for chan in self.chan:
            chan.updateBuffer();

    '''
    getCurrentTrigger
    It returns a string with the current trigger name
    '''
    def getCurrentTrigger(self):
        return self.attribute["current_trigger"].read()

    '''
    setCurrentTrigger
    It sets the current trigger for this cset.
    '''
    def setCurrentTrigger(self, trigType):
        self.attribute["current_trigger"].write(trigType)
        fullPath = self.trigger.path;
        self.trigger = zTrig(fullPath, "trigger")