# PyNVTX

A thin python wrapper for the nvToolsExt (NVTX) library, using pybind11. This
wrapper is meant to be as thin as possible -- so only provides minimal support.
Currently supported features are:
1. NVTX markers: `nvtxRangePushA` and `nvtxRangePop`
2. Function decorator: `PyNVTX.mark`
3. Automatic decorator generation `PyNVTX.mark_all_methods(<class name>)`



## Installation

Ensure that the `nvcc` is in your `PATH` -- or alternatively ensure that the
`CUDAHOME` environment variable points to your local CUDA install. To install,
either
```
pip install PyNVTX
```
or clone this repo and
```
python setup.py install
```


### This Won't Break If You Don't Have CUDA

You know what would suck? If including `PyNVTX` required CUDA to be installed?
Why? There are loads of applications that support CUDA, if available. And
default to the CPU-only version otherwise. `PyNVTX` is the same. If `nvcc` in
not in your `PATH` (nor in your `CUDAHOME`), then you'll see this warning:
```
 *** WARNING: The nvcc binary could not be located in your $PATH. Either add it to your path, or set $CUDAHOME
```
(note that it will not warn you if you're installing with pip) and `PyNVTX`
will still install (it just won't do anything). You can check if a local
version of `PyNVTX` has been built with CUDA support by checking:
```python
PyNVTX.cuda_enabled # True if compiled with CUDA support
```



## NVTX Markers (`nvtxRangePushA` / `nvtxRangePop`)

```python
import PyNVTX as nvtx

nvtx.RangePushA("Doing some work")

# code to time goes here

nvtx.RangePop()
```


### Function Decorator

The `PyNVTX.mark` will put `RangePushA` and `RangePop` the the beginning and of
the function call:
```python
import PyNVTX as nvtx

@nvtx.mark("test_function")
def test():
    # You code goes here
```


### Automatic Instrumentation

The `PyNVTX.mark_all_methods` will automatically decorate all methods in a
class, as well as all methods it inherits. A guard prevents accidentally
decorating any method twice. Eg.:
```python
import PyNVTX as nvtx

class MyClassA(object):
    def __init__(self):
        pass

    def f(self):
        pass

class MyClassB(MyClassA):
    def __init__(self):
        pass

    def g(self):
        pass


nvtx.mark_all_methods(MyClassB)
```
Will instrument `MyClassB`'s `__init__`, as well as `f` and `g`, but _not_
`MyClassA`'s `__init__`.

Adding a class/method name to `PyNVTX.REGISTRY` will prevent it from being
instrumented by `PyNVTX.mark_all_methods`. For example:
```python
nvtx.REGISTRY.add(MyClassB, "f") # note the method name is a string
nvtx.mark_all_methods(MyClassB)
```
will not instrument `f`.



## Example Code

To get you started, take a look at `test/test-nvtx.py`
