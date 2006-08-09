import os, sys
import unittest

from DateTime import DateTime

from test_project import rememberProjectTest
from test_project import makeContent

from Products.membrane.interfaces import ICategoryMapper
from Products.membrane.config import ACTIVE_STATUS_CATEGORY
from Products.membrane.utils import generateCategorySetIdForType

from Products.remember.config import DEFAULT_MEMBER_TYPE

from Products.CMFCore.utils import getToolByName

class TestMember(rememberProjectTest):

    def testCreateNewMember(self):
        wf_tool = getToolByName(self.portal, 'portal_workflow')
        mdata = self.portal.portal_memberdata
        id = 'newmember'
        password = 'secret'
        mem = makeContent(mdata, id, DEFAULT_MEMBER_TYPE)
        review_state = wf_tool.getInfoFor(mem, 'review_state')
        self.failUnless(review_state == 'new')
        values = {'fullname': 'New Member',
                  'email': 'noreply@xxxxxxxxyyyyyy.com',
                  'password': password,
                  'confirm_password': password,
                  }
        #transaction.get().commit(True) # processForm needs subtxn commit 
        mem.processForm(values=values)
        self.failUnless(mem.getId() == id)
        self.failUnless(mem.getPassword() == password)
        review_state = wf_tool.getInfoFor(mem, 'review_state')
        self.failUnless(review_state == 'public')
        
    def testMemberTitle(self):
        # title should be fullname, w/ failover to member id
        id = 'newmember'
        # create a new member obj so we get the id we want
        mdata = self.portal.portal_memberdata
        mem = makeContent(mdata, id, DEFAULT_MEMBER_TYPE)
        fullname = 'Full Name'
        mem.setFullname(fullname)
        self.failUnless(mem.Title() == fullname)
        mem.setFullname('')
        self.failUnless(mem.Title() == id)
        
    def testMemberRoles(self):
        # test member roles
        test_roles = str('Reviewer')
        test_roles_tuple = ('Reviewer',)
        self.portal_member.setRoles(test_roles)
        self.failUnless(self.portal_member.getRoles() == test_roles_tuple)

    def testMemberPassword(self):
        # test member's password
        self.portal_member._setPassword('newpasswd')
        self.assertEqual(self.portal_member.getPassword(), 'newpasswd')

    def testMemberDomains(self):
        # test member's domains
        self.portal_member.setDomains('127.0.0.1\r\n127.0.0.2\r\n  ')
        self.assertEqual(self.portal_member.getDomains(), ('127.0.0.1', '127.0.0.2'))

    def testMemberEmail(self):
        # test member's email
        email = 'test@test.com'
        self.portal_member.setEmail(email)
        self.assertEqual(self.portal_member.getEmail(), email)

    def testMemberLoginTime(self):
        # test member's login time
        self.portal_member
        new_login_time = DateTime()
        self.portal_member.setLast_login_time(new_login_time)
        self.assertEqual(self.portal_member.getLast_login_time(), new_login_time)

    def testMemberRolesInContext(self):
        portal_member_user = self.portal_member.getUser()
        self.folder.invokeFactory(id='folder1', type_name='Folder')
        folder1 = self.folder['folder1']
        folder1.changeOwnership(self.portal_member)
        folder1.manage_addLocalRoles(portal_member_user.getUserName(), ('Reviewer',))
        self.failUnless('Reviewer' in portal_member_user.getRolesInContext(folder1))


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestMember))
    return suite
