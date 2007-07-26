from Products.PloneTestCase import PloneTestCase

PloneTestCase.installProduct('membrane')
PloneTestCase.installProduct('remember')
PloneTestCase.installProduct('sampleremember')
PloneTestCase.setupPloneSite(extension_profiles=('membrane:default','remember:default','sampleremember:default', ))

class TestInstall(PloneTestCase.PloneTestCase):

    def afterSetUp(self):
        self.workflow = self.portal.portal_workflow

    def testWorkflowInstall(self):
        for w in ('member_approval_workflow','member_auto_workflow'):
            self.failUnless(w in self.workflow.getWorkflowIds(),
                            'workflow(s) not installed')
 
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestInstall))
    return suite

if __name__ == '__main__':
    framework()
