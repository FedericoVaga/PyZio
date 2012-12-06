"""
@author: Federico Vaga
@copyright: Federico Vaga 2012
@license: GPLv2
"""

class zInterface():
    """This class is a generic abstraction of a ZIO interface: Char Device
    and socket. PyZIO support only char device at the moment"""
    def __init__(self, zObj):
        self.zio_interface_path = "/dev/zio/"
        self.zObj = zObj
        self.interface_prefix = self.zObj.attribute["address"].getValue()
        self.isInput = False
        self.isOutput = False
        self.ctrlFile = ""
        self.dataFile = ""
        pass

