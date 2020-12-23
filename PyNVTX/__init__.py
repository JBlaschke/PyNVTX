#!/usr/bin/env python
# -*- coding: utf-8 -*-


from functools import wraps

from PyNVTX_backend import *
from .singleton     import Singleton
from .registry      import Registry


major_version   = 0;
minor_version   = 3;
release_version = 0;

NVTX_IDENTIFIER = "NVTX"
REGISTRY = Registry()



def annotate(label):
    def _annotate(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            RangePushA(label)
            ret = func(*args, **kwargs)
            RangePop()
            return ret
        return wrapped
    return _annotate



def is_decorated(cls, identifier):
    for attr in cls.__dict__:
        if attr == dec_id_str(identifier):
            return True



def dec_id_str(identifier):
    return f"__deco_{identifier}"



def annotate_all_methods(cls):
    if is_decorated(cls, NVTX_IDENTIFIER):
        return

    for attr in cls.__dict__:
        if REGISTRY.skip(cls, attr):
            continue

        if callable(cls.__dict__[attr]):
            dec = annotate(f"{cls}.{attr}")
            type.__setattr__(cls, attr, dec(cls.__dict__[attr]))

    type.__setattr__(cls, dec_id_str(NVTX_IDENTIFIER), True)

    for base in cls.__bases__:
        if base == object:
           continue
        annotate_all_methods(base)
