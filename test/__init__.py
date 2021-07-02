"""Allow test suite execution via `setup.py`."""


from unittest import TestLoader
from . import test_dqstutil


def test_dqstutil_suite():
    """Return test suite object for test runner use."""
    loader = TestLoader()
    suite = loader.loadTestsFromModule(test_dqstutil)
    return suite
