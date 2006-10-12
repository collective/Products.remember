import os, sys
import unittest

from zope.component import queryAdapter

import transaction as txn

from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.Permissions import access_contents_information
from AccessControl.Permissions import view

from Testing                 import ZopeTestCase
from Products.CMFCore.utils  import getToolByName
from Products.PloneTestCase.PloneTestCase import PloneTestCase
from Products.Archetypes.tests.ArchetypesTestCase import ArcheSiteTestCase

import Products.membrane
import Products.remember
import Products.remember.config as config
from Products.remember.interfaces import IHashPW
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

mem_password = 'secret'
mem_data = {
    'portal_member':
    {'fullname': 'Portal Member',
     'email': 'noreply@xxxxxxxxyyyyyy.com',
     'password': mem_password,
     'confirm_password': mem_password,
     },
    'default':
    {'email': 'noreply@xxxxxxxxyyyyyy.com',
     },
    }

# util for making content in a container
def makeContent(container, id, portal_type, title=None):
    container.invokeFactory(id=id, type_name=portal_type)
    o = getattr(container, id)
    if title is not None:
        o.setTitle(title)
    return o

def addMember(context, name):
    """
    Creates a member object, sets to an active state.
    """
    mdata = getToolByName(context, 'portal_memberdata')
    wft = getToolByName(context, 'portal_workflow')
    mem = makeContent(mdata, name, config.DEFAULT_MEMBER_TYPE)
    data = mem_data.get(name, mem_data['default'])
    mem.update(**data)
    return mem


class ZTCLayer:
    """
    configuration layer for default ZTC setup
    """
    @classmethod
    def setUp(cls):
        """
        Do all of the ZTC setup that would normally be happening in
        the ZTC base class (copied from ZopeTestCase.ZopeTestCase).
        """

        txn.begin()
        app = ZopeTestCase.app()

        # ZTC global data
        folder_name = 'test_folder_1_'
        user_name = 'test_user_1_'
        user_password = 'secret'
        user_role = 'test_role_1_'

        # ZTC _setupFolder: '''Creates and configures the folder.'''
        standard_permissions = [access_contents_information, view]
        app.manage_addFolder(folder_name)
        folder = getattr(app, folder_name)
        folder._addRole(user_role)
        folder.manage_role(user_role, standard_permissions)

        # ZTC _setupUserFolder: '''Creates the user folder.'''
        folder.manage_addUserFolder()

        # ZTC _setupUser: '''Creates the default user.'''
        uf = folder.acl_users
        uf.userFolderAddUser(user_name, user_password, [user_role], [])

        # ZTC login: '''Logs in.'''
        user = uf.getUserById(user_name)
        if not hasattr(user, 'aq_base'):
            user = user.__of__(uf)
        newSecurityManager(None, user)

        txn.commit()

    @classmethod
    def tearDown(cls):
        pass

class RememberProfileLayer(ZTCLayer):
    @classmethod
    def setUp(cls):
        """
        do all universal remember project test initialization in the layer here
        this layer is for tests that are non-destructive. destructive tests need
        to go in a sub-layer
        """

        txn.begin()
        app = ZopeTestCase.app()

        setup_tool = app.plone.portal_setup
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

        addMember(app.plone, 'blank_member')

        # basic portal member
        portal_member = addMember(app.plone, 'portal_member')
        portal_member.setRoles('Member')

        # admin member
        admin_member = addMember(app.plone, 'admin_member')
        admin_member.setRoles(['Manager','Member'])

        txn.commit()

# This is the test case. You will have to add test_<methods> to your
# class inorder to assert things about your Product.
class RememberTestBase(PloneTestCase):
    layer = RememberProfileLayer

    def addMember(self, name):
        return globals()['addMember'](self.portal, name)

    def afterSetUp(self):
        PloneTestCase.afterSetUp(self)
        # Because we add skins this needs to be called. Um... ick.
        self._refreshSkinData()

        # define some instance variables for convenience
        self.mbtool = self.portal.membrane_tool
        mtool = self.mtool = getToolByName(self.portal,
                                           'portal_membership')
        
        self.blank_member = mtool.getMemberById('blank_member')
        self.portal_member = mtool.getMemberById('portal_member')
        self.admin_member = mtool.getMemberById('admin_member')
