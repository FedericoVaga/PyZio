"""
@author: Federico Vaga
@copyright: Federico Vaga 2012
@license: GPLv2
"""

import os
import string
from .zDev import zDev
from .zConfig import zio_bus_path, devices_path, devices, buffers, triggers

'''
isLoaded
It returns true if ZIO is loaded correctly, otherwise it returns false
'''
def isLoaded():
    if not os.path.exists(zio_bus_path):
        print("ZIO is not loaded")
        return False

    if not os.access(zio_bus_path + "/available_buffers", os.R_OK) and \
       not os.access(zio_bus_path + "/available_triggers", os.R_OK):
        print("ZIO is not loaded correctly")
        return False
    return True

'''
updateDevices
It updates the internal list of available devices
'''
def updateDevices():
    del devices[:]
    for zdev in os.listdir(devices_path):
        print("Device found: " +  zdev)
        if string.find(zdev, "hw-") == 0:
            print("  skip because is HW device")
            continue
        newDev = zDev(devices_path, zdev)
        devices.append(newDev)
    pass

'''
updateBuffers
It updates the internal list of available buffers
'''
def updateBuffers():
    del buffers[:]
    # read all available buffers
    f = open(zio_bus_path + "/available_buffers", "r")
    for line in f:
        buffers.append(line.rstrip('\n'))
    f.close()
    pass

'''
updateTriggers
It updates the internal list of available triggers
'''
def updateTriggers():
    del triggers[:]
    # read all available triggers
    f = open(zio_bus_path + "/available_triggers", "r")
    for line in f:
        triggers.append(line.rstrip('\n'))
    f.close()
    pass

'''
It updates the internal list of available devices, buffers and triggers
'''
def updateAll():
    updateDevices()
    updateTriggers()
    updateBuffers()