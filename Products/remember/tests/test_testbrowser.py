import unittest
#from zope.testing import doctest
import doctest

from Testing.ZopeTestCase import FunctionalDocFileSuite
from base import RememberFunctionalTestBase

optionflags = (doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE |
               doctest.REPORT_NDIFF)


def test_suite():
    doc_suite = FunctionalDocFileSuite(
        'control_panel.txt',
        'reset.txt',
        'reinstall.txt',
        package='Products.remember.tests',
        optionflags=optionflags,
        test_class=RememberFunctionalTestBase)
    return doc_suite

if __name__ == "__main__":
    unittest.main(defaultTest='test_suite')
