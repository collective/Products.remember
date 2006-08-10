import os, sys
import unittest

from Testing                 import ZopeTestCase
from Products.CMFCore.utils  import getToolByName
from Products.CMFPlone.tests import PloneTestCase
from Products.Archetypes.tests.ArchetypesTestCase import ArcheSiteTestCase

from Products.Five import zcml

import Products.membrane
import Products.remember
import Products.remember.config as config
from Products.remember.utils import parseDependencies
from Products.remember.tools.memberdata import MemberDataContainer

# Dynamic bootstapping based on product config
def installConfiguredProducts():
    config, handler = parseDependencies()

    ZopeTestCase.installProduct("PythonScripts")
    ZopeTestCase.installProduct("Five")

    def registerProduct(values):
        for pkg in values:
            ZopeTestCase.installProduct(pkg, 0)

    handler({'required' : registerProduct,
             'optional' : registerProduct,
             })
    # and finally ourselves
    ZopeTestCase.installProduct("remember")


installConfiguredProducts()


# util for making content in a container
def makeContent(container, id, portal_type, title=None):
    container.invokeFactory(id=id, type_name=portal_type)
    o = getattr(container, id)
    if title is not None:
        o.setTitle(title)
    return o


# This is the test case. You will have to add test_<methods> to your
# class inorder to assert things about your Product.
class rememberProjectTest(ArcheSiteTestCase):
    def afterSetUp(self):
        zcml.load_config('configure.zcml', package=Products.membrane)
        zcml.load_config('configure.zcml', package=Products.remember)
        
        ArcheSiteTestCase.afterSetUp(self)
        setup_tool = self.portal.portal_setup
        setup_tool.setImportContext('profile-membrane:default')
        setup_tool.runAllImportSteps()

        # XXX: ugly hack to work around interference from the inherited
        # 'description' attribute
        if type(MemberDataContainer.description) != property:
            MemberDataContainer.description = property(
                fget = MemberDataContainer._nope,
                fset = MemberDataContainer._setDescription)

        setup_tool.setImportContext('profile-remember:default')
        setup_tool.runAllImportSteps()
        # Because we add skins this needs to be called. Um... ick.
        self._refreshSkinData()
        self.mbtool = self.portal.membrane_tool
        
        # set up some default members
        
        # blank member
        self.blank_member = self.addMember('blank_member')
        
        # basic portal member
        portal_member = self.addMember('portal_member')
        portal_member.setRoles('Member')
        password = 'secret'
        values = {'fullname': 'Portal Member',
                  'email': 'noreply@xxxxxxxxyyyyyy.com',
                  'password': password,
                  'confirm_password': password,
                  }
        # processForm triggers the state change to an active state
        portal_member.processForm(values=values)
        self.portal_member = portal_member

        
        # admin member
        admin_member = self.addMember('admin_user')
        admin_member.setRoles(['Manager','Member'])
        self.admin_member = admin_member

    def addMember(self, id):
        """
        Creates a member object, sets to an active state.
        """
        mdata = self.portal.portal_memberdata
        mem = makeContent(mdata, id, config.DEFAULT_MEMBER_TYPE)
        mem.setEmail('noreply@xxxxxxxxyyyyyy.com')
        wft = self.portal.portal_workflow
        wft.doActionFor(mem, 'trigger')
        return mem

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(rememberProjectTest))
    return suite
