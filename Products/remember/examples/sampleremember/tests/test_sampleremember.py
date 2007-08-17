from Products.PloneTestCase import PloneTestCase
from Products.CMFCore.utils import getToolByName
from Products.sampleremember.config import DEFAULT_MEMBER_TYPE

from base import RememberTestBase
from base import makeContent, addMember

from Products.remember.utils import getAdderUtility

from Products.membrane.interfaces import IMembraneUser
from Products.membrane.interfaces import IGroup

from Products.Archetypes.interfaces import IReferenceable

from Products.remember.interfaces import IReMember

from zope.interface import implementedBy, providedBy

class TestRememberBasedContent(RememberTestBase):

    def createMember(self, login="created_user", password="secret", fullname="New Individual"):
        """Creates a remember-based user"""
        
        mdata = self.portal.portal_memberdata
        uf = self.portal.acl_users
        id = login

        mem = makeContent(mdata, id, DEFAULT_MEMBER_TYPE)
        values = {'fullname': fullname,
                  'email': 'noreply@xxxxxxxxyyyyyy.com',
                  'password': password,
                  'confirm_password': password,
                  }

        # processForm triggers the state change to an active state
        mem.processForm(values=values)
        # uf.authenticate brings back MembraneUser
        #user = uf.authenticate(id, password, self.portal.REQUEST)
        return mem

    def afterSetUp(self):
        self.workflow = self.portal.portal_workflow
        self.acl_users = self.portal.acl_users
        self.uf = self.portal.acl_users
        self.mtool = self.portal.portal_membership
      
    def testCreateNewMemberSuccessfully(self):
        wftool = getToolByName(self.portal, 'portal_workflow')
        mdata = self.portal.portal_memberdata
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
        user = self.uf.authenticate(id, password, self.portal.REQUEST)
        self.failUnless(user is None)

        # processForm triggers the state change to an active state
        mem.processForm(values=values)
        self.failUnless(mem.getId() == id)
        review_state = wftool.getInfoFor(mem, 'review_state')
        self.failUnless(review_state == 'public')
        user = self.uf.authenticate(id, password, self.portal.REQUEST)
        self.failIf(user is None)        
        
    def testSetupNewDefaultMember(self):
        """ Did we set the proper default user? """
        addr = getAdderUtility(self.portal)
        self.failUnless(addr.default_member_type == DEFAULT_MEMBER_TYPE)

    def testInterfaces(self):
        individual = self.createMember(login='one_individual', password='secret', fullname="Individual One")
        self.failUnless(IReMember.providedBy(individual), "Individual doesn't provide IReMember")

    def testErrorIntroducedInComputeRoleMap(self):
        """ getInheritedLocalRoles() dying due to result variables being a list instead of normal string,
            so in Plone the Sharing tab created a "cannot concatenate 'str' and 'list' objects" in
            computedRoleMap.py script.
            
            Fix ultimately was deleting toolset.xml (since not needed by our extended type)
        """
        member = self.mtool.getMemberInfo('test_user_1_')
        fullname = member['fullname']
        self.failUnless(type(fullname) == str, "fullname should be a string")
        
class TestInstall(RememberTestBase):

    def testWorkflowInstall(self):
        """ Test install of default remember workflows """
        self.workflow = self.portal.portal_workflow
        for w in ('member_approval_workflow','member_auto_workflow'):
            self.failUnless(w in self.workflow.getWorkflowIds(),
                            'workflow(s) not installed')

    def testTypesInstall(self):
        typeslist = ('SampleRemember', )

        for t in typeslist:
            self.failUnless(t in self.portal.portal_types.objectIds(),
                            '%s content type not installed' % t)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestRememberBasedContent))
    suite.addTest(makeSuite(TestInstall))
    return suite

if __name__ == '__main__':
    framework()
