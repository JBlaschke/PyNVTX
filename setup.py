#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import pybind11
import setuptools

from os.path                     import join as pjoin
from glob                        import glob
from setuptools                  import setup, Extension
from distutils.command.build_ext import build_ext
from pybind11.setup_helpers      import Pybind11Extension



def find_in_path(name, path):
    """Find a file in a search path"""

    # Adapted fom http://code.activestate.com/recipes/52224
    for dir in path.split(os.pathsep):
        binpath = pjoin(dir, name)
        if os.path.exists(binpath):
            return os.path.abspath(binpath)
    return None



def locate_cuda():
    """Locate the CUDA environment on the system
    Returns a dict with keys 'home', 'nvcc', 'include', and 'lib64'
    and values giving the absolute path to each directory.
    Starts by looking for the CUDAHOME env variable. If not found,
    everything is based on finding 'nvcc' in the PATH.
    """

    # First check if the CUDAHOME env variable is in use
    if 'CUDAHOME' in os.environ:
        home = os.environ['CUDAHOME']
        nvcc = pjoin(home, 'bin', 'nvcc')
    else:
        # Otherwise, search the PATH for NVCC
        nvcc = find_in_path('nvcc', os.environ['PATH'])
        if nvcc is None:
            raise EnvironmentError('The nvcc binary could not be '
                'located in your $PATH. Either add it to your path, '
                'or set $CUDAHOME')
        home = os.path.dirname(os.path.dirname(nvcc))

    cudaconfig = {'home': home, 'nvcc': nvcc,
                  'include': pjoin(home, 'include'),
                  'lib64': pjoin(home, 'lib64')}
    for k, v in iter(cudaconfig.items()):
        if not os.path.exists(v):
            raise EnvironmentError('The CUDA %s path could not be '
                                   'located in %s' % (k, v))

    return cudaconfig



def customize_compiler_for_nvcc(self):
    """Inject deep into distutils to customize how the dispatch
    to gcc/nvcc works.
    If you subclass UnixCCompiler, it's not trivial to get your subclass
    injected in, and still have the right customizations (i.e.
    distutils.sysconfig.customize_compiler) run on it. So instead of going
    the OO route, I have this. Note, it's kindof like a wierd functional
    subclassing going on.
    """

    # Tell the compiler it can processes .cu
    self.src_extensions.append('.cu')

    # Save references to the default compiler_so and _comple methods
    default_compiler_so = self.compiler_so
    super = self._compile

    # Now redefine the _compile method. This gets executed for each
    # object but distutils doesn't have the ability to change compilers
    # based on source extension: we add it.
    def _compile(obj, src, ext, cc_args, extra_postargs, pp_opts):
        if os.path.splitext(src)[1] == '.cu':
            # use the cuda for .cu files
            self.set_executable('compiler_so', CUDA['nvcc'])
            # use only a subset of the extra_postargs, which are 1-1
            # translated from the extra_compile_args in the Extension class
            postargs = extra_postargs['nvcc']
        else:
            postargs = extra_postargs['gcc']

        super(obj, src, ext, cc_args, postargs, pp_opts)
        # Reset the default compiler_so, which we might have changed for cuda
        self.compiler_so = default_compiler_so

    # Inject our redefined _compile method into the class
    self._compile = _compile



# Run the customize_compiler
class custom_build_ext(build_ext):
    def build_extensions(self):
        customize_compiler_for_nvcc(self.compiler)
        build_ext.build_extensions(self)



CUDA = locate_cuda()



ext_modules = [
    Extension(
        "PyNVTX_backend",
        sorted(glob("PyNVTX/*.cu")),
        library_dirs=[CUDA["lib64"]],
        libraries=["cudart", "nvToolsExt"],
        runtime_library_dirs=[CUDA["lib64"]],
        # this syntax is specific to this build system we're only going to use
        # certain compiler args with nvcc and not with gcc the implementation of
        # this trick is in customize_compiler() below
        # extra_compile_args={"gcc": [],
        #                     "nvcc": ["-arch=sm_20", "--ptxas-options=-v",
        #                              "-c", "--compiler-options", "'-fPIC'"]},
        extra_compile_args={"gcc": [],
                            "nvcc": ["-std=c++11", "-O3", "-shared",
                                     "--compiler-options", "-fPIC",
                                     "-lnvToolsExt",]},
        include_dirs=[CUDA["include"], "PyNVTX"]
                    + [pybind11.get_include(True ), pybind11.get_include(False)]
    )
]



with open("README.md", "r") as fh:
    long_description = fh.read()



setup(
    name="PyNVTX",
    version="0.1.3",
    author="Johannes Blaschke",
    author_email="johannes@blaschke.science",
    description="A thin python wrapper for the nvToolsExt (NVTX) library, using pybind11",
    ext_modules=ext_modules,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JBlaschke/PyNVTX",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
      'pybind11',
    ],
    # inject our custom trigger
    cmdclass={'build_ext': custom_build_ext},
)
