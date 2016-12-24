#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_pyenvdiff
----------------------------------

Tests for `pyenvdiff` module.
"""

import pytest as pt
import inspect 

import pyenvdiff
from pyenvdiff.collectors import Collector, collector_classes
        
class TestCollectors(object):
    def test_all_collectors_are_captured(self):
        num = 0
        for obj_name in dir(pyenvdiff.collectors):
            obj = getattr(pyenvdiff.collectors, obj_name)
            if inspect.isclass(obj):
                if issubclass(obj, Collector):
                    num += 1
        num = num - 1 # Since the check above will catch the base class, Collector
        assert(len(collector_classes) == num), "All Collectors should be included in the collector_class list"
    @pt.mark.parametrize("CollectorClass", collector_classes)
    def test_equality_check(self, CollectorClass):
        assert(CollectorClass() == CollectorClass()), "Collector should be able to be compared for equality"
    @pt.mark.parametrize("CollectorClass", collector_classes)
    def test_string_returns_a_string(self, CollectorClass):
        col = str(CollectorClass())
        assert(isinstance(col, str)), "Collector should serialize to a string"
    @pt.mark.parametrize("CollectorClass", collector_classes)
    def test_english_property_exists(self, CollectorClass):
        col = CollectorClass()
        english = col.english
        assert(isinstance(english, str)), "Collector should have an english property"