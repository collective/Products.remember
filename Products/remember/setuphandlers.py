from Products.CMFCore.utils import getToolByName

from Products.membrane.setuphandlers import _membraneProfileActive
from Products.membrane.setuphandlers import _doRegisterUserAdderUtility

from Products.PluggableAuthService.interfaces.plugins \
     import IUserAdderPlugin

from utilities import UserAdder
from config import ADDUSER_UTILITY_NAME

PROFILE_ID = "profile-remember:default"

def registerUserAdderUtility(context):
    """ registers the remember IUserAdder utility """
    _doRegisterUserAdderUtility(context, 'remember-useradder',
                                PROFILE_ID, ADDUSER_UTILITY_NAME,
                                UserAdder())

def setupPlugins(context):
    """ initialize membrane plugins """
    portal = context.getSite()
    uf = getToolByName(portal, 'acl_users')
    plugins = uf.plugins

    # Make sure that the UserAdding is handled by membrane
    plugins.movePluginsUp(IUserAdderPlugin, ['membrane_users'])

