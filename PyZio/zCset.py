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
    """zCset class describe the zio_cset object from the ZIO framework. It
    inherits from zObject"""

    def __init__(self, path, name):
        """Constructor for zCset class. It calls the __init__ function
        from zObject for a generic initialization; then it looks for attributes,
        channels and trigger in its directory"""
        zObject.__init__(self, path, name)
        # List of channel children
        self.chan = []
        # Associated trigger
        self.trigger = None
        # Look into directory for channels and attributes
        for el in os.listdir(self.fullPath):
            # Skip if invalid element
            if not self.isValidSysfsAttribute(el):
                continue
            # If the element is "trigger", then create a trigger instance and
            # continue to the next element
            if el == "trigger":
                self.trigger = zTrig(self.fullPath, el)
                continue
            # if a sysfs element is a directory, then is a channel
            if os.path.isdir(os.path.join(self.fullPath, el)):
                newChan = zChan(self.fullPath, el)
                self.chan.append(newChan)
            # otherwise is an attribute
            else:
                self.attribute[el] = zAttribute(self.fullPath, el)

        # Update the zObject children list
        self.obj_children.append(self.trigger)
        self.obj_children.extend(self.chan)

    def getCurrentBuffer(self):
        """It returns the current buffer for all channels within this device"""
        return self.attribute["current_buffer"].read()

    def setCurrentBuffer(self, bufType):
        """It sets the current buffer for all channels within this cset. Then
        update the buffer for each channel"""
        self.attribute["current_buffer"].write(bufType)
        for chan in self.chan:
            chan.updateBuffer();

    def getCurrentTrigger(self):
        """It returns a string with the current trigger name"""
        return self.attribute["current_trigger"].read()

    def setCurrentTrigger(self, trigType):
        """It sets the current trigger for this cset. and change the trigger
        instance"""
        self.attribute["current_trigger"].write(trigType)
        fullPath = self.trigger.path;
        self.trigger = zTrig(fullPath, "trigger")
