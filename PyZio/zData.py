"""
@author: Federico Vaga
@copyright: Federico Vaga 2012
@license: GPL
"""

import os
import struct

class zData(object):
    def __init__(self, path, name, ctrl):
        self.file = os.path.join(path, name)
        self.ctrl = ctrl
        self.data = None
    
    '''
    updateCtrl is a boolean value, if true read control before read
    unpackData is a boolean value, if true data is unpacked
    '''
    def readData(self, updateCtrl, unpackData):
        if updateCtrl:
            self.ctrl.getControl()
        
        f = open(self.file, "r")
        size = self.ctrl.ssize * self.ctrl.nsamples
        self.data = f.read(size)
        
        if unpackData:
            format = "b"
            if self.ctrl.ssize == 1:
                format = "B"
            elif self.ctrl.ssize == 2:
                format = "H"
            elif self.ctrl.ssize == 4:
                format = "I"
            elif self.ctrl.ssize == 8:
                format = "Q"
            format = str(self.ctrl.nsamples) + format
            self.data = struct.unpack(format, self.data)
        
        f.close()
        return self.data
    
    def writeData(self):
        pass