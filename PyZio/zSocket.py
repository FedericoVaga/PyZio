"""
@author: Federico Vaga
@copyright: Federico Vaga 2012
@license: GPLv2
"""

class zInterface():
    def __init__(self, zObj):
        self.zObj = zObj
        self.fullPath = self.zObj.attribute["address"].read()
        pass

    def readData(self):
        pass

