"""
@author: Federico Vaga
@copyright: Federico Vaga 2012
@license: GPLv2
"""
import os

from PyZio.ZioObject import ZioObject
from PyZio.ZioAttribute import ZioAttribute
from PyZio.ZioChan import ZioChan
from PyZio.ZioTrig import ZioTrig


class ZioCset(object, ZioObject):
    """zCset class describe the zio_cset object from the ZIO framework. It
    inherits from zObject"""

    def __init__(self, path, name):
        """It calls the __init__ function from zObject for a generic
        initialization; then it looks for attributes, channels and trigger in
        its directory. Valid directory are channels except the 'trigger'
        directory; all valid files are attributes. The list of children object
        is made of trigger and channels."""
        ZioObject.__init__(self, path, name) # Initialize zObject
        self.chan = [] # List of channel children
        self.trigger = None # Associated trigger
        self.interleave = None # Interleaved channel

        for el in os.listdir(self.fullpath):
            if not self.is_valid_sysfs_element(el): # Skip if invalid element
                continue
            if el == "trigger" and os.path.isdir(os.path.join(self.fullpath, el)):
                self.trigger = ZioTrig(self.fullpath, el)
                continue

            if os.path.isdir(os.path.join(self.fullpath, el)): # Subdir is a channel
                newchan = ZioChan(self.fullpath, el)
                self.chan.append(newchan)
                if el == "chani":
                    self.interleave = newchan
            else: # otherwise is an attribute
                self.attribute[el] = ZioAttribute(self.fullpath, el)

        # Update the zObject children list
        self.obj_children.append(self.trigger)
        self.obj_children.extend(self.chan)

    def is_interleaved(self):
        """It returns True is the cset is interleave capable"""
        return False if self.interleave == None else True

    def get_current_buffer(self):
        """It returns the current buffer for all channels within this device"""
        return self.attribute["current_buffer"].get_value()

    def set_current_buffer(self, buftype):
        """It sets the current buffer for all channels within this cset. Then
        update the buffer for each channel"""
        self.attribute["current_buffer"].set_value(buftype)
        for chan in self.chan:
            chan.update_buffer();

    def get_current_trigger(self):
        """It returns a string with the current trigger name"""
        return self.attribute["current_trigger"].get_value()

    def set_current_trigger(self, trigtype):
        """It sets the current trigger for this cset. and change the trigger
        instance"""
        self.attribute["current_trigger"].set_value(trigtype)
        fullpath = self.trigger.path;
        self.trigger = ZioTrig(fullpath, "trigger")