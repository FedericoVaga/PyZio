"""
@author: Federico Vaga
@copyright: Federico Vaga 2012
@license: GPLv2
"""

import struct

class zCtrlAttr(object):
    def __init__(self, sm, em, sattr, eattr):
        self.std_mask = sm
        self.ext_mask = em
        self.std_val = list(sattr)
        self.ext_val = list(eattr)

class zTLV(object):
    def __init__(self, t, l, v):
        self.type = t
        self.len = l
        self.val = v

class zAddress(object):
    def __init__(self, fam, htype, hid, did, cset, chan, dev):
        self.sa_family = fam
        self.host_type = htype
        self.hostid = hid
        self.dev_id = did
        self.cset_i = cset
        self.chan_i = chan
        self.devname = dev

class zTimeStamp(object):
    def __init__(self, s, t, b):
        self.seconds = s
        self.ticks = t
        self.bins = b

class zCtrl(object):
    def __init__(self):
        # Description of the control structure field's length
        self.packstring = "4B2I2H1H2B8BI2H12s3Q3I12s2HI16I32I2HI16I32I2I8B"
        #                  ^ ^ ^ ^           ^ ^ ^  ^        ^        ^
        self.clear()


    def isValid(self):
        """The control must follow some rule. This function check if the value
        in this control are valid"""
        # nsamples must be pre_samples + post_samples
        if self.nsamples != self.attr_trigger.std_val[1] + self.attr_trigger.std_val[2]:
            return False
        return True

    def unpackToCtrl(self, binctrl):
        """This function unpack a given binary control to fill the fields of
        this class. It use the self.packstring class attribute to unpack"""
        ctrl = struct.unpack(self.packstring, binctrl)
        # 4B
        self.major_version = ctrl[0]
        self.minor_version = ctrl[1]
        self.alarms_zio = ctrl[2]
        self.alarms_dev = ctrl[3]
        # 2I
        self.seq_num = ctrl[4]
        self.nsamples = ctrl[5]
        # 2H
        self.ssize = ctrl[6]
        self.nbits = ctrl[7]
        # 1H2B8BI2H12s
        # ctrl[10] is a filler
        self.addr = zAddress(ctrl[8], ctrl[9], ctrl[11:19], \
                             ctrl[19], ctrl[20], ctrl[21], ctrl[22])
        # 3Q
        self.tstamp = zTimeStamp(ctrl[23], ctrl[24], ctrl[25]);
        # 3I
        self.mem_offset = ctrl[26]
        self.reserved = ctrl[27]
        self.flags = ctrl[28]
        # 12s
        self.triggername = ctrl[29]
        # 2HI16I32I
        self.attr_channel = zCtrlAttr(ctrl[30], ctrl[32], ctrl[33:49], \
                                      ctrl[49:81])
        # 2HI16I32I
        self.attr_trigger = zCtrlAttr(ctrl[81], ctrl[83], ctrl[84:100], \
                                      ctrl[100:132])
        self.tlv = zTLV(ctrl[132], ctrl[133], ctrl[134:142])

    def packToBin(self):
        """This function pack this control into a binary control"""
        pack_list = []
        pack_list.append(self.major_version)
        pack_list.append(self.minor_version)
        pack_list.append(self.alarms_zio)
        pack_list.append(self.alarms_dev)
        pack_list.append(self.seq_num)
        pack_list.append(self.nsamples)
        pack_list.append(self.ssize)
        pack_list.append(self.nbits)
        pack_list.append(self.addr.sa_family)
        pack_list.append(self.addr.host_type)
        pack_list.append(0) # filler
        pack_list.extend(self.addr.hostid)
        pack_list.append(self.addr.dev_id)
        pack_list.append(self.addr.cset_i)
        pack_list.append(self.addr.chan_i)
        pack_list.append(self.addr.devname)
        pack_list.append(self.tstamp.seconds)
        pack_list.append(self.tstamp.ticks)
        pack_list.append(self.tstamp.bins)
        pack_list.append(self.mem_offset)
        pack_list.append(self.reserved)
        pack_list.append(self.flags)
        pack_list.append(self.triggername)
        pack_list.append(self.attr_channel.std_mask)
        pack_list.append(0) # filler
        pack_list.append(self.attr_channel.ext_mask)
        pack_list.extend(self.attr_channel.std_val)
        pack_list.extend(self.attr_channel.ext_val)
        pack_list.append(self.attr_trigger.std_mask)
        pack_list.append(0) # filler
        pack_list.append(self.attr_trigger.ext_mask)
        pack_list.extend(self.attr_trigger.std_val)
        pack_list.extend(self.attr_trigger.ext_val)
        pack_list.append(self.tlv.type)
        pack_list.append(self.tlv.len)
        pack_list.extend(self.tlv.val)
        return struct.pack(self.packstring, *pack_list)

    def clear(self):
        # Control information
        self.major_version = 0
        self.minor_version = 0
        self.alarms_zio = 0
        self.alarms_dev = 0
        self.seq_num = 0
        self.nsamples = 0
        self.ssize = 0
        self.nbits = 0
        self.mem_offset = 0
        self.reserved = 0
        self.flags = 0
        self.triggername = ""
        # ZIO Address
        self.addr = None
        # ZIO Time Stamp
        self.tstamp = None
        # Device and Trigger Attributes
        self.attr_channel = None
        self.attr_trigger = None
        # ZIO TLV
        self.tlv = None