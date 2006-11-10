import unittest

from AccessControl.SecurityManagement import newSecurityManager

from Products.PythonScripts.PythonScript import manage_addPythonScript

from Products.CMFCore.utils import getToolByName

from base import RememberTestBase
from base import makeContent

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

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestWorkflow))
    return suite
