"""
@author: Federico Vaga
@copyright: Federico Vaga 2012
@license: GPLv2
"""

zio_bus_path = "/sys/bus/zio/"
devices_path = zio_bus_path + "devices/"

triggers = [] # list of available triggers (string)
buffers = []  # list of available buffers (string)
devices = []  # list of available devices (zdev object)

# sysfs standard attributes name tuples
zio_dev_attr_name = ("gain_factor", "offset", "resolution-bits", \
                     "max-sample-rate", "vref-src")
zio_buf_attr_name = ("max-buffer-len", "max-buffer-kb")
zio_trg_attr_name = ("re-enable", "pre-samples", "post-samples")
