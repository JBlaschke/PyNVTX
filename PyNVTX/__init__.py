#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import wraps

from PyNVTX_backend import *

major_version   = 0;
minor_version   = 1;
release_version = 2;



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
