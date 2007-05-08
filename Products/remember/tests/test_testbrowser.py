import unittest
import doctest

from Testing.ZopeTestCase import FunctionalDocFileSuite
from base import RememberTestBase

def test_suite():
    suite = FunctionalDocFileSuite(
        'control_panel.txt',
        package='Products.remember.tests',
        optionflags=doctest.ELLIPSIS|doctest.NORMALIZE_WHITESPACE,
        test_class=RememberTestBase)
    return suite

if __name__ == "__main__":
    unittest.main(defaultTest='test_suite')
