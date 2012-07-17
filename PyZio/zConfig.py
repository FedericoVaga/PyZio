"""
@author: Federico Vaga
@copyright: Federico Vaga 2012
@license: GPLv2
"""

zio_bus_path = "/sys/bus/zio/"
devices_path = zio_bus_path + "devices/"

# fot char device interface
zio_cdev_path = "/dev/zio/"

triggers = [] # list of available triggers (string)
buffers = []  # list of available buffers (string)
devices = []  # list of available devices (zdev object)