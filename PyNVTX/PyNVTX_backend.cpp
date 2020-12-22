#include <pybind11/pybind11.h>


namespace py = pybind11;


PYBIND11_MODULE(PyNVTX_backend, m) {
    m.def(
        "RangePush",
        [](const char * label) {}
    );

    m.def(
        "RangePushA",
        [](const char * label) {}
    );

    m.def(
        "RangePop",
        []() {}
    );

    m.attr("backend_major_version")   = py::int_(0);
    m.attr("backend_minor_version")   = py::int_(2);
    m.attr("backend_release_version") = py::int_(0);

    // Warn user that this backend has been compiled _without_ CUDA support
    m.attr("cuda_enabled")            = py::bool_(false);
}
