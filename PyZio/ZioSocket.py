"""
@author: Federico Vaga
@copyright: Federico Vaga 2012
@license: GPLv2
"""

from PyZio.ZioInterface import ZioInterface

class ZioSocket(object, ZioInterface):
    def __init__(self, zobj):
        self.zobj = zobj
        self.fullpath = self.zObj.attribute["devname"].get_value()

