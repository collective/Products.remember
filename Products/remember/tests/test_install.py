import os, sys
import unittest

from test_project import RememberProjectTest

from Products.membrane.interfaces import ICategoryMapper
from Products.membrane.config import ACTIVE_STATUS_CATEGORY
from Products.membrane.utils import generateCategorySetIdForType

from Products.remember.config import DEFAULT_MEMBER_TYPE

class TestRememberInstall(RememberProjectTest):

    def testActiveWFStates(self):
        cat_set = generateCategorySetIdForType(DEFAULT_MEMBER_TYPE)
        cat_map = ICategoryMapper(self.mbtool)
        states = cat_map.listCategoryValues(cat_set,
                                            ACTIVE_STATUS_CATEGORY)
        self.failUnless('private' in states and 'public' in states)

    def testPreferencesURL(self):
        prefs_url = self.portal.restrictedTraverse('prefs_url')()
        self.assertEqual(prefs_url,
                         '%s/personalize_form' % self.portal.absolute_url())
        mem = self.addMember('henry')
        self.login('henry')
        prefs_url = self.portal.restrictedTraverse('prefs_url')()
        self.assertEqual(prefs_url,
                         '%s/edit' % mem.absolute_url())


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestRememberInstall))
    return suite
