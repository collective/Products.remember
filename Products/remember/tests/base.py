from zope.app.component.hooks import setSite
from zope.app.component.hooks import setHooks

import transaction as txn

from AccessControl.SecurityManagement import newSecurityManager

from Testing                 import ZopeTestCase
from Products.CMFCore.utils  import getToolByName
from Products.PloneTestCase import layer
from Products.CMFPlone.tests.PloneTestCase import PloneTestCase

import Products.remember.config as config
from Products.remember.utils import parseDependencies
from Products.remember.tools.memberdata import MemberDataContainer

SiteLayer = layer.PloneSite

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
all_num_remem_mems = our_num_remem_mems + 1  # PortalTestCase creates a remember member during setup
all_mems = all_num_remem_mems + 1            # 1 Non remember member is created during setup

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
    # stuff the fullname into the request so the reg email notifier
    # can extract it and put it into the outgoing email
    req = context.REQUEST
    req.form['fullname'] = mem_data.get(name, {}).get('fullname', '')
    mdata = getToolByName(context, 'portal_memberdata')
    mem   = makeContent(mdata, name, config.DEFAULT_MEMBER_TYPE)
    # ensure ownership is properly assigned
    mem.setId(name)
    data = def_mem_data.copy()
    # mem_data now only contains properties BEYOND those specified in def_mem_data
    data.update(mem_data.get(name, {}))
    mem.update(**data)
    return mem

    
class RememberProfileLayer(SiteLayer):

    @classmethod
    def setUp(cls):
        """
        do all universal remember project test initialization in the
        layer here this layer is for tests that are
        non-destructive. destructive tests need to go in a sub-layer
        """
        txn.begin()
        app = ZopeTestCase.app()

        setHooks()
        setSite(app.plone)

        # BBB: Plone 3.0 no longer allows anonymous users to join by
        # default.  This should be removed and the tests adjusted when
        # Plone 2.5 is no longer supported in trunk
        app.plone.manage_permission(
            'Add portal member', roles=[], acquire=1)

        setup_tool = app.plone.portal_setup

        # XXX: ugly hack to work around interference from the inherited
        # 'description' attribute
        if type(MemberDataContainer.description) != property:
            MemberDataContainer.description = property(
                fget = MemberDataContainer._nope,
                fset = MemberDataContainer._setDescription)

        setup_tool.runAllImportStepsFromProfile('profile-membrane:default')
        setup_tool.runAllImportStepsFromProfile('profile-remember:default')

        # mock sending emails
        rtool = getToolByName(app.plone, 'portal_registration')
        rtool.MailHost = MailHostMock()
        rtool.mail_password_response = do_nothing

        # don't send emails out by default
        ptool = getToolByName(app.plone, 'portal_properties')
        ptool.site_properties.validate_email = 0

        # add all our remember members (as portal_owner)
        user = app.acl_users.getUser('portal_owner')
        newSecurityManager(None, user)
        
        for mem_id in mem_data:
            addMember(app.plone, mem_id)
        
        # stock default plone non-remember user/member
        user_name = 'non_remember_member'
        user_password = 'secret'
        user_role = 'Member'

        uf = app.plone.acl_users
        uf.source_users.doAddUser(user_name, user_password)
        non_remember_member = uf.getUser(user_name)
        non_remember_member._addRoles(['Member'])

        txn.commit()

    @classmethod
    def tearDown(cls):
        pass

    @classmethod
    def testSetUp(cls):
        pass

    @classmethod
    def testTearDown(cls):
        pass

def do_nothing(*a):
    """ would make this a lambda, but zodb complains about pickling"""
    return True

class MailHostMock(object):
    """
    mock up the send method so that emails do not actually get sent
    during unit tests we can use this to verify that the registration
    process is still working as expected
    """
    def __init__(self):
        self.mail_text = ''
        self.n_mails = 0
    def send(self, mail_text):
        self.mail_text += mail_text
        self.n_mails += 1
    def validateSingleEmailAddress(self, email):
        return True

# This is the test case. You will have to add test_<methods> to your
# class inorder to assert things about your Product.
class RememberTestBase(PloneTestCase):
    layer = RememberProfileLayer

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
