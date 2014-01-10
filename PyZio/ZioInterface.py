"""
@author: Federico Vaga <federico.vaga@gmail.com>
@copyright: Federico Vaga 2012
@license: GPLv2
"""
from PyZio.ZioUtil import is_readable, is_writable
import struct

class ZioInterface(object):
    """
    It is a generic abstraction of a ZIO interface: Char Device and socket.
    """

    zio_interface_path = "/dev/zio/"

    def __init__(self, zobj):
        self.zobj = zobj
        self.interface_prefix = self.zobj.attribute["devname"].get_value()
        self.ctrlfile = "" # Full path to the control file
        self.datafile = "" # Full path to the data file
        self.lastctrl = None

    def is_ctrl_readable(self):
        """
        It returns if you can read control from device
        """
        return is_readable(self.ctrlfile)

    def is_ctrl_writable(self):
        """
        It returns if you can write control into device
        """
        return is_writable(self.ctrlfile)

    def is_data_readable(self):
        """
        It returns if you can read data from device
        """
        return is_readable(self.datafile)

    def is_data_writable(self):
        """
        It returns if you can write data into device
        """
        return is_writable(self.datafile)


    def is_device_ready(self, timeout = 0):
        """
        It is a mandatory method for the derived class. It must returns two
        boolean value: the first is 'True' if the device is ready to be read;
        the second is 'True if the device is ready to be write'. The optional
        parameter 'timeout' sets the time to wait before return. The '0' value
        mean immediately, 'None' mean infinite, and a different value represent
        the milliseconds to wait.
        """
        raise NotImplementedError


    # Mandatory Open Methods
    def open_ctrl_data(self, perm):
        """
        It is a mandatory method for the derived class. It opens both control
        and data source. The 'perm' parameter set the permission to use during
        open
        """
        raise NotImplementedError

    def open_data(self, perm):
        """
        It is a mandatory method for the derived class. It opens samples's
        source. The 'perm' parameter set the permission to use during open
        """
        raise NotImplementedError

    def open_ctrl(self, perm):
        """
        It is a mandatory method for the derived class. It opens control's
        source. The 'perm' parameter set the permission to use during open
        """
        raise NotImplementedError


    # Mandatory Close Methods
    def close_ctrl_data(self):
        """
        It is a mandatory method for the derived class. It closes both control
        and data source.
        """
        raise NotImplementedError

    def close_data(self):
        """
        It is a mandatory method for the derived class. It closes sample's
        source.
        """
        raise NotImplementedError

    def close_ctrl(self):
        """
        It is a mandatory method for the derived class. It closes control's
        source.
        """
        raise NotImplementedError


    # Mandatory Read/Write Methods
    def read_ctrl(self):
        """
        It is a mandatory method for the derived class. It reads, and returns,
        a control structure from a channel.
        """
        raise NotImplementedError

    def read_data(self, ctrl = None, unpack = True):
        """
        It is a mandatory method for the derived class. It reads, and returns,
        samples from a channel.
        """
        raise NotImplementedError

    def read_block(self, rctrl = True, rdata = True, unpack = True):
        """
        It is a mandatory method for the derived class. It reads, and returns,
        a block from a channel. The block is a python set with control and
        data.
        """
        raise NotImplementedError

    def write_ctrl(self, ctrl):
        """
        It is a mandatory method for the derived class. It writes a control
        to a channel
        """
        raise NotImplementedError

    def write_data(self, samples):
        """
        It is a mandatory method for the derived class. It writes samples to
        a channel
        """
        raise NotImplementedError

    def write_block(self, ctrl, samples):
        """
        It is a mandatory method for the derived class. It writes both control
        and samples to a channel
        """
        raise NotImplementedError

    def _unpack_data(self, data, nsamples, ssize):
        """
        It unpacks 'data' of nsamples elements of the same size 'ssize'
        """
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