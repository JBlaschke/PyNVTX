#include <nvToolsExt.h>
#include <pybind11/pybind11.h>



PYBIND11_MODULE(PyNVTX, m) {
    m.def(
        "RangePush",
        [](const char * label) {
            nvtxRangePush(label);
        }
    );

    m.def(
        "RangePushA",
        [](const char * label) {
            nvtxRangePushA(label);
        }
    );

    m.def(
        "RangePop",
        []() {
            nvtxRangePop();
        }
    );
}
