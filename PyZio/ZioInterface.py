"""
@author: Federico Vaga <federico.vaga@gmail.com>
@copyright: Federico Vaga 2012
@license: GPLv2
"""
from PyZio.ZioUtil import is_readable, is_writable

class ZioInterface:
    """It is a generic abstraction of a ZIO interface: Char Device and socket."""
    def __init__(self, zobj):
        self.zio_interface_path = "/dev/zio/"
        self.zobj = zobj
        self.interface_prefix = self.zobj.attribute["devname"].get_value()
        self.ctrlfile = "" # Full path to the control file
        self.datafile = "" # Full path to the data file

    def is_ctrl_readable(self):
        """It returns if you can read control from device"""
        return is_readable(self.ctrlfile)

    def is_ctrl_writable(self):
        """It returns if you can write control into device"""
        return is_writable(self.ctrlfile)

    def is_data_readable(self):
        """It returns if you can read data from device"""
        return is_readable(self.datafile)

    def is_data_writable(self):
        """It returns if you can write data into device"""
        return is_writable(self.datafile)
