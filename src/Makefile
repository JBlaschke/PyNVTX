CXX      := g++
NVCXX    := nvcc
CXXSTD   := -std=c++11
CXXFLAGS := $(CXXSTD) -O3 -shared 
NVOPTS   := --compiler-options -fPIC 
INCLUDES := $(shell python -m pybind11 --includes)
PYSUFFIX := $(shell python3-config --extension-suffix)

all: PyNVTX$(PYSUFFIX)


%$(PYSUFFIX): %.cu
	$(NVCXX) $(CXXFLAGS) $(NVOPTS) $(INCLUDES) $< -o $@ -lnvToolsExt
