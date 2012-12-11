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
        self.interface_prefix = self.zObj.attribute["address"].getValue()
        self.ctrlFile = ""
        self.dataFile = ""

    def isInput(self):
        return os.access(self.ctrlFile, os.R_OK)

    def isOutput(self):
        return os.access(self.ctrlFile, os.W_OK)

