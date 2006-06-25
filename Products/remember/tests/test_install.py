import os, sys
import unittest

from test_project import rememberProjectTest

from Products.membrane.interfaces import ICategoryMapper
from Products.membrane.config import ACTIVE_STATUS_CATEGORY
from Products.membrane.utils import generateCategorySetIdForType

from Products.remember.config import DEFAULT_MEMBER_TYPE

if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

class TestRememberInstall(rememberProjectTest):

    def testActiveWFStates(self):
        cat_set = generateCategorySetIdForType(DEFAULT_MEMBER_TYPE)
        cat_map = ICategoryMapper(self.mbtool)
        states = cat_map.listCategoryValues(cat_set,
                                            ACTIVE_STATUS_CATEGORY)
        self.failUnless('private' in states and 'public' in states)

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestRememberInstall))
    return suite

if __name__ == '__main__':
    framework()
