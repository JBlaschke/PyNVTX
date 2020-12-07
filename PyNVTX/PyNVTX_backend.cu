#include <nvToolsExt.h>
#include <pybind11/pybind11.h>


namespace py = pybind11;


PYBIND11_MODULE(PyNVTX_backend, m) {
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

    m.attr("backend_major_version")   = py::int_(0);
    m.attr("backend_minor_version")   = py::int_(1);
    m.attr("backend_release_version") = py::int_(0);
}
