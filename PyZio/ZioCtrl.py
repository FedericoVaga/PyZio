"""
@author: Federico Vaga
@copyright: Federico Vaga 2012
@license: GPLv2
"""

import struct

class ZioCtrlAttr(object):
    """
    It represent the python version of the zio_ctrl_attr structure
    """
    def __init__(self, sm, em, sattr, eattr):
        self.std_mask = sm
        self.ext_mask = em
        self.std_val = list(sattr)
        self.ext_val = list(eattr)

    def __eq__(self, other):
        if not isinstance(other, ZioCtrlAttr):
            return False

        ret = True
        ret = ret and self.std_mask == other.std_mask
        ret = ret and self.ext_mask == other.ext_mask
        for val1, val2 in zip(self.std_val, other.std_val):
            ret = ret and val1 == val2
        for val1, val2 in zip(self.ext_val, other.ext_val):
            ret = ret and val1 == val2

        return ret

    def __ne__(self, other):
        return not self.__eq__(other)

class ZioTLV(object):
    """
    It represent the python version of the zio_tlv structure
    """
    def __init__(self, t, l, v):
        self.type = t
        self.len = l
        self.val = v

class ZioAddress(object):
    """
    It represent the python version of the zio_addr structure
    """
    def __init__(self, fam, htype, hid, did, cset, chan, dev):
        self.sa_family = fam
        self.host_type = htype
        self.hostid = hid
        self.dev_id = did
        self.cset_i = cset
        self.chan_i = chan
        self.devname = dev.replace("\x00", "")

    def __eq__(self, other):
        if not isinstance(other, ZioAddress):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)

class ZioTimeStamp(object):
    """
    It represent the python version of the zio_timestamp structure
    """
    def __init__(self, s, t, b):
        self.seconds = s
        self.ticks = t
        self.bins = b

    def __eq__(self, other):
        if not isinstance(other, ZioTimeStamp):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)

class ZioCtrl(object):
    """
    It represent the python verion of the zio_control structure
    """

    def __init__(self):
        # Description of the control structure field's length
        self.packstring = "4B2I2H1H2B8BI2H12s3Q3I12s2HI16I32I2HI16I32I2I8B"
        #                  ^ ^ ^ ^           ^ ^ ^  ^        ^        ^

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

    def __eq__(self, other):
        if not isinstance(other, ZioCtrl):
            return False

        ret = True
        # Fields
        ret = ret and self.major_version == other.major_version
        ret = ret and self.minor_version == other.minor_version
        ret = ret and self.alarms_zio == other.alarms_zio
        ret = ret and self.alarms_dev == other.alarms_dev
        ret = ret and self.seq_num == other.seq_num
        ret = ret and self.nsamples == other.nsamples
        ret = ret and self.ssize == other.ssize
        ret = ret and self.nbits == other.nbits
        ret = ret and self.mem_offset == other.mem_offset
        ret = ret and self.reserved == other.reserved
        ret = ret and self.flags == other.flags
        # Objects
        ret = ret and self.addr == other.addr
        ret = ret and self.tstamp == other.tstamp
        ret = ret and self.triggername == other.triggername
        ret = ret and self.attr_channel == other.attr_channel
        ret = ret and self.attr_trigger == other.attr_trigger

        return ret

    def __ne__(self, other):
        return not self.__eq__(other)

    def is_valid(self):
        """
        The control must follow some rule. This function check if the value
        in this control are valid
        FIXME ONLY FOR OUTPUT
        """
        # nsamples must be pre_samples + post_samples
        attr_nsamples = self.attr_trigger.std_val[1] \
                      + self.attr_trigger.std_val[2]
        if self.nsamples != attr_nsamples:
            return False
        return True

    def unpack_to_ctrl(self, binctrl):
        """
        This function unpack a given binary control to fill the fields of
        this class. It use the self.packstring class attribute to unpack
        """
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
        self.addr = ZioAddress(ctrl[8], ctrl[9], ctrl[11:19], \
                               ctrl[19], ctrl[20], ctrl[21], ctrl[22])
        # 3Q
        self.tstamp = ZioTimeStamp(ctrl[23], ctrl[24], ctrl[25])
        # 3I
        self.mem_offset = ctrl[26]
        self.reserved = ctrl[27]
        self.flags = ctrl[28]
        # 12s
        self.triggername = ctrl[29].replace("\x00", "")
        # 2HI16I32I
        self.attr_channel = ZioCtrlAttr(ctrl[30], ctrl[32], ctrl[33:49], \
                                      ctrl[49:81])
        # 2HI16I32I
        self.attr_trigger = ZioCtrlAttr(ctrl[81], ctrl[83], ctrl[84:100], \
                                      ctrl[100:132])
        self.tlv = ZioTLV(ctrl[132], ctrl[133], ctrl[134:142])

    def pack_to_bin(self):
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
        pack_list.append(0)  # filler
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
        pack_list.append(0)  # filler
        pack_list.append(self.attr_channel.ext_mask)
        pack_list.extend(self.attr_channel.std_val)
        pack_list.extend(self.attr_channel.ext_val)
        pack_list.append(self.attr_trigger.std_mask)
        pack_list.append(0)  # filler
        pack_list.append(self.attr_trigger.ext_mask)
        pack_list.extend(self.attr_trigger.std_val)
        pack_list.extend(self.attr_trigger.ext_val)
        pack_list.append(self.tlv.type)
        pack_list.append(self.tlv.len)
        pack_list.extend(self.tlv.val)
        return struct.pack(self.packstring, *pack_list)

    def clear(self):
        """
        It clears the content of the class
        """
        self.__init__()
