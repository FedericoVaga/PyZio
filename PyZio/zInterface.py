"""
@author: Federico Vaga <federico.vaga@gmail.com>
@copyright: Federico Vaga 2012
@license: GPLv2
"""

import os

class zInterface():
    """This class is a generic abstraction of a ZIO interface: Char Device
    and socket. PyZIO support only char device at the moment"""
    def __init__(self, zObj):
        self.zio_interface_path = "/dev/zio/"
        self.zObj = zObj
        self.interface_prefix = self.zObj.attribute["devname"].getValue()
        self.ctrlFile = ""
        self.dataFile = ""

    def is_ctrl_readable(self):
        """It returns if you can read control from device"""
        return os.access(self.ctrlFile, os.R_OK)

    def is_ctrl_writable(self):
        """It returns if you can write control into device"""
        return os.access(self.ctrlFile, os.W_OK)

    def is_data_readable(self):
        """It returns if you can read data from device"""
        return os.access(self.dataFile, os.R_OK)

    def is_data_writable(self):
        """It returns if you can write data into device"""
        return os.access(self.dataFile, os.W_OK)

