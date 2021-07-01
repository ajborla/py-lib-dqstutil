"""
Module identifier.

This file is needed to allow the test suite to execute via `setup.py`.
"""


import unittest

from . import test_dqstutil

def test_dqstutil_suite():
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(test_dqstutil)
    return suite
