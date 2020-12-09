#!/usr/bin/env python
# -*- coding: utf-8 -*-


#_______________________________________________________________________________
# Initialize CUDA Driver
#
import pycuda
import pycuda.driver as drv

drv.init()

#-------------------------------------------------------------------------------


if __name__ == "__main__":
    device = drv.Device(0)
    attrs  = device.get_attributes()

    print(f"*** Attributes for device 0: ***")
    for key, value in attrs.items():
        print(f"{key}:{value}")


