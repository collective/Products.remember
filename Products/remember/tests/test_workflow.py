import unittest

from AccessControl.SecurityManagement import newSecurityManager

from Products.PythonScripts.PythonScript import manage_addPythonScript

from Products.remember.config import DEFAULT_MEMBER_TYPE

from Products.CMFCore.utils import getToolByName

from base import RememberTestBase
from base import makeContent, addMember


class TestWorkflow(RememberTestBase):

    def setupWorkflowScript(self):
        """Setup a dummy workflow script on the plone workflow."""
        wftool = getToolByName(self.portal, 'portal_workflow')
        manage_addPythonScript(wftool.plone_workflow.scripts, 'dummy')
        wftool.plone_workflow.scripts.dummy.ZPythonScript_edit(
            'state_change', '')
        trans = wftool.plone_workflow.transitions.publish
        trans.script_name = 'dummy'
    
    def test_WorkflowScript(self):
        """Make sure that workflows with scripts play nicely with
        remember members."""
        self.login('admin_member')
        self.setupWorkflowScript()
        wftool = getToolByName(self.portal, 'portal_workflow')
        doc = makeContent(self.portal, 'test_doc', 'Document')
        wftool.doActionFor(doc, 'publish')
        self.assertEqual(wftool.getInfoFor(doc, 'review_state'),
                         'published')

    def test_ApprovalWorkflowPublicMemberRegistration(self):
        """Make sure that a new member being approved with a public profile, receive
        its registration mail"""
        # set approval workflow on remember object
        wftool = getToolByName(self.portal, 'portal_workflow')
        wftool.setChainForPortalTypes((DEFAULT_MEMBER_TYPE,), 'member_approval_workflow')
        wftool.updateRoleMappings()
        
        # create new user
        mem = self.addMember('lammy')
        # check if new user state is pending
        self.assertEqual(wftool.getInfoFor(mem, 'review_state'),
                                'pending')
        
        # save current state to revert back later
        rtool = getToolByName(self.portal, 'portal_registration')
        mh = rtool.MailHost
        ptool = getToolByName(self.portal, 'portal_properties')
        ptool.site_properties.validate_email = 1
        old_mailtext = mh.mail_text
        old_n_mails = mh.n_mails

        mh.mail_text = ''
        mh.n_mails = 0
        
        # approve new member
        self.login('admin_member')
        wftool.doActionFor(mem, 'register_public')
        
        # check if registration mail is sent
        self.assertEqual(mh.mail_text.count('Welcome'), 1)
        self.assertEqual(mh.n_mails, 1)

        # tear down changes made by current test
        mh.mail_text = old_mailtext
        mh.n_mails = old_n_mails
        ptool.site_properties.validate_email = 0
        wftool.setChainForPortalTypes((DEFAULT_MEMBER_TYPE,), 'member_auto_workflow')
        wftool.updateRoleMappings()
        
    def test_ApprovalWorkflowPrivateMemberRegistration(self):
        """Make sure that a new member being approved with a private profile, receive
        its registration mail"""
        # set approval workflow on remember object
        wftool = getToolByName(self.portal, 'portal_workflow')
        wftool.setChainForPortalTypes((DEFAULT_MEMBER_TYPE,), 'member_approval_workflow')
        wftool.updateRoleMappings()
        
        # create new user
        mem = self.addMember('lammy')
        # check if new user state is pending
        self.assertEqual(wftool.getInfoFor(mem, 'review_state'),
                                'pending')
        
        # save current state to revert back later
        rtool = getToolByName(self.portal, 'portal_registration')
        mh = rtool.MailHost
        ptool = getToolByName(self.portal, 'portal_properties')
        ptool.site_properties.validate_email = 1
        old_mailtext = mh.mail_text
        old_n_mails = mh.n_mails

        mh.mail_text = ''
        mh.n_mails = 0
        
        # approve new member
        self.login('admin_member')
        wftool.doActionFor(mem, 'register_private')
        
        # check if registration mail is sent
        self.assertEqual(mh.mail_text.count('Welcome'), 1)
        self.assertEqual(mh.n_mails, 1)

        # tear down changes made by current test
        mh.mail_text = old_mailtext
        mh.n_mails = old_n_mails
        ptool.site_properties.validate_email = 0
        wftool.setChainForPortalTypes((DEFAULT_MEMBER_TYPE,), 'member_auto_workflow')
        wftool.updateRoleMappings()


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestWorkflow))
    return suite
