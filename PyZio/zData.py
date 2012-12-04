"""
@author: Federico Vaga
@copyright: Federico Vaga 2012
@license: GPLv2
"""

import os
import sys
import struct

class zData(object):
    def __init__(self, path, name, ctrl):
        self.fullPath = os.path.join(path, name)
        self.ctrl = ctrl
        self.data = None
        self.readable = True if os.access(self.fullPath, os.R_OK) else False
        self.writable = True if os.access(self.fullPath, os.W_OK) else False

    '''
    __unpack_data
    data: data to unpack
    nsamples: nsamples in data
    unpack data according to ssize
    '''
    def __unpack_data(self, data, nsamples):
        format = "b"
        if self.ctrl.ssize == 1:
            format = "B"
        elif self.ctrl.ssize == 2:
            format = "H"
        elif self.ctrl.ssize == 4:
            format = "I"
        elif self.ctrl.ssize == 8:
            format = "Q"
        return struct.unpack((str(nsamples) + format), data)
    
    '''
    readData
    readCtrl: is a boolean value, if true read control before read
    unpackData: is a boolean value, if true data is unpacked
    '''
    def readData(self, readCtrl, unpackData):
        if readCtrl:
            self.ctrl.get_ctrl()
        with open(self.fullPath, "r") as f:
            try:
                data_tmp = f.read(self.ctrl.ssize * self.ctrl.nsamples)
                if unpackData:
                    self.data = self.__unpack_data(data_tmp, self.ctrl.nsamples)
                else:
                    self.data = data_tmp
            except IOError as e:
                print("I/O error({0}): {1}".format(e.errno, e.strerror))
                return -e.errno
            except:
                print("Unexpected error:", sys.exc_info()[0])
                return -2
                raise
        return self.data

    def writeData(self):
        pass