import unittest
import doctest

from Testing.ZopeTestCase import FunctionalDocFileSuite
from base import RememberFunctionalTestBase


def test_suite():
    suite = FunctionalDocFileSuite(
        'control_panel.txt',
        package='Products.remember.tests',
        optionflags=doctest.ELLIPSIS|doctest.NORMALIZE_WHITESPACE,
        test_class=RememberFunctionalTestBase)
    return suite

if __name__ == "__main__":
    unittest.main(defaultTest='test_suite')
