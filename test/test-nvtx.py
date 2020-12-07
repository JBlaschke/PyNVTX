#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy  as np
import PyNVTX as nvtx
from   time   import sleep
from   atexit import register
from   mpi4py import MPI



@nvtx.mark("test_function")
def test():
    #___________________________________________________________________________
    # Initialize CUDA Driver
    #
    nvtx.RangePushA("Initializing PyCUDA Driver")

    import pycuda
    import pycuda.driver    as drv
    from   pycuda.gpuarray import GPUArray, to_gpu

    drv.init()

    nvtx.RangePop()
    #---------------------------------------------------------------------------


    #___________________________________________________________________________
    # Generate sample data
    #
    nvtx.RangePushA("Generating Random Data")

    giant_data = np.random.rand(1024**3)

    nvtx.RangePop()
    #---------------------------------------------------------------------------


    #___________________________________________________________________________
    # Configure device context to use the GPU belonging to this rank
    #
    nvtx.RangePushA("Setting Device Context")

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    register(MPI.Finalize)

    dev = drv.Device(rank)
    ctx = dev.make_context()
    # ctx.push()  # NOTE: `make_context` seems to already push to the context
    # stack
    register(ctx.pop)

    nvtx.RangePop()
    #---------------------------------------------------------------------------


    #___________________________________________________________________________
    # Copy data to device
    #
    nvtx.RangePushA("Sending Data to Device")

    d_giant_data = to_gpu(giant_data)

    nvtx.RangePop()
    #---------------------------------------------------------------------------



if __name__ == "__main__":

    test()

    sleep(10)
