"""
@author: Federico Vaga
@copyright: Federico Vaga 2012
@license: GPLv2
"""

class zInterface():
    def __init__(self, zObj):
        self.zio_interface_path = "/dev/zio/"
        self.zObj = zObj
        self.interface_prefix = self.zObj.attribute["address"].read()
        self.isInput = False
        self.isOutput = False
        self.ctrlFile = ""
        self.dataFile = ""
        pass

    def readData(self):
        pass

