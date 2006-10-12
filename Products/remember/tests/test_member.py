import os, sys
import unittest

from DateTime import DateTime

from base import RememberTestBase
from base import makeContent

from Products.CMFPlone.tests import dummy

from Products.membrane.interfaces import ICategoryMapper
from Products.membrane.config import ACTIVE_STATUS_CATEGORY
from Products.membrane.utils import generateCategorySetIdForType

from Products.remember.config import DEFAULT_MEMBER_TYPE

from Products.CMFCore.utils import getToolByName

class TestMember(RememberTestBase):

    def getUser(self):
        """
        Not simply stored as an attribute b/c we need a newly
        generated user object to be sure we get fresh state
        """
        mem_id = self.portal_member.getId()
        return self.portal.acl_users.getUser(mem_id)
        
    def testCreateNewMember(self):
        wftool = getToolByName(self.portal, 'portal_workflow')
        mdata = self.portal.portal_memberdata
        uf = self.portal.acl_users
        id = 'newmember'
        password = 'secret'
        mem = makeContent(mdata, id, DEFAULT_MEMBER_TYPE)
        review_state = wftool.getInfoFor(mem, 'review_state')
        self.failUnless(review_state == 'new')
        values = {'fullname': 'New Member',
                  'email': 'noreply@xxxxxxxxyyyyyy.com',
                  'password': password,
                  'confirm_password': password,
                  }
        user = uf.authenticate(id, password, self.portal.REQUEST)
        self.failUnless(user is None)

        # processForm triggers the state change to an active state
        mem.processForm(values=values)
        self.failUnless(mem.getId() == id)
        review_state = wftool.getInfoFor(mem, 'review_state')
        self.failUnless(review_state == 'public')
        user = uf.authenticate(id, password, self.portal.REQUEST)
        self.failIf(user is None)
        
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
        self.assertEqual(self.portal_member.getRoles(), test_roles_tuple)

        user_roles = test_roles_tuple + ('Authenticated',)
        self.assertEqual(self.getUser().getRoles(), list(user_roles))

    def testMemberPassword(self):
        # test member's password
        passwd = 'newpasswd'
        mem_id = self.portal_member.getId()
        self.portal_member._setPassword(passwd)
        user = self.portal.acl_users.authenticate(mem_id,
                                                  passwd,
                                                  self.portal.REQUEST)
        self.assertEqual(user.getId(), mem_id)

    def testMemberDomains(self):
        # test member's domains
        self.portal_member.setDomains('127.0.0.1\r\n127.0.0.2\r\n  ')
        self.assertEqual(self.portal_member.getDomains(),
                         ('127.0.0.1', '127.0.0.2'))

    def testMemberEmail(self):
        # test member's email
        email = 'test@test.com'
        self.portal_member.setEmail(email)
        self.assertEqual(self.portal_member.getEmail(), email)
        self.assertEqual(self.getUser().getProperty('email'), email)

    def testMemberLoginTime(self):
        # test member's login time
        new_login_time = DateTime()
        self.portal_member.setLast_login_time(new_login_time)
        self.assertEqual(self.portal_member.getLast_login_time(),
                         new_login_time)

    def testMemberRolesInContext(self):
        self.loginAsPortalOwner()
        portal_member_user = self.portal_member.getUser()
        self.folder.invokeFactory(id='folder1', type_name='Folder')
        folder1 = self.folder['folder1']
        folder1.changeOwnership(self.portal_member)
        folder1.manage_addLocalRoles(portal_member_user.getUserName(),
                                     ('Reviewer',))
        self.failUnless('Reviewer' in
                        portal_member_user.getRolesInContext(folder1))

    def testMemberGroups(self):
        admingrp = 'Administrators'
        user = self.getUser()
        self.failIf(admingrp in user.getGroups())
        self.portal_member.setGroups((admingrp,))
        user = self.getUser()
        self.failUnless(admingrp in user.getGroups())

    def testMemberPortrait(self):
        self.portal_member.setPortrait(dummy.Image())
        self.assertEqual(self.portal_member.getPortrait().data, dummy.GIF)
        self.assertEqual(self.portal_member.getPortrait(),
                         self.getUser().getProperty('portrait'))

    def testMemberPasswordChange(self):
        # create a member's password
        mtool = self.portal.portal_membership
        mem = self.portal_member
        passwd = 'newpasswd'
        mem._setPassword(passwd)
        oldhash = mem.getPassword()

        # now modify the password at the same level as the password form
        newpasswd = 'newerpasswd'
        mtool.setPassword(newpasswd)

        # verify that the password changed
        newhash = mem.getPassword()
        self.failIfEqual(oldhash, newhash)

        # and now verify that the user can login with the changed password
        mem_id = mem.getId()
        user = self.portal.acl_users.authenticate(mem_id,
                                                  newpasswd,
                                                  self.portal.REQUEST)        
        self.assertEqual(mem_id, user.getId())

    def testEmailPasswordCheckbox(self):
        """ 
        test to see if the "Send a mail with the password"
        checkbox appears on joining, but not on editting
        preferences once logged in
        """
        # in addition, a test should be written to verify that for a 
        # member that is not in the acl_users list,
        # the password field should be shown
        self.failIf(self.portal_member.showPasswordField())

    def testPrivateWorkflowTransitions(self):
        """
        verify that the member object states transition correctly
        """
        member_name = 'portal_member'
        m = getattr(self, member_name)

        wft = getToolByName(m, 'portal_workflow')

        def verifyState(state):
            shouldBePrivate = (state == 'private')
            self.failUnless(state == wft.getInfoFor(m, 'review_state'))
            self.failUnless(shouldBePrivate == m.getMakePrivate())

        verifyState('public')

        m.setMakePrivate('1')
        verifyState('private')

        m.setMakePrivate('0')
        verifyState('public')
        

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestMember))
    return suite
