# -*- coding: utf-8 -*-

from .builder import Builder

class SRL(object):

    def __init__(self, dsl=None):
        self.dsl = dsl
        self.compiled = Builder.parse(dsl)

    def __str__(self):
        return self.compiled.pattern

    def __getattr__(self, method):
        return getattr(self.compiled, method)
