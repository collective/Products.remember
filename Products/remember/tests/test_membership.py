import os, sys
import unittest

from base import RememberTestBase

from Products.membrane.interfaces import ICategoryMapper
from Products.membrane.config import ACTIVE_STATUS_CATEGORY
from Products.membrane.utils import generateCategorySetIdForType

from Products.remember.config import DEFAULT_MEMBER_TYPE

class TestMembershipTool(RememberTestBase):

    def afterSetUp(self):
        RememberTestBase.afterSetUp(self)
        self.mtool = self.portal.portal_membership
        self.uf = self.portal.acl_users
        self.login('admin_member')

    def test_addMember(self):
        id = 'new_member'
        self.mtool.addMember(id, 'secret', ('Member',), tuple)
        user = self.uf.getUser(id)
        self.failIf(user is None)

    def test_deleteMembers(self):
        self.mtool.addMember('new_member', 'secret', ('Member',), tuple)
        del_ids = ('new_member', 'portal_member')
        self.mtool.deleteMembers(del_ids)
        for del_id in del_ids:
            self.failUnless(self.mtool.getMemberById(del_id) is None)

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestMembershipTool))
    return suite
