"""
@author: Federico Vaga
@copyright: Federico Vaga 2012
@license: GPLv2
"""

import os
from stat import ST_MODE

from .zInterface import zInterface
from .zCtrl import zCtrl
from .zData import zData

"""
This class represent the Char Device interface of ZIO. It has to char device:
one for control and one for data. The have both the same file permission.
"""
class zCharDevice(object, zInterface):
    def __init__(self, zObj):
        zInterface.__init__(self, zObj)
        # Set the char device directions
        zmode = oct(os.stat(self.zio_interface_path + \
                            self.interface_prefix + "-ctrl")\
                    [ST_MODE])[-3:]
        self.isOutput = True if zmode & 222 else False
        self.isIntput = True if zmode & 444 else False

        self.ctrlFile = os.path.join(self.zio_interface_path, \
                                     self.interface_prefix + "-ctrl")
        self.dataFile = os.path.join(self.zio_interface_path, \
                                     self.interface_prefix + "-data")
        self.ctrl = zCtrl()
        self.data = zData(self.dataFile, self.ctrl)

        self.cfgCtrlFirst = False
        self.cfgUnpackData = False
        pass

    def setReadCtrlFirst(self, status):
        self.cfgCtrlFirst = status
    def setUnpackData(self, status):
        self.cfgUnpackData = status
    def isReadCtrlFirst(self, status):
        return self.cfgCtrlFirst
    def isUnpackData(self, status):
        return self.cfgUnpackData

    def readData(self):
        return self.data.readData(True)

    def readCtrl(self):
        return self.ctrl.get_ctrl(self.ctrlFile)

    def writeData(self, data):
        return self.data.writeData(data)

    def writeCtrl(self):
        return self.ctrl.set_ctrl(self.ctrlFile)

