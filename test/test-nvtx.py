#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import numpy  as np
import PyNVTX as nvtx
from   time   import sleep
from   atexit import register
from   mpi4py import MPI

#_______________________________________________________________________________
# Initialize CUDA Driver
#
import pycuda
import pycuda.driver as drv

drv.init()

from pycuda.gpuarray import GPUArray, to_gpu
from pycuda.compiler import SourceModule

#-------------------------------------------------------------------------------


#_______________________________________________________________________________
# Configure device context to use the GPU belonging to this rank
#
nvtx.RangePushA("Setting Device Context")

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
register(MPI.Finalize)

dev = drv.Device(rank)
ctx = dev.make_context()
# ctx.push()  # NOTE: `make_context` seems to already push
register(ctx.pop)

nvtx.RangePop()
#-------------------------------------------------------------------------------



@nvtx.mark("Build CUDA code")
def init():

    #___________________________________________________________________________
    # Define worker function
    #
    mod = SourceModule("""
    __global__
    void multiply_cuda(double * dest, double * a, double * b, int N) {
        const int index = threadIdx.x + blockIdx.x*blockDim.x;
        for (int i=0; i<N+blockDim.x; i+=blockDim.x) {
            if (index < N) {
                dest[index] = a[index] * b[index];
            }
        }
    }
    """)

    multiply_cuda = mod.get_function("multiply_cuda")
    #---------------------------------------------------------------------------

    return multiply_cuda



class Test(object):

    def __init__(self, size, dim=1024):

        #_______________________________________________________________________
        # Generate sample data
        #
        nvtx.RangePushA("Generating Random Data")

        self.N   = size
        self.dim = dim
        self.A   = np.random.rand(self.N)
        self.B   = np.random.rand(self.N)

        nvtx.RangePop()
        #-----------------------------------------------------------------------


        #_______________________________________________________________________
        # Copy data to device
        #
        nvtx.RangePushA("Sending Data to Device")

        self.d_A = to_gpu(self.A)
        self.d_B = to_gpu(self.B)

        nvtx.RangePop()
        #-----------------------------------------------------------------------


    def apply_fn(self, fn):

        dest = np.zeros_like(self.A)
        fn(drv.Out(dest), self.d_A, self.d_B, np.int64(self.N),
           block=(self.dim, 1, 1), grid=(1, 1))

        return dest


if __name__ == "__main__":

    size = 2**10
    if len(sys.argv) > 1:
        size = int(sys.argv[1])

    print(f"Running test for {size} elements")

    nvtx.mark_all_methods(Test)

    fn   = init()
    test = Test(size)

    AB = test.apply_fn(fn)
