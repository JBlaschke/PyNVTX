# PyNVTX

A thin python wrapper for the nvToolsExt (NVTX) library, using pybind11. This
wrapper is meant to be as thin as possible -- so only provides minimal support.
Currently supported features are:
1. NVTX markers: `nvtxRangePushA` and `nvtxRangePop`
2. Function decorator: `PyNVTX.mark`
3. Automatic decorator generation `PyNVTX.mark_all_methods(<class name>)`


## Installation

Ensure that the `CUDAHOME` environment variable points to your local CUDA
install. To install, either
```
pip install PyNVTX
```
or clone this repo and
```
python setup.py install
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

The  `PyNVTX.mark_all_methods` will automatically decorate all methods in a
class. A guard prevents accidentally decorating any method twice.


## Example Code

To get you started, take a look at `test/test-nvtx.py`
