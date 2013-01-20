"""
@author: Federico Vaga <federico.vaga@gmail.com>
@copyright: Federico Vaga 2012
@license: GPLv2
"""

import os
import struct

from PyZio.ZioInterface import ZioInterface
from PyZio.ZioCtrl import ZioCtrl

class ZioCharDevice(ZioInterface):
    """This class represent the Char Device interface of ZIO. It has to char
    device: one for control and one for data. The have both the same file
    permission."""

    def __init__(self, zobj):
        """Initialize zCharDevice class. the zobj parameter is the object
        which use this interface. This object should be a channel"""
        ZioInterface.__init__(self, zobj)

        # Set data and ctrl char devices
        self.ctrlfile = os.path.join(self.zio_interface_path, \
                                     self.interface_prefix + "-ctrl")
        self.datafile = os.path.join(self.zio_interface_path, \
                                     self.interface_prefix + "-data")

        self.lastctrl = None
        # Options
        self.cfg_unpack_data = True
        pass

    def set_unpack_data(self, status):
        self.cfg_unpack_data = status

    def is_unpack_data(self):
        return self.cfg_unpack_data

    def read_block(self, rctrl, rdata):
        """It read the control and the samples of a block from char devices.
        It stores the last control in self.lastCtrl. The parameter rctrl and
        rdata are boolean value: if True they acquire the associated
        information"""
        ctrl = None
        samples = None

        if self.is_ctrl_readable() and rctrl:
            # Read the control
            fd = os.open(self.ctrlfile, os.O_RDONLY)
            bin_ctrl = os.read(fd, 512)
            os.close(fd)
            ctrl = ZioCtrl()
            self.lastctrl = ctrl
            ctrl.unpack_to_ctrl(bin_ctrl)

        if self.is_data_readable() and rdata: # Read the data
            if ctrl == None:
                if self.lastCtrl == None:
                    print("WARNING: you never read control, then only 16byte will be read")
                    tmpctrl = ZioCtrl()
                    tmpctrl.ssize = 1
                    tmpctrl.nsamples = 16
                else:
                    tmpctrl = self.lastCtrl
            else:
                tmpctrl = ctrl
            fd = os.open(self.datafile, os.O_RDONLY)
            data_tmp = os.read(fd, tmpctrl.ssize * tmpctrl.nsamples)
            os.close(fd)
            if self.cfg_unpack_data:
                samples =  self.__unpack_data(data_tmp, tmpctrl.nsamples, tmpctrl.ssize)

        return ctrl, samples

    def write_block(self, ctrl, samples):
        """It writes the control and the samples of this class to the char
        device. User should edit ctrl and samples before write"""
        if self.is_ctrl_writable() and isinstance(ctrl, ZioCtrl):
            fd = os.open(self.ctrlfile, os.O_WRONLY)
            os.write(fd, ctrl.pack_to_bin())
            os.close(fd)
        else:
            raise #FIXME define zio exception
        if self.is_data_writable() and samples != None:
            fd = os.open(self.datafile, os.O_WRONLY)
            os.write(fd, samples)
            os.close(fd)
        else:
            raise #FIXME define zio exception


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
