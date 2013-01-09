"""
@author: Federico Vaga <federico.vaga@gmail.com>
@copyright: Federico Vaga 2012
@license: GPLv2
"""

import os
import struct

from .zInterface import zInterface
from .zCtrl import zCtrl

class zCharDevice(object, zInterface):
    """This class represent the Char Device interface of ZIO. It has to char
    device: one for control and one for data. The have both the same file
    permission."""
    def __init__(self, zObj):
        """Initialize zCharDevice class. zObj is the object which use this interface"""
        zInterface.__init__(self, zObj)

        # Set data and ctrl char devices
        self.ctrlFile = os.path.join(self.zio_interface_path, \
                                     self.interface_prefix + "-ctrl")
        self.dataFile = os.path.join(self.zio_interface_path, \
                                     self.interface_prefix + "-data")

        self.lastCtrl = None
        # Options
        self.cfgEnable = True
        self.cfgUnpackData = True
        pass

    def setUnpackData(self, status):
        self.cfgUnpackData = status

    def enable(self):
        """It enables char device read/write."""
        self.cfgEnable = True

    def disable(self):
        """It disable char device read/write."""
        self.cfgEnable = False

    def isUnpackData(self, status):
        return self.cfgUnpackData

    def isEnable(self):
        return self.cfgEnable


    def isInput(self):
        return os.access(self.ctrlFile, os.R_OK)

    def isOutput(self):
        return os.access(self.ctrlFile, os.W_OK)


    def readBlock(self, rCtrl, rData):
        """It read the control and the samples of a block from char devices.
        It stores the last control in self.lastCtrl"""

        ctrl = None
        samples = None
        if self.isInput() and self.zObj.isEnable():

            if rCtrl: # Read the control
                fd = os.open(self.ctrlFile, os.O_RDONLY)
                binCtrl = os.read(fd, 512)
                os.close(fd)
                ctrl = zCtrl()
                self.lastCtrl = ctrl
                ctrl.unpackToCtrl(binCtrl)

            if rData: # Read the data
                if ctrl == None:
                    if self.lastCtrl == None:
                        print("WARNING: you never read control, then only 16byte will be read")
                        tmpctrl = zCtrl()
                        tmpctrl.ssize = 1
                        tmpctrl.nsamples = 16
                    else:
                        tmpctrl = self.lastCtrl
                else:
                    tmpctrl = ctrl
                fd = os.open(self.dataFile, os.O_RDONLY)
                data_tmp = os.read(fd, tmpctrl.ssize * tmpctrl.nsamples)
                os.close(fd)
                if self.cfgUnpackData:
                    samples =  self.__unpack_data(data_tmp, tmpctrl.nsamples, tmpctrl.ssize)

        return ctrl, samples

    def writeBlock(self, ctrl, samples):
        """It writes the control and the samples of this class to the char
        device. User should edit ctrl and samples before write"""
        if self.isOutput() and self.zObj.isEnable():
            if isinstance(ctrl, zCtrl):
                fd = os.open(self.ctrlFile, os.O_WRONLY)
                os.write(fd, ctrl.packToBin())
                os.close(fd)
            if samples != None:
                fd = os.open(self.dataFile, os.O_WRONLY)
                os.write(fd, samples)
                os.close(fd)


    # # # # # PRIVATE FUNCTIONS # # # # #
    def __unpack_data(self, data, nsamples, ssize):
        """It unpacks data in a list of nsampples elements"""
        fmt = "b"
        if ssize == 1:
            fmt = "B"
        elif ssize == 2:
            fmt = "H"
        elif ssize == 4:
            fmt = "I"
        elif ssize == 8:
            fmt = "Q"
        return struct.unpack((str(nsamples) + fmt), data)
