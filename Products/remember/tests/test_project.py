import os, sys
import unittest

if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Testing                 import ZopeTestCase
from Products.CMFCore.utils  import getToolByName
from Products.CMFPlone.tests import PloneTestCase
from Products.Archetypes.tests.ArchetypesTestCase import ArcheSiteTestCase

from Products.Five import zcml

import Products.membrane
import Products.remember
import Products.remember.config as config
from Products.remember.utils import parseDependencies

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
        setup_tool.setImportContext('profile-remember:default')
        setup_tool.runAllImportSteps()
        # Because we add skins this needs to be called. Um... ick.
        self._refreshSkinData()

        self.mbtool = self.portal.membrane_tool


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(rememberProjectTest))
    return suite

if __name__ == '__main__':
    framework()
