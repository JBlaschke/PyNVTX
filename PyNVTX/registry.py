#!/usr/bin/env python
# -*- coding: utf-8 -*-


from .singleton import Singleton


class Registry(object, metaclass=Singleton):

    def __init__(self):
        self.registry = dict()


    def add(self, cls, method):
        if cls in self.registry:
            self.registry[cls].append(method)
        else:
            self.registry[cls] = [method]


    def skip(self, cls, method):
        if cls in self.registry:
            if method in self.registry[cls]:
                return True

        return False
