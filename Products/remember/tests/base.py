from Testing import ZopeTestCase
from Zope2.App import zcml
from Products.Five import fiveconfigure

from Products.CMFCore.utils import getToolByName

from Products.CMFPlone.tests.PloneTestCase import PloneTestCase
from Products.CMFPlone.tests.PloneTestCase import FunctionalTestCase

from collective.testcaselayer import ptc as tcl_ptc
from collective.testcaselayer import mail

import Products.remember.config as config
import Products.remember
from Products.remember.tools.memberdata import MemberDataContainer

ZopeTestCase.installProduct("membrane")
ZopeTestCase.installProduct("remember")


def load_zcml_of_testing_profile():
    fiveconfigure.debug_mode = True
    zcml.load_config('testing.zcml', package=Products.remember)
    fiveconfigure.debug_mode = False


mem_password = 'secret'
def_mem_data = {
    'email': 'noreply@xxxxxxxxyyyyyy.com',
    'password': mem_password,
    'confirm_password': mem_password,
}

mem_data = {
    'portal_member':
        {
            'fullname': 'Portal Member',
            'mail_me': True,
        },
    'admin_member':
        {
            'roles': ['Manager', 'Member']
        },
    'blank_member':
        {},
}

our_num_remem_mems = len(mem_data.items())
# PortalTestCase creates a remember member during setup
all_num_remem_mems = our_num_remem_mems + 1
# 1 Non remember member is created during setup
all_mems = all_num_remem_mems + 1


# util for making content in a container
def makeContent(container, id, portal_type, title=None):
    container.invokeFactory(id=id, type_name=portal_type)
    o = getattr(container, id)
    if title is not None:
        o.setTitle(title)
    return o


def addMember(context, name, portal_type=config.DEFAULT_MEMBER_TYPE):
    """
    Creates a member object, sets to an active state.
    """
    # stuff the fullname into the request so the reg email notifier
    # can extract it and put it into the outgoing email
    req = context.REQUEST
    req.form['fullname'] = mem_data.get(name, {}).get('fullname', '')
    mdata = getToolByName(context, 'portal_memberdata')
    mem = makeContent(mdata, name, portal_type)
    # ensure ownership is properly assigned
    mem.setId(name)
    data = def_mem_data.copy()
    # mem_data now only contains properties BEYOND those specified in
    # def_mem_data
    data.update(mem_data.get(name, {}))
    mem.update(**data)
    return mem


class RememberProfileLayer(mail.MockMailHostLayer):

    def afterSetUp(self):
        """
        do all universal remember project test initialization in the
        layer here this layer is for tests that are
        non-destructive. destructive tests need to go in a sub-layer
        """

        # BBB: Plone 3.0 no longer allows anonymous users to join by
        # default.  This should be removed and the tests adjusted when
        # Plone 2.5 is no longer supported in trunk
        self.portal.manage_permission(
            'Add portal member', roles=[], acquire=1)

        # XXX: ugly hack to work around interference from the inherited
        # 'description' attribute
        if type(MemberDataContainer.description) != property:
            MemberDataContainer.description = property(
                fget=MemberDataContainer._nope,
                fset=MemberDataContainer._setDescription)

        self.addProfile('Products.remember:default')
        super(RememberProfileLayer, self).afterSetUp()

        # mock sending emails
        rtool = getToolByName(self.portal, 'portal_registration')
        rtool.mail_password_response = do_nothing

        # don't send emails out by default
        ptool = getToolByName(self.portal, 'portal_properties')
        ptool.site_properties.validate_email = 0

        # Make sure the site has a valid mail sending configuration
        self.portal.manage_changeProperties(
            email_from_address='portal_ownwer@nohost.org')

        # add all our remember members (as portal_owner)
        self.loginAsPortalOwner()

        for mem_id in mem_data:
            addMember(self.portal, mem_id)

        # stock default plone non-remember user/member
        user_name = 'non_remember_member'
        user_password = 'secret'
        user_role = 'Member'

        uf = self.portal.acl_users
        uf.source_users.doAddUser(user_name, user_password)
        non_remember_member = uf.getUser(user_name)
        non_remember_member._addRoles([user_role])

remember_profile_layer = RememberProfileLayer([tcl_ptc.ptc_layer])


def do_nothing(*a):
    """ would make this a lambda, but zodb complains about pickling"""
    return True


# This is the test case. You will have to add test_<methods> to your
# class in order to assert things about your Product.
class RememberTestBase(PloneTestCase):
    layer = remember_profile_layer

    def addMember(self, name):
        return globals()['addMember'](self.portal, name)

    def _setup(self):
        # Because we add skins this needs to be called. Um... ick.
        # This needs to happen before users are added so that the
        # workflow guard expressions which depend on skin objects can
        # execute during setup
        self._refreshSkinData()
        return super(RememberTestBase, self)._setup()

    def afterSetUp(self):
        PloneTestCase.afterSetUp(self)

        # define some instance variables for convenience
        self.mbtool = self.portal.membrane_tool
        mtool = self.mtool = getToolByName(self.portal,
                                           'portal_membership')

        self.blank_member = mtool.getMemberById('blank_member')
        self.portal_member = mtool.getMemberById('portal_member')
        self.admin_member = mtool.getMemberById('admin_member')

        self.login('portal_member')


class RememberFunctionalTestBase(FunctionalTestCase, PloneTestCase):
    layer = remember_profile_layer
