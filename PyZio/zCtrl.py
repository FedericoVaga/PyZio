"""
@author: Federico Vaga
@copyright: Federico Vaga 2012
@license: GPLv2
"""
import os
import struct

class zCtrl(object):
    def __init__(self, path, name):
        self.fullPath = os.path.join(path, name)
        # control information
        self.major_verion = None
        self.minor_varion = None
        self.more_ctrl = None
        self.alarms = None
        self.seq_num = None
        self.flags = None
        self.nsamples = None
        self.ssize = None
        self.nbits = None
        self.hostid = None
        self.devname = None
        self.dev_id = None
        self.cset_i = None
        self.chan_i = None
        self.tstamp = None
        self.mem_offset = None
        self.reserved = None
        self.triggername = None
        self.attr_channel = None
        self.attr_trigger = None
        
    def getControl(self):
        f = open(self.fullPath, "r")
        data = f.read(512)
        f.close()
        # This unpack the control structure element by element
        ctrl = struct.unpack("4B3I2H8B12sI2H3Q2I12s2HI16I32I2HI16I32I20B",data)
        self.major_verion = ctrl[0]
        self.minor_varion = ctrl[1]
        self.more_ctrl = ctrl[2]
        self.alarms = ctrl[3]
        self.seq_num = ctrl[4]
        self.flags = ctrl[5]
        self.nsamples = ctrl[6]
        self.ssize = ctrl[7]
        self.nbits = ctrl[8]
        self.hostid = ctrl[9:16]
        self.devname = ctrl[17]
        self.dev_id = ctrl[18]
        self.cset_i = ctrl[19]
        self.chan_i = ctrl[20]
        self.tstamp = ctrl[21:23]
        self.mem_offset = ctrl[24]
        self.reserved = ctrl[25]
        self.triggername = ctrl[26]
        self.attr_channel = ctrl[27:77]
        self.attr_trigger = ctrl[78:128]
        
        pass
    def setControl(self):
        # FIXME develop me
        pass