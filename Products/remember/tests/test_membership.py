import unittest

from Products.CMFCore.utils import getToolByName

from base import RememberTestBase


class TestMembershipTool(RememberTestBase):
    """
    This test is a vestige from when remember implemented its own
    MembershipTool.  (We're confirming that its removal isn't breaking
    anything.)
    """

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

    def test_addMemberToFolderPermission(self):
        """
        verify that the 'add member to folder' link appears only for
        managers
        """
        self.login('portal_member')
        mdtool = getToolByName(self.portal, 'portal_memberdata')
        self.failUnless('Member' in mdtool.getNotAddableTypes())
        self.loginAsPortalOwner()
        self.failIf('Member' in mdtool.getNotAddableTypes())

    def test_addCustomMemberTypeToFolderPermission(self):
        """
        verify that any custom ReMember-based objects
        are addable only for managers as well.  Tests
        integration of the ReMember UI with the membrane
        tool's listMembraneTypes - Note: this could have
        been done with the Generic Setup test profile
        or with Python.  The latter is done below.
        """
        self.types = self.portal.portal_types

        # Copy Member and make it AnotherMember in types tool
        self.types.manage_pasteObjects(
            self.types.manage_copyObjects('Member'))

        self.types.manage_renameObject('copy_of_Member',
                                       'AnotherMember')

        # Add the "AnotherMember" type to PortalMemberdata's allowed types
        memberdatacontainer = self.types['MemberDataContainer']
        if 'AnotherMember' not in memberdatacontainer.allowed_content_types:
            list(memberdatacontainer.allowed_content_types
                 ).append('AnotherMember')

        # Make sure it's listed as a Membrane Type
        self.portal.membrane_tool.registerMembraneType('AnotherMember')

        # Prove that listMembraneTypes is providing correct values to
        # the memberdata tools implementation of getAllowedMemberTypes
        self.login('portal_member')
        mdtool = getToolByName(self.portal, 'portal_memberdata')
        self.failUnless('AnotherMember' in mdtool.getNotAddableTypes())
        self.loginAsPortalOwner()
        self.failIf('AnotherMember' in mdtool.getNotAddableTypes())


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestMembershipTool))
    return suite
