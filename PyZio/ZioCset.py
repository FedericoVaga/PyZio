"""
@author: Federico Vaga
@copyright: Federico Vaga 2012
@license: GPLv2
"""
import os
from os.path import join, isdir
from PyZio.ZioObject import ZioObject
from PyZio.ZioAttribute import ZioAttribute
from PyZio.ZioChan import ZioChan
from PyZio.ZioTrig import ZioTrig
from PyZio.ZioError import ZioMissingAttribute


class ZioCset(ZioObject):
    """
    ZioCset class describe the zio_cset object from the ZIO framework.
    """

    def __init__(self, path, name):
        """
        It calls the __init__ function from ZioObject for a generic
        initialization; then it looks for attributes, channels and trigger in
        its directory. Valid directory are channels except the 'trigger'
        directory; all valid files are attributes. The list of children object
        is made of trigger and channels.
        """
        ZioObject.__init__(self, path, name) # Initialize zObject
        self.chan = [] # List of channel children
        self.trigger = None # Associated trigger
        self.interleave = None # Interleaved channel

        for tmp in os.listdir(self.fullpath):
            if not self.is_valid_sysfs_element(tmp): # Skip if invalid element
                continue
            if tmp == "trigger" and isdir(join(self.fullpath, tmp)):
                self.trigger = ZioTrig(self.fullpath, tmp)
                continue

            if isdir(join(self.fullpath, tmp)): # Subdir is a channel
                newchan = ZioChan(self.fullpath, tmp)
                self.chan.append(newchan)
                if tmp == "chani":
                    self.interleave = newchan
            else: # otherwise is an attribute
                self.attribute[tmp] = ZioAttribute(self.fullpath, tmp)

        # Update the zObject children list
        self.obj_children.append(self.trigger)
        self.obj_children.extend(self.chan)

    def is_interleaved(self):
        """
        It returns True is the cset is interleave capable
        """
        return False if self.interleave == None else True

    def get_current_buffer(self):
        """
        It returns the current buffer for all channels within this device
        """
        if not "current_buffer" in self.attribute:
            raise ZioMissingAttribute("current_buffer")

        return self.attribute["current_buffer"].get_value()

    def set_current_buffer(self, buftype):
        """
        It sets the current buffer for all channels within this cset. Then
        update the buffer for each channel
        """
        if not "current_buffer" in self.attribute:
            raise ZioMissingAttribute("current_buffer")

        self.attribute["current_buffer"].set_value(buftype)
        for chan in self.chan:
            chan.update_buffer()

    def get_current_trigger(self):
        """
        It returns a string with the current trigger name
        """
        if not "current_trigger" in self.attribute:
            raise ZioMissingAttribute("current_trigger")

        return self.attribute["current_trigger"].get_value()

    def set_current_trigger(self, trigtype):
        """
        It sets the current trigger for this cset. and change the trigger
        instance
        """
        if not "current_trigger" in self.attribute:
            raise ZioMissingAttribute("current_trigger")

        self.attribute["current_trigger"].set_value(trigtype)
        fullpath = self.trigger.path
        self.trigger = ZioTrig(fullpath, "trigger")
