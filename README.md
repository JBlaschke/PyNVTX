# PyNVTX

A thin python wrapper for the nvToolsExt (NVTX) library, using pybind11. This
wrapper is meant to be as thin as possible -- so only provides minimal support.
Currently supported features are:
1. NVTX markers: `nvtxRangePushA` and `nvtxRangePop`
2. Function decorator: `PyNVTX.mark`


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


## Example Code

To get you started, take a look at `test/test-nvtx.py`
