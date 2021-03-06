"""
@author: Federico Vaga <federico.vaga@gmail.com>
@copyright: Federico Vaga 2012
@license: GPLv2
"""

import os
import select

from PyZio.ZioInterface import ZioInterface
from PyZio.ZioCtrl import ZioCtrl

class ZioCharDevice(ZioInterface):
    """
    This class represent the Char Device interface of ZIO. It has two char
    devices: one for control and one for data. The have both the same file
    permission.
    """

    def __init__(self, zobj):
        """
        Initialize ZioCharDevice class. The zobj parameter is the object
        which use this interface. This object should be a channel
        """
        ZioInterface.__init__(self, zobj)
        self.lastctrl = None
        self.__fdc = None
        self.__fdd = None
        # Set data and ctrl char devices
        self.ctrlfile = os.path.join(self.zio_interface_path, \
                                     self.interface_prefix + "-ctrl")
        self.datafile = os.path.join(self.zio_interface_path, \
                                     self.interface_prefix + "-data")
        self.__poll = select.poll()

    def fileno_ctrl(self):
        """
        Return ctrl char device file descriptor
        """
        return self.__fdc
    def fileno_data(self):
        """
        Return data char device file descriptor
        """
        return self.__fdd

    def open_ctrl_data(self, perm):
        self.open_ctrl(perm)
        self.open_data(perm)

    def open_data(self, perm):
        """
        Open data char device
        """
        if self.__fdd == None:
            self.__fdd = os.open(self.datafile, perm)
            self.__poll.register(self.__fdd)
        else:
            print("File already open")
    def open_ctrl(self, perm):
        """
        Open ctrl char device
        """
        if self.__fdc == None:
            self.__fdc = os.open(self.ctrlfile, perm)
            self.__poll.register(self.__fdc)
        else:
            print("File already open")

    def close_ctrl_data(self):
        self.close_ctrl()
        self.close_data()

    def close_data(self):
        """
        Close data char device
        """
        if self.__fdd != None:
            self.__poll.unregister(self.__fdd)
            os.close(self.__fdd)
            self.__fdd = None
    def close_ctrl(self):
        """
        Close ctrl char device
        """
        if self.__fdc != None:
            self.__poll.unregister(self.__fdc)
            os.close(self.__fdc)
            self.__fdc = None


    def read_ctrl(self):
        """
        If the control char device is open and it is readable, then it reads
        the control structure. Every time it internally store the control; it
        will be used as default when no control is provided
        """
        if self.__fdc == None or not self.is_ctrl_readable():
            return None
        # Read the control
        bin_ctrl = os.read(self.__fdc, 512)

        ctrl = ZioCtrl()
        self.lastctrl = ctrl
        ctrl.unpack_to_ctrl(bin_ctrl)
        return ctrl

    def read_data(self, ctrl = None, unpack = True):
        """
        If the data char device is open and it is readable, then it reads
        the data
        """
        if self.__fdd == None or not self.is_data_readable():
            return None

        if ctrl == None:
            if self.lastctrl == None:
                print("WARNING: you never read control, only 16 samples read")
                tmpctrl = ZioCtrl()
                tmpctrl.ssize = 1
                tmpctrl.nsamples = 16
            else:
                tmpctrl = self.lastctrl
        else:
            tmpctrl = ctrl

        data_tmp = os.read(self.__fdd, tmpctrl.ssize * tmpctrl.nsamples)
        if unpack:
            return self._unpack_data(data_tmp, tmpctrl.nsamples, tmpctrl.ssize)
        else:
            return data_tmp

    def read_block(self, rctrl = True, rdata = True, unpack = True):
        """
        It read the control and the samples of a block from char devices.
        It stores the last control in self.lastCtrl. The parameter rctrl and
        rdata are boolean value: if True they acquire the associated
        information
        """
        ctrl = None
        samples = None

        if rctrl and self.__fdc == None:
            self.open_ctrl(os.O_RDONLY)
        if rdata and self.__fdd == None:
            self.open_data(os.O_RDONLY)

        if rctrl:
            ctrl = self.read_ctrl()

        if rdata:  # Read the data
            samples = self.read_data(ctrl, unpack)

        return ctrl, samples

    def write_ctrl(self, ctrl):
        raise NotImplementedError

    def write_data(self, samples):
        raise NotImplementedError

    def write_block(self, ctrl, samples):
        raise NotImplementedError

    def is_device_ready(self, timeout = 0):
        in_ready = False
        out_ready = False
        events = self.poll(timeout)
        if len(events) == 0:  # Check if it is possible to access device
            return False, False

        for __fd, flags in events:
            if flags & (select.POLLIN | select.POLLPRI):
                in_ready = True
            elif flags & select.POLLOUT:
                out_ready = True

        return in_ready, out_ready

    def poll(self, timeout = None):
        """
        It poll() both control and data. It return the Python's list of the
        events occurred on control or data
        """
        return self.__poll.poll(timeout)
