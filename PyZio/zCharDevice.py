"""
@author: Federico Vaga
@copyright: Federico Vaga 2012
@license: GPLv2
"""

import os
import sys
import struct

from .zInterface import zInterface
from .zCtrl import zCtrl

class zCharDevice(object, zInterface):
    """This class represent the Char Device interface of ZIO. It has to char
    device: one for control and one for data. The have both the same file
    permission."""
    def __init__(self, zObj):
        zInterface.__init__(self, zObj)

        # Set data and ctrl char devices
        self.ctrlFile = os.path.join(self.zio_interface_path, \
                                     self.interface_prefix + "-ctrl")
        self.dataFile = os.path.join(self.zio_interface_path, \
                                     self.interface_prefix + "-data")
        # Block
        self.samples = None
        self.ctrl = None

        # Options
        self.cfgEnable = True
        self.cfgCtrlEnable = True
        self.cfgDataEnable = True
        self.cfgUnpackData = True
        pass

    def setCtrlEnable(self, status):
        self.cfgCtrlEnable = status

    def setDataEnable(self, status):
        self.cfgDataEnable = status

    def setUnpackData(self, status):
        self.cfgUnpackData = status

    def enable(self):
        """It enables char device read/write."""
        self.cfgEnable = True

    def disable(self):
        """It disable char device read/write."""
        self.cfgEnable = False

    def isCtrlEnable(self, status):
        return self.cfgCtrlEnable

    def isDataEnable(self, status):
        return self.cfgDataEnable

    def isUnpackData(self, status):
        return self.cfgUnpackData

    def isEnable(self):
        return self.cfgEnable

    def setSamples(self, samples):
        """It sets the samples for the next write"""
        if os.access(self.dataFile, os.W_OK):
            self.samples = samples

    def getSamples(self):
        """It returns the samples stored since the last read"""
        if os.access(self.dataFile, os.R_OK):
            return self.samples
        return None

    def setControl(self, ctrl):
        """It sets the control for the next write"""
        if os.access(self.ctrlFile, os.W_OK):
            if ctrl.isValid():
                self.ctrl = ctrl

    def getControl(self):
        """It returns a reference to the control class. The control class is
        filled with value from the last read"""
        if os.access(self.ctrlFile, os.R_OK):
            return self.ctrl
        return None


    def readBlock(self):
        """It read the control and the samples of a block from char devices.
        It stores the block in self.ctrl and self.samples"""

        if os.access(self.ctrlFile, os.R_OK) and self.zObj.isEnable():
            size = 0 #FIXME
            if self.cfgCtrlEnable:
                binCtrl = self.__readCtrl()
                self.ctrl = zCtrl()
                self.ctrl.unpackToCtrl(binCtrl)
                size = self.ctrl.ssize * self.ctrl.nsamples
            if self.cfgDataEnable:
                self.samples = self.__readData(size)

    def writeBlock(self):
        """It writes the control and the samples of this class to the char
        device. User should edit ctrl and samples before write"""
        if os.access(self.ctrlFile, os.W_OK) and self.zObj.isEnable():
            if self.cfgCtrlEnable:
                self.__writeCtrl(self.ctrl.packToBin())
            if self.cfgDataEnable:
                self.__writeData(self.samples)


    # # # # # PRIVATE FUNCTIONS # # # # #
    def __unpack_data(self, data, nsamples):
        """It unpacks data in a list of nsampples elements"""
        fmt = "b"
        if self.ctrl.ssize == 1:
            fmt = "B"
        elif self.ctrl.ssize == 2:
            fmt = "H"
        elif self.ctrl.ssize == 4:
            fmt = "I"
        elif self.ctrl.ssize == 8:
            fmt = "Q"
        return struct.unpack((str(nsamples) + fmt), data)

    def __readData(self, size):
        """This function reads samples from data char device"""
        with open(self.dataFile, "r") as f:
            try:
                data_tmp = f.read(size)
                if self.cfgUnpackData:
                    return self.__unpack_data(data_tmp, self.ctrl.nsamples)
                else:
                    return data_tmp
            except IOError as e:
                print("I/O error({0}): {1}".format(e.errno, e.strerror))
                return -e.errno
            except:
                print("Unexpected error:", sys.exc_info()[0])
                raise

    def __writeData(self, samples):
        """This function writes samples into the data char device"""
        with open(self.dataFile, "w") as f:
            try:
                f.write(samples)
            except IOError as e:
                print("I/O error({0}): {1}".format(e.errno, e.strerror))
            except:
                print("Unexpected error:", sys.exc_info()[0])
                raise
        pass


    def __readCtrl(self):
        # and write it
        with open(self.ctrlFile, 'r') as f:
            try:
                return f.read(512)
            except IOError as e:
                print("I/O error({0}): {1}".format(e.errno, e.strerror))
            except:
                print("Unexpected error:", sys.exc_info()[0])
                raise

    def __writeCtrl(self, binCtrl):
        with open(self.ctrlFile, 'w') as f:
            try:
                f.write(binCtrl)
            except IOError as e:
                print("I/O error({0}): {1}".format(e.errno, e.strerror))
                raise
            except:
                print("Unexpected error:", sys.exc_info()[0])
                raise
