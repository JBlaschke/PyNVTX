#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import wraps

from PyNVTX_backend import *


major_version   = 0;
minor_version   = 1;
release_version = 3;

NVTX_IDENTIFIER = "NVTX"



def mark(label):
    def _mark(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            RangePushA(label)
            ret = func(*args, **kwargs)
            RangePop()
            return ret
        return wrapped
    return _mark



def is_decorated(cls, identifier):
    for attr in cls.__dict__:
        if attr == dec_id_str(identifier):
            return True



def dec_id_str(identifier):
    return f"__deco_{identifier}"



def mark_all_methods(cls):
    if is_decorated(cls, NVTX_IDENTIFIER):
        return

    for attr in cls.__dict__:
        if callable(getattr(cls, attr)):
            dec = mark(f"{cls}.{attr}")
            setattr(cls, attr, dec(getattr(cls, attr)))

    setattr(cls, dec_id_str(NVTX_IDENTIFIER), True)

    for base in cls.__bases__:
        if base == object:
           continue
        mark_all_methods(decorator, base)
